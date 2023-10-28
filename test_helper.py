from helper.utils import destructure_name, extract_expectation_amount
from helper.enums import CandidateFields


def test_destructure_name():
    """Función que prueba la función destructure_name"""

    name, last_name = destructure_name("")
    assert name == ""
    assert last_name == ""

    name, last_name = destructure_name("jose juan dominguez lopez")
    assert name == "jose juan"
    assert last_name == "dominguez lopez"

    name, last_name = destructure_name("jose dominguez lopez")
    assert name == "jose"
    assert last_name == "dominguez lopez"


def test_expectation_amount():
    data = "Mensual S/. 0.00"
    amount = extract_expectation_amount(data)
    expected = "0.00"

    assert amount == expected


def test_enum():
    expected = "name"

    assert CandidateFields.NAME.value == expected
