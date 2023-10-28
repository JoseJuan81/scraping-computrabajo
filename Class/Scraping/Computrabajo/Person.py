from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from Class.Scraping.ScraperBase import ScraperBase

from helper.enums import CandidateFields

class Person(ScraperBase):
    CANDIDATE_AGE = "ul li.edad"
    CANDIDATE_APLICATION_TIME = "ul li.aplicado"
    CANDIDATE_EXPERIENCE = "ul li"
    CANDIDATE_GRADE = "ul li.estudios"
    CANDIDATE_IMG = "ul li.nombre img.lazy"
    CANDIDATE_MATCH = "ul li.adecuacion p"
    CANDIDATE_NAME = "ul li.nombre a"
    CANDIDATE_PROFILE_DATA_LEFT = "ul.small.table li"
    CANDIDATE_PROFILE_DATA_RIGHT = "div.bb1"
    CANDIDATE_PROFILE_PAGE = "ul li.nombre a"

    def __init__(self) -> None :
        self.web_element: WebElement = None

        self.person_data: dict = {}
        self.contact_data_left: list = []
        self.contact_data_right: list = []

    def set_driver(self, driver: webdriver) -> None:
        """Funcion para establecer el driver en person"""
        
        self.driver = driver

    def set_web_element(self, web_element: WebElement) -> None:
        """Funcion para establecer el webelement del candidato"""
        
        self.web_element = web_element

    def set_person_data(self, person_data: dict) -> None:
        """Funcion para establecer el objeto candidato con sus valores"""

        self.person_data = person_data

    def name(self) -> str:
        """Función para extraer el nombre del candidato"""

        _name = self.get_element(self.CANDIDATE_NAME, self.web_element)
        return _name.text if _name else "Sin Nombre"

    def image(self) -> str:
        """Función para extraer la imagen del candidato"""

        _image = self.get_element(self.CANDIDATE_IMG, self.web_element)
        return _image.get_attribute("src") if _image else "Sin Imagen"

    def profile_page(self) -> str:
        """Función para extraer la url del perfil del candidato"""

        _profile_page = self.get_element(self.CANDIDATE_PROFILE_PAGE, self.web_element)
        return _profile_page.get_attribute("href") if _profile_page else "Sin perfil de usuario"

    def application_time(self) -> str:
        """Función para extraer el tiempo en que aplicó al puesto el candidato"""

        _time = self.get_element(self.CANDIDATE_APLICATION_TIME, self.web_element)
        return _time.text if _time else "Sin Tiempo"

    def age(self) -> int:
        """Función para extraer la edad del candidato"""

        _old = self.get_element(self.CANDIDATE_AGE, self.web_element)
        return int(_old.text) if _old else 0

    def grade(self) -> str:
        """Función para extraer nivel de estudios del candidato"""

        _grade = self.get_element(self.CANDIDATE_GRADE, self.web_element)
        return _grade.text if _grade else "Sin estudios"

    def match(self) -> str:
        """Función para extraer el match del candidato al puesto de trabajo"""

        _match = self.get_element(self.CANDIDATE_MATCH, self.web_element)
        return _match.text if _match else "Sin match"

    def go_profile_page(self) -> None:
        """Función para ir a la página de perfil del candidato"""

        url = self.person_data[CandidateFields.PROFILE_PAGE.value]
        self.driver.get(url)

        self.get_left_side_data()
        self.get_right_side_data()

    def get_left_side_data(self) -> None:
        """Función que extrae los datos de la izquierda en la página del candidato"""

        self.contact_data_left = self.get_elements(
            self.CANDIDATE_PROFILE_DATA_LEFT, self.driver)

    def get_right_side_data(self) -> None:
        """Función que extrae los datos de la derecha en la página del candidato"""

        self.contact_data_right = self.get_elements(
            self.CANDIDATE_PROFILE_DATA_RIGHT, self.driver)

    def email(self) -> str:
        """Función para extraer el correo del candidato"""

        return self.contact_data_left[0].text

    def dni(self) -> str:
        """Función para extraer el dni del candidato"""

        return self.contact_data_left[1].text

    def phone(self) -> str:
        """Función para extraer el teléfono del candidato"""

        return self.contact_data_left[2].text

    def city(self) -> str:
        """Función para extraer la ciudad donde reside el candidato"""

        return self.contact_data_left[3].text

    def expectation(self) -> str:
        """Función para extraer la expectativa económica del candidato"""

        _expectation = self.contact_data_left[-1].text
        return _expectation

    def personal_summary(self) -> str:
        """Función para extraer el resumen personal del candidato"""

        return self.contact_data_right[0].text

    def work_experience(self) -> str:
        """Función para extraer la experiencia del candidato"""

        w_experience_div = self.contact_data_right[2]
        lis = self.get_elements(self.CANDIDATE_EXPERIENCE, w_experience_div)

        w_experiences = "\n".join(el.text for el in lis)

        return w_experiences
