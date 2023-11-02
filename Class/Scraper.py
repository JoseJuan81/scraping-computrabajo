import threading

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from helper.enums import PlataformsNames

from Class.Scraping.Computrabajo.Computrabajo import Computrabajo
from Class.Scraping.LinkedIn.LinkedIn import LinkedIn
from Class.Scraping.Bumeran.Bumeran import Bumeran

class Scraper:
    """Clase que realiza el scraping de los candidatos de un anuncio de empleo en computrabajo"""

    def __init__(self) -> None:
        self.driver: webdriver = None
        self.candidates: list = []
        self.next_button: WebElement = None
        self.ghl_contacts: list[dict] = []
        # external api debe ser una list[str] para incluir varias aplicaciones.
        self.external_api: str = ""
        self.job_position: str = ""
        self.plataforms: list[str] = []
        self.hilos: list = []

    def set_plataforms(self, plataforms: list[str] = []) -> bool:
        """Funcion que establece las plataformas de trabajo a escrapear
        (computrabajo, linkedin, bumeran, etc)"""

        if len(plataforms) > 0:
            self.plataforms = plataforms
            return True
        else:
            print("RR"*40)
            print("No selecciono plataforma para scrapear !!!")
            print("RR"*40)
            self.end()

            return False

    def init(self) -> None:
        """Inicio del webdriver por plataforma para hacer scraping"""

        if PlataformsNames.Computrabajo.value in self.plataforms:
            hilo_computrabajo = threading.Thread(target=self.computrabajo_hilo)
            self.hilos.append(hilo_computrabajo)

        if PlataformsNames.Linkedin.value in self.plataforms:
            hilo_linkedin = threading.Thread(target=self.linkedin_hilo)
            self.hilos.append(hilo_linkedin)

        if PlataformsNames.Bumeran.value in self.plataforms:
            hilo_bumeran = threading.Thread(target=self.bumeran_hilo)
            self.hilos.append(hilo_bumeran)

        self.start_all_hilos()

    def use_external_api(self, send: str = "") -> None:
        """Función que registra las aplicaciones externas para envío de datos"""

        self.external_api = send

    def end(self) -> None:
        """Funcion que termina los hilos de ejecucion y 
        muestra el mensaje de FIN del scraping"""

        self.end_all_hilos()

    def computrabajo_hilo(self) -> None:
            self.computrabajo = Computrabajo(external_api = self.external_api)
            self.computrabajo.start()

    def linkedin_hilo(self) -> None:
            self.linkedin = LinkedIn(external_api = self.external_api)
            self.linkedin.start()

    def bumeran_hilo(self) -> None:
            self.bumeran = Bumeran(external_api = self.external_api)
            self.bumeran.start()

    def start_all_hilos(self) -> None:
        """Funcion que inicia todos los hilos creados"""

        for hilo in self.hilos:
            hilo.start()

    def end_all_hilos(self) -> None:
        """Funcion que finaliza todos los hilos"""

        if len(self.hilos) > 0:
            for hilo in self.hilos:
                hilo.join()
    
