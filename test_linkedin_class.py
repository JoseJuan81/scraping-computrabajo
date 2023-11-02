import os
import pytest

from Class.Scraping.LinkedIn.LinkedIn import LinkedIn
from dotenv import load_dotenv

load_dotenv()

USER_EMAIL = os.getenv("LINKEDIN_USER_EMAIL")
USER_PASSWORD = os.getenv("LINKEDIN_USER_PASSWORD")

# fixture para inicio de sesion
@pytest.fixture(scope="module")
def logged_in_session():
    link = LinkedIn()
    link.init_web_browser()
    link.login()
    yield link

def test_has_user_and_pass():
    link = LinkedIn()

    assert link.user_email == USER_EMAIL
    assert link.user_password == USER_PASSWORD

def test_login_selector():
    link = LinkedIn()

    assert link.EMAIL_SELECTOR == "input#session_key"
    assert link.PASS_SELECTOR == "input#session_password"
    assert link.BTN_SELECTOR == "button[data-id='sign-in-form__submit-btn']"

def test_login(logged_in_session):
    link = logged_in_session

    expected_url = "https://www.linkedin.com/feed/?trk=homepage-basic_sign-in-submit"
    current_url = link.driver.current_url

    assert current_url == expected_url

def test_get_candidates_webelements(logged_in_session):
    url = "https://www.linkedin.com/hiring/jobs/3748458706/applicants/21233934333/detail/?r=UNRATED%2CGOOD_FIT%2CMAYBE&sort_by=APPLIED_DATE"
    compu = logged_in_session

    compu.go_to_jobposition_page(url)
    candidates = compu.get_candidates_webelements(selector = compu.LIST_OF_CANDIDATES_SELECTOR)

    assert len(candidates) > 0
    assert len(candidates) > 1