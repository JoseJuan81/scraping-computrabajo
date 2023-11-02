from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from Class.Scraping.ScraperBase import ScraperBase

class Person(ScraperBase):

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

        name_selector = self.CANDIDATE_NAME
        _name = self.get_element(selector=name_selector, web_element=self.web_element)
        return _name.text if _name else "Sin Nombre"

    def image(self) -> str:
        """Función para extraer la imagen del candidato"""

        image_selector = self.CANDIDATE_IMG
        _image = self.get_element(selector=image_selector, web_element=self.web_element)
        return _image.get_attribute("src") if _image else "Sin Imagen"

    def profile_page(self) -> str:
        """Función para extraer la url del perfil del candidato"""

        profile_page_selector = self.CANDIDATE_PROFILE_PAGE
        _profile_page = self.get_element(selector=profile_page_selector, web_element=self.web_element)
        return _profile_page.get_attribute("href") if _profile_page else "Sin perfil de usuario"

    def application_time(self) -> str:
        """Función para extraer el tiempo en que aplicó al puesto el candidato"""

        time_selector = self.CANDIDATE_APLICATION_TIME
        _time = self.get_element(selector=time_selector, web_element=self.web_element)
        return _time.text if _time else "Sin Tiempo"

    def age(self) -> int:
        """Función para extraer la edad del candidato"""

        age_selector = self.CANDIDATE_AGE
        _old = self.get_element(selector=age_selector, web_element=self.web_element)
        return int(_old.text) if _old else 0

    def grade(self) -> str:
        """Función para extraer nivel de estudios del candidato"""

        grade_selector = self.CANDIDATE_GRADE
        _grade = self.get_element(selector=grade_selector, web_element=self.web_element)
        return _grade.text if _grade else "Sin estudios"

    def match(self) -> str:
        """Función para extraer el match del candidato al puesto de trabajo"""

        match_selector = self.CANDIDATE_MATCH
        _match = self.get_element(selector=match_selector, web_element=self.web_element)
        return _match.text if _match else "Sin match"
