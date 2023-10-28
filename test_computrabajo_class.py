import os
import pytest

from dotenv import load_dotenv

from Class.Scraping.Computrabajo.Computrabajo import Computrabajo

from helper.enums import CandidateFields

load_dotenv()

USER_EMAIL = os.getenv("COMPUTRABAJO_USER_EMAIL")
USER_PASSWORD = os.getenv("COMPUTRABAJO_USER_PASSWORD")

# fixture para inicio de sesion
@pytest.fixture(scope="module")
def logged_in_session():
    compu = Computrabajo()
    compu.init_web_browser()
    compu.login()
    yield compu

def test_has_user_email_and_pass():
    compu = Computrabajo()

    assert compu.user_email == USER_EMAIL
    assert compu.user_password == USER_PASSWORD

def test_login_selector():
    compu = Computrabajo()

    assert compu.EMAIL_SELECTOR == "#Email"
    assert compu.PASS_SELECTOR == "#Password"
    assert compu.BTN_SELECTOR == "#bbR"

def test_login(logged_in_session):
    compu = logged_in_session
    expected_url = "https://empresa.pe.computrabajo.com/Company"
    current_url = compu.driver.current_url

    assert current_url == expected_url


def test_extract_initial_data_from_candidates(logged_in_session):
    url = "https://empresa.pe.computrabajo.com/Company/Offers/Match?oi=3F53912A8623304361373E686DCF3405&cf=469814F59E4D6F04"
    compu = logged_in_session

    compu.go_to_jobposition_page(url)
    candidates = compu.get_candidates_webelements()
    compu.extract_initial_data_from_candidates(candidates)
    first_candidate, *_rest = compu.candidates

    name = first_candidate[CandidateFields.NAME.value]
    image = first_candidate[CandidateFields.IMAGE.value]
    page = first_candidate[CandidateFields.PROFILE_PAGE.value]
    time = first_candidate[CandidateFields.APPLICATION_TIME.value]
    age = first_candidate[CandidateFields.AGE.value]
    grade = first_candidate[CandidateFields.GRADE.value]
    match = first_candidate[CandidateFields.MATCH.value]

    assert type(name) == str
    assert name.lower() != "sin nombre"

    assert type(image) == str
    assert image.lower() != "sin image"

    assert type(page) == str
    assert page.lower() != "sin perfil de usuario"

    assert type(time) == str
    assert time.lower() != "sin tiempo"

    assert type(age) == int
    assert age != 0

    assert type(grade) == str
    assert grade.lower() != "sin estudios"

    assert type(match) == str
    assert match.lower() != "sin match"

def test_next_page(logged_in_session):
    url = "https://empresa.pe.computrabajo.com/Company/Offers/Match?oi=3F53912A8623304361373E686DCF3405&cf=469814F59E4D6F04"
    compu = logged_in_session

    compu.go_to_jobposition_page(url)
    page = compu.next_page()

    assert page == True or page == None

def test_detail_page(logged_in_session):
    url = "https://empresa.pe.computrabajo.com/Company/Offers/Match?oi=3F53912A8623304361373E686DCF3405&cf=469814F59E4D6F04"
    compu = logged_in_session

    compu.go_to_jobposition_page(url)
    candidates = compu.get_candidates_webelements()
    compu.extract_initial_data_from_candidates(candidates)
    first_candidate, *_rest = compu.candidates

    compu.person.set_person_data(first_candidate)
    compu.person.go_profile_page()

    email = compu.person.email()
    dni = compu.person.dni()
    phone = compu.person.phone()
    city = compu.person.city()
    expectation = compu.person.expectation()
    personal_summary = compu.person.personal_summary()
    work_experience = compu.person.work_experience()

    # Estos datos dependen de la url pasada al inicio de la funcion
    assert email.find("@") != -1
    assert len(dni) >= 8
    assert len(phone) >= 8
    assert len(city) >= 5
    assert expectation.find("Mensual") != -1
    assert len(personal_summary) > 10
    assert len(work_experience) > 10
