import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from helper.enums import CandidateFields
from helper.file import save_file_path
class ScraperBase:
    def __init__(self) -> None:
        self.user_email: str = ""
        self.user_password: str = ""
        self.login_url: str = ""
        self.driver: webdriver = None

    def login(self, email_selector:str = "", password_selector:str = "", btn_selector:str = "") -> None:
        """Funcion general para inicio de sesion en plataformas de empleo"""
        
        self.driver.get(self.login_url)

        input_email = self.get_element(selector = email_selector)
        input_pass = self.get_element(selector = password_selector)

        input_email.send_keys(self.user_email)
        input_pass.send_keys(self.user_password)

        btn = self.get_element(selector = btn_selector)
        btn.click()

    def get_elements(self, selector: str = "", web_element: WebElement | None = None) -> list[webdriver]:
        """Funcion que obtiene el elemento html basado en el selector pasado"""

        html = web_element if web_element else self.driver
        try:
            ele = html.find_elements(By.CSS_SELECTOR, selector)
        except:
            ele = []

        return ele

    def get_element(self, selector: str = "", web_element: WebElement | None = None) -> WebElement:
        """Función para obtener 1 elemento html por css Selector"""

        html = web_element if web_element else self.driver
        try:
            ele = html.find_element(By.CSS_SELECTOR, selector)
        except:
            ele = None

        return ele

    def go_to_jobposition_page(self, url: str = "") -> bool:
        """Función que solicita la url al usuario y luego va a la página de los candidatos"""

        validating_url = True

        while validating_url:
            if url:
                self.driver.get(url)
                return True
            else:
                print("!!"*50)
                print("La url no es válida")
                print("Mira bien lo que estas haciendo!!, sino deja de fastidiar")
                print("Vas a intentatrlo otra vez???")

                response = input("s - sí\nn - no\n")
                if response.lower().strip() == "n":
                    return False

                print("!!"*50)

    def get_candidates_webelements(self, selector: str = "") -> list[WebElement]:
        """Función que obtiene y retorna lista de candidatos de la plataforma"""

        candidates = self.get_elements(selector = selector)

        return candidates if candidates else []
    
    def next_page(self, button_selector:str = "") -> None:
        """Función que obtiene el boton de paginación y lo presiona. Retorna True o False"""
        pagination_btn = self.get_next_pagination_button(selector=button_selector)

        if pagination_btn:
            pagination_btn.click()
            return True

        return False
    
    def save_candidates(self, candidates: list = [], file_name: str = "", plataform: str = "") -> list[dict]:
        """Función para guardar lista de candidatos scrapeados"""

        dt = pd.DataFrame.from_dict(candidates, orient="columns")

        _unusefull_data = dt[CandidateFields.NAME.value] != "Sin Nombre"
        dt = dt.loc[_unusefull_data]

        print("Contactos filtrados:")
        print(f"{len(dt.index)} contactos a guardar")
        print("=="*50)

        save_path = save_file_path(f"{plataform}__{file_name}")
        dt.to_csv(save_path, index=False, header=True)

        return dt.to_dict(orient="records")
