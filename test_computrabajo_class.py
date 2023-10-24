import os

from Class.Scraping.Computrabajo import Computrabajo
from dotenv import load_dotenv

load_dotenv()

USER_EMAIL = os.getenv("COMPUTRABAJO_USER_EMAIL")
USER_PASSWORD = os.getenv("COMPUTRABAJO_USER_PASSWORD")

def test_has_user_and_pass():
    compu = Computrabajo()

    assert compu.user_email == USER_EMAIL
    assert compu.user_password == USER_PASSWORD

def test_login_selector():
    compu = Computrabajo()

    assert compu.email_selector == "#Email"
    assert compu.pass_selector == "#Password"
    assert compu.btn_selector == "#bbR"

def test_login():
    compu = Computrabajo()
    compu.init_web_browser()
    compu.login()

    expected_url = "https://empresa.pe.computrabajo.com/Company"
    current_url = compu.driver.current_url

    assert current_url == expected_url

