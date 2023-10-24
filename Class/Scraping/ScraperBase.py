from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class ScraperBase:
    def __init__(self) -> None:
        self.user_email: str = ""
        self.user_password: str = ""
        self.login_url: str = ""

    def login(self, email_selector:str = "", password_selector:str = "", btn_selector:str = "") -> None:
        """Funcion general para inicio de sesion en plataformas de empleo"""
        
        self.driver.get(self.login_url)

        input_email = self.get_element(email_selector)
        input_pass = self.get_element(password_selector)

        input_email.send_keys(self.user_email)
        input_pass.send_keys(self.user_password)

        btn = self.get_element(btn_selector)
        btn.click()

    def get_elements(self, selector: str, web_element: WebElement) -> list[webdriver]:
        """Funcion que obtiene el elemento html basado en el selector pasado"""

        html = web_element if web_element else self.driver
        try:
            ele = html.find_elements(By.CSS_SELECTOR, selector)
        except:
            ele = []

        return ele

    def get_element(self, selector: str, web_element: WebElement) -> WebElement:
        """Función para obtener 1 elemento html por css Selector"""

        html = web_element if web_element else self.driver
        try:
            ele = html.find_element(By.CSS_SELECTOR, selector)
        except:
            ele = None

        return ele

    def go_to_jobposition_page(self, url) -> None:
        """Función que solicita la url al usuario y luego va a la página de los candidatos"""

        print("%%"*50)
        url = input("Introduzca la url de la página del anuncio\n")
        print("%%"*50)

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
