from Class.Scraping.PersonBase import Person as PersonBase
from Class.Scraping.Computrabajo.CompuTrabajoSelectors import CompuTrabajoSelectors

from helper.enums import CandidateFields

class CompuTrabajoPerson(PersonBase, CompuTrabajoSelectors):

    def go_profile_page(self) -> None:
        """Función para ir a la página de perfil del candidato"""

        url = self.person_data[CandidateFields.PROFILE_PAGE.value]
        self.driver.get(url)

        self.get_left_side_data()
        self.get_right_side_data()

    def get_left_side_data(self) -> None:
        """Función que extrae los datos de la izquierda en la página del candidato"""

        data_left_selector = self.CANDIDATE_PROFILE_DATA_LEFT
        self.contact_data_left = self.get_elements(data_left_selector, self.driver)

    def get_right_side_data(self) -> None:
        """Función que extrae los datos de la derecha en la página del candidato"""

        data_right_selector = self.CANDIDATE_PROFILE_DATA_RIGHT
        self.contact_data_right = self.get_elements(
            selector = data_right_selector, web_element = self.driver)

    def email(self) -> str:
        """Función para extraer el correo del candidato"""

        return self.contact_data_left[0].text

    def dni(self) -> str:
        """Función para extraer el dni del candidato"""

        return self.contact_data_left[1].text

    def phone(self) -> str:
        """Función para extraer el teléfono del candidato"""

        return self.contact_data_left[2].text

    def city(self) -> str:
        """Función para extraer la ciudad donde reside el candidato"""

        return self.contact_data_left[3].text

    def expectation(self) -> str:
        """Función para extraer la expectativa económica del candidato"""

        _expectation = self.contact_data_left[-1].text
        return _expectation

    def personal_summary(self) -> str:
        """Función para extraer el resumen personal del candidato"""

        return self.contact_data_right[0].text

    def work_experience(self) -> str:
        """Función para extraer la experiencia del candidato"""

        w_experience_div = self.contact_data_right[2]
        experience_selector = self.CANDIDATE_EXPERIENCE
        lis = self.get_elements(selector = experience_selector, web_element = w_experience_div)

        w_experiences = "\n".join(li.text for li in lis)

        return w_experiences