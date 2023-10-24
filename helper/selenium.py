from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from helper.css_selector import SELECTOR_CANDIDATES, NEXT_PAGE


def get_element(path: str, driver: webdriver) -> WebElement:
    """Función para obtener elementos por css Selector"""

    try:
        ele = driver.find_element(By.CSS_SELECTOR, path)
    except:
        ele = None

    return ele


def get_elements(path: str, driver: webdriver) -> [WebElement]:
    """Función para obtener elementos por css Selector"""

    try:
        ele = driver.find_elements(By.CSS_SELECTOR, path)
    except:
        ele = []

    return ele


def get_candidates_webelements(driver: webdriver) -> [WebElement]:
    """Función que obtiene y retorna los candidatos"""

    candidates = get_elements(SELECTOR_CANDIDATES, driver)

    return candidates if candidates else []


def go_to_jobposition_page(driver: webdriver) -> None:
    """Función que solicita la url al usuario y luego va a la página de los candidatos"""

    print("%%"*50)
    url = input("Introduzca la url de la página del anuncio\n")
    print("%%"*50)

    validating_url = True

    while validating_url:
        if url:
            driver.get(url)
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


def get_next_pagination_button(driver: webdriver) -> WebElement | None:
    """Función que obtiene próximo botón de la paginación y lo retorna"""

    elements_list = get_elements(NEXT_PAGE, driver)
    return elements_list[0] if elements_list else None


def go_to_page(url: str, driver: webdriver) -> None:
    """Función para ir a una determinada página"""

    driver.get(url)
