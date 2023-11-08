import os
import time

from selenium.webdriver.remote.webelement import WebElement
from dotenv import load_dotenv
from selenium import webdriver

from Class.Scraping.ScraperBase import ScraperBase
from Class.Scraping.LinkedIn.LinkedPerson import LinkedInPerson as Person
from Class.Scraping.LinkedIn.LinkedInSelectors import LinkedInSelectors

from helper.enums import CandidateFields
from helper.decoradores import tiempo_ejecucion

load_dotenv()

USER_EMAIL = os.getenv("LINKEDIN_USER_EMAIL")
USER_PASSWORD = os.getenv("LINKEDIN_USER_PASSWORD")
LINKEDIN_URL_LOGIN = os.getenv("LINKEDIN_URL_LOGIN")

LINKEDIN = "LinkedIn"

class LinkedIn(ScraperBase, LinkedInSelectors):

    def __init__(self, external_api: str = "") -> None:
        super().__init__() #llama al constructor de ScraperBase

        self.driver: webdriver = None # hereda la propiedad de ScraperBase
        self.user_email: str = USER_EMAIL # hereda la propiedad de ScraperBase
        self.user_password: str = USER_PASSWORD # hereda la propiedad de ScraperBase
        self.login_url: str = LINKEDIN_URL_LOGIN # hereda la propiedad de ScraperBase
        self.external_api: str = external_api
        self.person = Person()
        self.plataform_name = LINKEDIN
        self.candidates: list = []

    @tiempo_ejecucion(LINKEDIN)
    def start(self) -> None:
        """Funcion para iniciar proceso de scrping en LinkedIn"""

        self.init_web_browser()
        self.login()
        self.list_of_candidates()

    def list_of_candidates(self) -> None:
        """Funcion que obtiene los candidatos que ha aplicado"""

        print("...obteniendo los datos de LinkedIn")

        loop_validator = True
        self.job_position = input(
            "Introduce el nombre del puesto de trabajo ( LinkedIn )\n")

        print("%%"*50)
        url = input("Introduzca la url de la página del anuncio en LinkedIn\n")
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
                loop_validator = super().next_page()
            else:
                print("=="*50)
                print("Usuario no quiso hacer el scraping a LinkedIn...le dio miedito :(")
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

    def extract_initial_data_from_candidates(self, candidates: list = []) -> None:
        """Función para extraer la información de cada candidato desde la
        lista inicial de la pagina del anuncio en Linkedin"""

        local_candidates = []
        for candidate in candidates:
            self.person.set_web_element(candidate)
            self.person.click()

            data = dict([
                (CandidateFields.NAME.value, self.person.name()),
                (CandidateFields.IMAGE.value, self.person.image()),
                (CandidateFields.PROFILE_PAGE.value, self.person.profile_page()),
                (CandidateFields.APPLICATION_TIME.value, self.person.application_time()),
                (CandidateFields.WORK_EXPERIENCE.value, self.person.work_experience()),
                (CandidateFields.EMAIL.value, self.person.email()),
                (CandidateFields.PHONE.value, self.person.phone()),
                (CandidateFields.CITY.value, self.person.city()),
            ])

            local_candidates.append(data)

        self.candidates += local_candidates

    def init_web_browser(self) -> None:
        """Funcion para iniciar el webdriver para LinkedIn"""

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

        self.person.set_driver(self.driver)

    def login(self) -> None:
        """Funcion para iniciar sesion en plataforma LinkedIn"""

        super().login(
            email_selector = self.EMAIL_SELECTOR,
            password_selector = self.PASS_SELECTOR,
            btn_selector = self.BTN_SELECTOR
        )
        print("=="*30)
        input("Ingresa el codigo de validacion de ser necesario\n")
    
    def get_next_pagination_button(self) -> WebElement | None:
        """Función que obtiene próximo botón de la paginación y lo retorna"""

        all_buttons = self.get_elements(selector=self.PAGINATION_BUTTONS_SELECTOR)
        current_button = self.get_element(selector=self.PAGINATION_CURRENT_SELECTOR)

        current_index = -1
        for i, button in enumerate(all_buttons):
            if button.text == current_button.text:
                current_index = i
            
        next_index = current_index + 1
        return all_buttons[next_index] if current_index > -1 else None
            

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
