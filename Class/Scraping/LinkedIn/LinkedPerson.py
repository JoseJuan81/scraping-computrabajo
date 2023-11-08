from Class.Scraping.PersonBase import Person as PersonBase
from Class.Scraping.LinkedIn.LinkedInSelectors import LinkedInSelectors

class LinkedInPerson(PersonBase, LinkedInSelectors):

    def __init__(self) -> None:
        super().__init__()
        self.mas_button_clicked: bool = False

    def mas_button_on_click(self) -> None:
        """Funcion para presionar el boton 'Mas' y mostrar correo y telefono
        del candidato"""

        selector = self.CANDIDATE_MAS_BUTTON
        button = self.get_element(selector=selector)
        button.click()
        self.mas_button_clicked = not self.mas_button_clicked

    def click(self) -> None:
        """Funcion para hacer click en el web_element del candidato"""

        self.web_element.click()

    def email(self) -> str:
        """Función para extraer el correo del candidato"""

        if not self.mas_button_clicked:
            self.mas_button_on_click()

        selector = self.CANDIDATE_EMAIL
        email = self.get_element(selector=selector)
        self.mas_button_on_click()

        return email.text if email else "Sin correo"

    def phone(self) -> str:
        """Función para extraer el teléfono del candidato"""

        if not self.mas_button_clicked:
            self.mas_button_on_click()
        
        selector = self.CANDIDATE_PHONE
        phone = self.get_element(selector=selector)
        self.mas_button_on_click()

        return phone.text if phone else "Sin telefono"

    def city(self) -> str:
        """Función para extraer la ciudad donde reside el candidato"""

        selector = self.CANDIDATE_CITY
        _, city = self.get_elements(selector=selector, web_element=self.web_element)
        return city.text if city else "Sin ciudad"

    def expectation(self) -> str:
        """Función para extraer la expectativa económica del candidato"""

        return "Buscar espectativa de trabajo"

    def profile_page(self) -> str:
        """Función para extraer la url del perfil del candidato"""

        profile_page_selector = self.CANDIDATE_PROFILE_PAGE
        _profile_page = self.get_element(profile_page_selector)
        print("profile page SELECTOR")
        print(self.CANDIDATE_PROFILE_PAGE)
        print("profile page")
        print(_profile_page)
        return _profile_page.get_attribute("href") if _profile_page else "Sin perfil de usuario"

    def work_experience(self) -> str:
        """Función para extraer la experiencia del candidato"""

        experience_selector = self.CANDIDATE_EXPERIENCE
        divs = self.get_elements(selector = experience_selector)

        w_experiences = "\n".join(div.text for div in divs)

        return w_experiences
