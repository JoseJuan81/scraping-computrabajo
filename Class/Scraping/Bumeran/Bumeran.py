import os

from dotenv import load_dotenv
from selenium import webdriver

from Class.Scraping.ScraperBase import ScraperBase

load_dotenv()

USER_EMAIL = os.getenv("BUMERAN_USER_EMAIL")
USER_PASSWORD = os.getenv("BUMERAN_USER_PASSWORD")
LINKEDIN_URL_LOGIN = os.getenv("BUMERAN_URL_LOGIN")

class Bumeran(ScraperBase):
    EMAIL_SELECTOR = "input#user"
    PASS_SELECTOR = "input#password"
    BTN_SELECTOR = "button#ingresar"

    def __init__(self, external_api: str = "") -> None:
        super().__init__() #llama al constructor de ScraperBase

        self.driver: webdriver = None # hereda la propiedad de ScraperBase
        self.user_email: str = USER_EMAIL # hereda la propiedad de ScraperBase
        self.user_password: str = USER_PASSWORD # hereda la propiedad de ScraperBase
        self.login_url: str = LINKEDIN_URL_LOGIN # hereda la propiedad de ScraperBase
        self.external_api = external_api

    def init_web_browser(self) -> None:
        """Funcion para iniciar el webdriver para computrabajo"""

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def login(self) -> None:
        """Funcion para iniciar sesion en plataforma computrabajo"""

        super().login(
            email_selector = self.EMAIL_SELECTOR,
            password_selector = self.PASS_SELECTOR,
            btn_selector = self.BTN_SELECTOR
        )

    def start(self) -> None:
        """Funcion para iniciar proceso de scrping en Bumeran"""
        
        self.init_web_browser()
        self.login()

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
