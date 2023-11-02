import os

from selenium.webdriver.remote.webelement import WebElement
from dotenv import load_dotenv
from selenium import webdriver

from Class.Scraping.ScraperBase import ScraperBase
from Class.Scraping.Computrabajo.CompuTrabajoPerson import CompuTrabajoPerson as Person
from Class.Scraping.Computrabajo.CompuTrabajoSelectors import CompuTrabajoSelectors
from Class.GHL import GoHighLevel, GHL_APP

from helper.enums import CandidateFields
from helper.decoradores import tiempo_ejecucion

load_dotenv()

USER_EMAIL = os.getenv("COMPUTRABAJO_USER_EMAIL")
USER_PASSWORD = os.getenv("COMPUTRABAJO_USER_PASSWORD")
COMPUTRABAJO_URL_LOGIN = os.getenv("COMPUTRABAJO_URL_LOGIN")

COMPUTRABAJO = "Computrabajo"

class Computrabajo(ScraperBase, CompuTrabajoSelectors):

    def __init__(self, external_api: str = "") -> None:
        super().__init__() #llama al constructor de ScraperBase

        self.user_email: str = USER_EMAIL # hereda la propiedad de ScraperBase
        self.user_password: str = USER_PASSWORD # hereda la propiedad de ScraperBase
        self.login_url: str = COMPUTRABAJO_URL_LOGIN # hereda la propiedad de ScraperBase
        self.job_position: str = ""
        self.candidates: list[WebElement] = []
        self.plataform_name = COMPUTRABAJO
        self.person = Person()
        self.external_api = external_api

    @tiempo_ejecucion(COMPUTRABAJO)
    def start(self) -> None:
        """Funcion para iniciar proceso de scrping en Computrabajo"""
        
        self.init_web_browser()
        self.login()
        self.list_of_candidates()
        self.details_of_candidates()

    def init_web_browser(self) -> None:
        """Funcion para iniciar el webdriver para computrabajo"""

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.person.set_driver(self.driver)

    def login(self) -> None:
        """Funcion para iniciar sesion en plataforma computrabajo"""

        super().login(
            email_selector = self.EMAIL_SELECTOR,
            password_selector = self.PASS_SELECTOR,
            btn_selector = self.BTN_SELECTOR
        )

    def list_of_candidates(self) -> None:
        """Función para obtener candidatos en un determinado puesto de trabajo en computrabajo"""

        print("...obteniendo los datos de Computrabajo")

        loop_validator = True
        self.job_position = input(
            "Introduce el nombre del puesto de trabajo ( Computrabajo )\n")

        print("%%"*50)
        url = input("Introduzca la url de la página del anuncio en Computrabajo\n")
        print("%%"*50)

        # considerar omitir este flujo.
        # Debe ser:
        # Mensaje para que usuario vaya a la pagina y luego presionar enter en la terminal
        # el codigo debe obtener la url de la pagina.
        exist_page_to_scrap = super().go_to_jobposition_page(url)

        counter = 1
        while loop_validator:
            if exist_page_to_scrap:
                print(f"página {counter} ")

                candidates = super().get_candidates_webelements(selector = self.LIST_OF_CANDIDATES_SELECTOR)
                self.extract_initial_data_from_candidates(candidates = candidates)
                loop_validator = super().next_page(button_selector=self.NEXT_PAGE_SELECTOR)
            else:
                print("=="*50)
                print("Usuario no quiso hacer el scraping...le dio miedito :(")
                print("=="*50)

                loop_validator = False

            counter += 1

        if exist_page_to_scrap:
            print("=="*50)
            print(f"Se encontraron {len(self.candidates)} candidatos")

            self.candidates = self.save_candidates(
                candidates=self.candidates,
                file_name=self.job_position,
                plataform=self.plataform_name)
            
            print("información preliminar de los candidatos guardada!!")
            print("__"*50)

    def details_of_candidates(self) -> None:
        """Función para extraer información detallada del candidato de Comoputrabajo"""

        counter = 1
        local_candidates = []
        for candidate in self.candidates:

            print(
                f'{counter} - Candidato: {candidate[CandidateFields.NAME.value]}')

            self.person.set_person_data(candidate)
            self.person.go_profile_page()

            data = dict([
                (CandidateFields.EMAIL.value, self.person.email()),
                (CandidateFields.DNI.value, self.person.dni()),
                (CandidateFields.PHONE.value, self.person.phone()),
                (CandidateFields.CITY.value, self.person.city()),
                (CandidateFields.EXPECTATION.value, self.person.expectation()),
                (CandidateFields.PERSONAL_SUMMARY.value, self.person.personal_summary()),
                (CandidateFields.WORK_EXPERIENCE.value, self.person.work_experience()),
            ])

            candidate_full_data = { **candidate, **data }
            local_candidates.append(candidate_full_data)

            self.send_data_to_external_api(candidate_full_data)
            
            counter += 1

        self.candidates = self.save_data_to_file(local_candidates, self.job_position)
    
    def save_data_to_file(self, candidates: dict = {}, job_position_name: str = "") -> dict:
        """Funcion para guardar la data scrapeada a un archivo tipo .csv"""

        _job_position = f"{self.plataform_name}_{job_position_name}"
        return self.save_candidates(candidates, _job_position)

    def send_data_to_external_api(self, candidate_data: dict = {}) -> None:
        """Función que determina si la información del candidato debe envivarse a una Api externa"""

        if self.external_api == GHL_APP:
            ghl = GoHighLevel(candidate=candidate_data)
            ghl.set_tags([self.plataform_name, self.job_position])
            ghl.send()

    def extract_initial_data_from_candidates(self, candidates: list = []) -> None:
        """Función para extraer la información de cada candidato desde la
        lista inicial de la pagina del anuncio en Computrabajo"""

        local_candidates = []
        for candidate in candidates:
            self.person.set_web_element(candidate)

            data = dict([
                (CandidateFields.NAME.value, self.person.name()),
                (CandidateFields.IMAGE.value, self.person.image()),
                (CandidateFields.PROFILE_PAGE.value, self.person.profile_page()),
                (CandidateFields.APPLICATION_TIME.value, self.person.application_time()),
                (CandidateFields.AGE.value, self.person.age()),
                (CandidateFields.GRADE.value, self.person.grade()),
                (CandidateFields.MATCH.value, self.person.match()),
            ])

            local_candidates.append(data)

        self.candidates += local_candidates

    def get_next_pagination_button(self, selector: str = "") -> WebElement | None:
        """Función que obtiene próximo botón de la paginación y lo retorna"""

        elements_list = self.get_elements(selector=selector)
        return elements_list[0] if elements_list else None
    
    # def descargar_archivo(self) -> None:
    #
    #     url = 'https://www.juntadeandalucia.es/eboja/2021/40/index.html'
    #
    #     driver = webdriver.Edge(executable_path='msedgedriver.exe')
    #     driver.get(url)
    #
    #     boja = driver.find_element_by_link_text('Sumario boletín nº 40')
    #     url_pdf = boja.get_attribute('href')
    #
    #     print(url_pdf) # https://www.juntadeandalucia.es/eboja/2021/40/BOJA21-040-00012_00003686.pdf
    #
    #     driver.get(url_pdf) # Si quieres navegar a la url del pdf en la misma pestaña (no es necesario para descargar el pdf)
    #     r = requests.get(url_pdf, stream=True)
    #
    #     with open('boja1.pdf', 'wb') as f:
    #         f.write(r.content)
