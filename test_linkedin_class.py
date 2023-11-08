import os
import pytest
from dotenv import load_dotenv

from Class.Scraping.LinkedIn.LinkedIn import LinkedIn
from helper.enums import CandidateFields

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

def test_login_success(logged_in_session):
    link = logged_in_session

    expected_url = "https://www.linkedin.com/feed/?trk=homepage-basic_sign-in-submit"
    current_url = link.driver.current_url

    assert current_url == expected_url

def test_get_candidates_webelements(logged_in_session):
    url = "https://www.linkedin.com/hiring/jobs/3748458706/applicants/21233934333/detail/?r=UNRATED%2CGOOD_FIT%2CMAYBE&sort_by=APPLIED_DATE"
    linkedin = logged_in_session

    linkedin.go_to_jobposition_page(url)
    candidates = linkedin.get_candidates_webelements(selector = linkedin.LIST_OF_CANDIDATES_SELECTOR)

    assert len(candidates) > 20

def test_extract_data_from_candidates(logged_in_session):
    url = "https://www.linkedin.com/hiring/jobs/3748458706/applicants/21233934333/detail/?r=UNRATED%2CGOOD_FIT%2CMAYBE&sort_by=APPLIED_DATE"
    linkedin = logged_in_session

    linkedin.go_to_jobposition_page(url)
    candidates = linkedin.get_candidates_webelements(selector = linkedin.LIST_OF_CANDIDATES_SELECTOR)
    linkedin.extract_initial_data_from_candidates(candidates = candidates[:6])

    q, c = linkedin.candidates[4], linkedin.candidates[5]

    assert q[CandidateFields.NAME.value] == "Pilar Acevedo"
    assert c[CandidateFields.NAME.value] == "Maria Laura Moreno"

    assert q[CandidateFields.IMAGE.value] == "https://media.licdn.com/dms/image/D4D03AQH5Ngqc08J8fg/profile-displayphoto-shrink_100_100/0/1688732704934?e=1704931200&v=beta&t=BCdyErJJ_dHFuFWOBhPxpqv5uMfPh0hmapej6MOJox4"
    assert c[CandidateFields.IMAGE.value] == "https://media.licdn.com/dms/image/D4D03AQEbOK09jh1gBQ/profile-displayphoto-shrink_100_100/0/1698511656263?e=1704931200&v=beta&t=r6O68hjSztYxqeXEVdug34GGSCRbfZdM3ub4tfSBRxM"
    
    assert q[CandidateFields.PROFILE_PAGE.value] == "https://www.linkedin.com/in/pilaracevedo/"
    assert c[CandidateFields.PROFILE_PAGE.value] == "https://www.linkedin.com/in/maria-laura-moreno-b05151196/"
    
    assert "Solicitado Hace" in q[CandidateFields.APPLICATION_TIME.value]
    assert "Solicitado Hace" in c[CandidateFields.APPLICATION_TIME.value]
    
    assert q[CandidateFields.EMAIL.value] == "pilartacevedo@gmail.com"
    assert c[CandidateFields.EMAIL.value] == "morenomarialaura1998@gmail.com"
    
    assert q[CandidateFields.PHONE.value] == "+541130648270"
    assert c[CandidateFields.PHONE.value] == "+541133584119"
    
    assert q[CandidateFields.CITY.value] == "Argentina"
    assert c[CandidateFields.CITY.value] == "Buenos Aires, Provincia de Buenos Aires, Argentina"
    
    assert q[CandidateFields.WORK_EXPERIENCE.value] == "Universidad de Buenos Aires\nEditora, Edición\nAños que estudió: de 2019 a 2023\n2019 – 2023\n\n"
    assert c[CandidateFields.WORK_EXPERIENCE.value] == "E-commerce\nResearch textil SRL (Narrow Jeans)\nAños trabajando: 2021 - actualidad\n2021 – actualidad\nE-commerce\nKinderland jugueteria\nAños trabajando: 2020 - 2021\n2020 – 2021\n\n\n\nUniversidad Nacional de La Matanza\nAsistente Contable, Contabilidad\nAños que estudió: de 2021 a 2021\n2021 – 2021\n\n"

def test_pagination(logged_in_session):
    url = "https://www.linkedin.com/hiring/jobs/3748458706/applicants/21233934333/detail/?r=UNRATED%2CGOOD_FIT%2CMAYBE&sort_by=APPLIED_DATE"
    linkedin = logged_in_session
    linkedin.go_to_jobposition_page(url)

    all_buttons = linkedin.get_elements(selector=linkedin.PAGINATION_BUTTONS_SELECTOR)
    current_button = linkedin.get_element(selector=linkedin.PAGINATION_CURRENT_SELECTOR)

    assert len(all_buttons) == 3
    assert all_buttons[0].text == "1"
    assert all_buttons[1].text == "2"
    assert current_button.text == "1"

    next_btn = linkedin.get_next_pagination_button()
    assert next_btn.text == "2"

    pagination_btn_clicked = linkedin.next_page()
    assert pagination_btn_clicked == True

    new_current_pagination = linkedin.get_next_pagination_button()
    assert new_current_pagination.text == "2"
