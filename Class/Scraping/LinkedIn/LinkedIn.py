import os

from dotenv import load_dotenv
from selenium import webdriver

from Class.Scraping.ScraperBase import ScraperBase

load_dotenv()

USER_EMAIL = os.getenv("LINKEDIN_USER_EMAIL")
USER_PASSWORD = os.getenv("LINKEDIN_USER_PASSWORD")
LINKEDIN_URL_LOGIN = os.getenv("LINKEDIN_URL_LOGIN")

class LinkedIn(ScraperBase):
    email_selector = "input#session_key"
    pass_selector = "input#session_password"
    btn_selector = "button[data-id='sign-in-form__submit-btn']"

    def __init__(self, external_api: str = "") -> None:
        super().__init__() #llama al constructor de ScraperBase

        self.driver: webdriver = None # hereda la propiedad de ScraperBase
        self.user_email: str = USER_EMAIL # hereda la propiedad de ScraperBase
        self.user_password: str = USER_PASSWORD # hereda la propiedad de ScraperBase
        self.login_url: str = LINKEDIN_URL_LOGIN # hereda la propiedad de ScraperBase
        self.external_api: str = external_api

    def init_web_browser(self) -> None:
        """Funcion para iniciar el webdriver para computrabajo"""

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def login(self) -> None:
        """Funcion para iniciar sesion en plataforma computrabajo"""

        super().login(
            email_selector = self.email_selector,
            password_selector = self.pass_selector,
            btn_selector = self.btn_selector
        )
    
    def start(self) -> None:
        """Funcion para iniciar proceso de scrping en LinkedIn"""
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
