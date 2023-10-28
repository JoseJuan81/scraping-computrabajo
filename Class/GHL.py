import os
import requests

from pydantic import BaseModel
from typing import Union
from dotenv import load_dotenv

from helper.enums import CandidateFields
from helper.utils import destructure_name

load_dotenv()
GHL_URL = os.getenv("GHL_URL")
GHL_TOKEN = os.getenv("GHL_TOKEN")

GHL_APP = "ghl"

class GHLContactModel(BaseModel):
    address1: Union[str, None] = ""
    email: str
    firstName: str
    lastName: str
    phone: str
    source: str = "computrabajo_scrapper"
    tags: Union[list[str], None] = []
    city: Union[str, None] = ""
    customField: Union[dict, None] = {}

class GoHighLevel:
    def __init__(self, candidate: dict = {}) -> None:
        self.candidate = candidate
        self.custom_fields: dict = {}
        self.tags: list[str] = []

        self.set_tags_in_candidate()

    def set_tags_in_candidate(self) -> None:
        """Funcion para agrgar la propiedad tags en candidate"""

        self.candidate.update({ "tags": [] })

    def set_tags(self, tags: list[str]) -> None:
        """Funcion que establece tags a agregar en cada candidato"""

        self.tags = tags
        self.candidate["tags"] += self.tags

    def send(self) -> None:
        """Función para enviar contacto a Go High Level"""

        _candidate = self.build_ghl_data(self.candidate)
        headers = self.ghl_headers()

        try:
            res = requests.post(GHL_URL, headers=headers, json=_candidate)

            print("&&"*50)
            if res.status_code == 200:
                print("Resultado satisfactorio al crear contactos en GHL")
            else:
                print("Error al crear contacto en GHL")

            print(res.json())
            print("&&"*50)

        except Exception as error:
            print("&&"*50)
            print(
                f"Error al enviar contacto a GHL ({self.candidate[CandidateFields.NAME.value]})")
            print(error)
            print("&&"*50)

    def ghl_headers(self) -> dict:
        """Funcion que construye el header para enviar token de cuenta GHL"""

        headers = dict([
            ("Authorization", f"Bearer {GHL_TOKEN}"),
            ("Content-Type", "application/json")
        ])

        return headers
    
    def build_ghl_data(self, candidate: dict = {}) -> dict:
        """Función para transformar la data a la estructura de GHL"""
        
        candidate_name = candidate[CandidateFields.NAME.value]
        first_name, last_name = destructure_name(candidate_name)
        custom_field = self.build_custom_fields(candidate)

        _data = dict([
            ("email", candidate[CandidateFields.EMAIL.value]),
            ("firstName", first_name),
            ("lastName", last_name),
            ("phone", candidate[CandidateFields.PHONE.value]),
            ("address1", candidate[CandidateFields.CITY.value]),
            ("customField", custom_field),
            ("tags", candidate[CandidateFields.TAGS.value])
        ])

        data = GHLContactModel(**_data)
        return data.dict()

    def build_custom_fields(candidate: dict) -> dict:
        """Función para construir campos personalizado para GHL"""

        data = dict([
            ("dni", candidate[CandidateFields.DNI.value]),
            ("expectativa_salarial",
            candidate[CandidateFields.EXPECTATION.value]),
            ("resumen_personal",
            candidate[CandidateFields.PERSONAL_SUMMARY.value]),
            ("experiencia_laboral",
            candidate[CandidateFields.WORK_EXPERIENCE.value]),
        ])

        return data