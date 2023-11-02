"""Módulo de inicio para hacer scraping en computrabajo"""

from Class.Scraper import Scraper
from Class.GHL import GHL_APP

from helper.enums import PlataformsNames

if __name__ == "__main__":

    scraper = Scraper()

    plataforms = scraper.set_plataforms(plataforms=[
        PlataformsNames.Computrabajo.value,
        #PlataformsNames.Linkedin.value,
        #PlataformsNames.Bumeran.value
    ])

    if plataforms:
        scraper.init()
        #scraper.use_external_api(send=GHL_APP)
        scraper.use_external_api(send=False)
        scraper.end()
