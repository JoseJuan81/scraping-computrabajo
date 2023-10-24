import os

from Class.Scraping.LinkedIn.LinkedIn import LinkedIn
from dotenv import load_dotenv

load_dotenv()

USER_EMAIL = os.getenv("LINKEDIN_USER_EMAIL")
USER_PASSWORD = os.getenv("LINKEDIN_USER_PASSWORD")

def test_has_user_and_pass():
    compu = LinkedIn()

    assert compu.user_email == USER_EMAIL
    assert compu.user_password == USER_PASSWORD

def test_login_selector():
    compu = LinkedIn()

    assert compu.email_selector == "input#session_key"
    assert compu.pass_selector == "input#session_password"
    assert compu.btn_selector == "button[data-id='sign-in-form__submit-btn']"

def test_login():
    link = LinkedIn()
    link.init_web_browser()
    link.login()

    expected_url = "https://www.linkedin.com/feed/?trk=homepage-basic_sign-in-submit"
    current_url = link.driver.current_url

    assert current_url == expected_url

