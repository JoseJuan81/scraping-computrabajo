import threading

from selenium import webdriver
from selenium.webdriver.Remote import _web_element_cls

from helper.enums import PlataformsNames

from Class.Scraping.Computrabajo.Computrabajo import Computrabajo
from Class.Scraping.LinkedIn.LinkedIn import LinkedIn
from Class.Scraping.Bumeran.Bumeran import Bumeran

class Scraper:
    """Clase que realiza el scraping de los candidatos de un anuncio de empleo en computrabajo"""

    def __init__(self) -> None:
        self.driver: webdriver = None
        self.candidates: list = []
        self.next_button: _web_element_cls = None
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

    def save(self) -> None:
        """Funcion para guardar datos recolectados de todas las plataformas"""

        self.end_all_hilos()

        if PlataformsNames.Computrabajo.value in self.plataforms:
            self.computrabajo.save()

        if PlataformsNames.Linkedin.value in self.plataforms:
            self.linkedin.save()

        if PlataformsNames.Bumeran.value in self.plataforms:
            self.bumeran.save()

    def use_external_api(self, send: str = "") -> None:
        """Función que registra las aplicaciones externas para envío de datos"""

        self.external_api = send

    def send_data_to_external_api(self) -> None:
        """Enviar data recolectada a API externa"""

        if PlataformsNames.Computrabajo.value in self.plataforms:
            self.computrabajo.send_data_to_external_api(self.external_api)

        if PlataformsNames.Linkedin.value in self.plataforms:
            self.linkedin.send_data_to_external_api()

        if PlataformsNames.Bumeran.value in self.plataforms:
            self.bumeran.send_data_to_external_api()

    def end(self) -> None:
        """Funcion que muestra el mensaje de FIN del scraping"""
        print("%%"*40)
        print("%%"*40)
        print("FIN")
        print("%%"*40)
        print("%%"*40)

    def computrabajo_hilo(self) -> None:
            self.computrabajo = Computrabajo()
            self.computrabajo.start()

    def linkedin_hilo(self) -> None:
            self.linkedin = LinkedIn()
            self.linkedin.start()

    def bumeran_hilo(self) -> None:
            self.bumeran = Bumeran()
            self.bumeran.start()

    def start_all_hilos(self) -> None:
        """Funcion que inicia todos los hilos creados"""

        for hilo in self.hilos:
            hilo.start()

    def end_all_hilos(self) -> None:
        """Funcion que finaliza todos los hilos"""

        for hilo in self.hilos:
            hilo.join()
    
