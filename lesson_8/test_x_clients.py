import pytest
import requests
from lesson_8.Employee import Employer, Company
from lesson_8.constants import X_client_URL

employer = Employer()
company = Company()


def test_authorization(get_token):
    token = get_token
    assert token is not None
    assert isinstance(token, str)

def test_getcompany_id():
    company_id = company.last_active_company_id()
    assert company_id is not None
    assert str(company_id).isdigit()

def test_add_employer(get_token):
    token = get_token
    com_id = company.last_active_company_id()
    body_employer = {
        'id': 0,
        'firstName': 'Yarik',
        'lastName': 'Pon',
        'middleName': 'Vladich',
        'companyId': com_id,
        'email': 'test@mail.ru',
        'url': 'string',
        'birthdate': '2024-07-02T11:49:58.124Z',
        'isActive': 'true'
    }
    
    # Добавление без тела (ОР ошибка 500)
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        employer.add_new(token, {})
    assert excinfo.value.response.status_code == 500

    # Добавление нового работника
    new_employer = employer.add_new(token, body_employer)
    new_employer_id = new_employer['id']
    assert new_employer_id is not None
    assert str(new_employer_id).isdigit()

    # Запрос для получения информации о новом работнике
    info = employer.get_info(new_employer_id)
    assert info.status_code == 200
    assert info.json()['id'] == new_employer_id

def test_add_employer_without_token():
    token = ''
    com_id = company.last_active_company_id()
    body_employer = {
        'id': 0,
        'firstName': 'Yarik',
        'lastName': 'Pon',
        'middleName': 'Vladich',
        'companyId': com_id,
        'email': 'test@mail.ru',
        'url': 'string',
        'birthdate': '2024-07-02T11:49:58.124Z',
        'isActive': 'true'
    }
    
    # Добавление работника без токена (ОР ошибка 401)
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        employer.add_new(token, body_employer)
    assert excinfo.value.response.status_code == 401

def test_get_employer():
    com_id = company.last_active_company_id()
    list_employers = employer.get_list(com_id)
    assert isinstance(list_employers, list)

def test_get_list_employers_missing_company_id():
    with pytest.raises(TypeError) as excinfo:
        employer.get_list()
    assert str(excinfo.value) == 'Employer.get_list() missing 1 required positional argument: "company_id"'

def test_get_list_employers_invalid_company_id():
    with pytest.raises(TypeError):
        employer.get_list('')

def test_change_employer_info(get_token):
    token = get_token
    com_id = company.last_active_company_id()
    body_employer = {
        'id': 0,
        'firstName': 'Yarik',
        'lastName': 'Pon',
        'middleName': 'Vladich',
        'companyId': com_id,
        'email': 'test@mail.ru',
        'url': 'string',
        'birthdate': '2024-07-02T11:49:58.124Z',
        'isActive': 'true'
    }
    
    # Добавление сотрудника через метод .add_new
    just_employer = employer.add_new(token, body_employer)
    id = just_employer['id']

    # Изменение информации не заполняя обязательные поля (ОР ошибка 500)
    body_change_employer = {}
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        employer.change_info(token, id, body_change_employer)
    assert excinfo.value.response.status_code == 500

    # Получение изменненой информации о работнике
    employer_changed = employer.get_info(id)
    assert employer_changed.status_code == 200
    assert employer_changed.json()['id'] == id
    assert employer_changed.json()['email'] == body_employer['email']

def test_employers_missing_id_and_token():
    with pytest.raises(TypeError) as excinfo:
        employer.change_info()
    assert str(excinfo.value) == "Employer.change_info() missing 3 required positional arguments: 'token', 'employee_id', 'body'"
