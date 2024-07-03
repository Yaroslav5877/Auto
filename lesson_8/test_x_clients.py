# import pytest
# import requests
# from lesson_8.Employee import Employer, Company
# from lesson_8.constants import X_client_URL

# employer = Employer()
# company = Company()

# @pytest.fixture(scope='session')
# def get_token():
#     username = "raphael"
#     password = "cool-but-crude"
#     log_pass = {"username": username, "password": password}
#     resp_token = requests.post(X_client_URL + "/auth/login", json=log_pass)
#     resp_token.raise_for_status()
#     token = resp_token.json()["userToken"]
#     return token

# def test_authorization(get_token):
#     token = get_token
#     assert token is not None
#     assert isinstance(token, str)

# def test_get_company_id():
#     company_id = company.last_active_company_id()
#     assert company_id is not None
#     assert str(company_id).isdigit()

# def test_add_employer(get_token):
#     token = get_token
#     com_id = company.last_active_company_id()
#     body_employer = {
#         'id': 0,
#         'firstName': 'Yarik',
#         'lastName': 'Pon',
#         'middleName': 'Vladich',
#         'companyId': com_id,
#         'email': 'test@mail.ru',
#         'url': 'string',
#         'birthdate': '2024-07-02T11:49:58.124Z',
#         'isActive': 'true'
#     }

#     # Попытка добавить сотрудника без тела (ожидаем ошибку 400)
#     try:
#         employer.add_new(token, {})
#     except requests.exceptions.HTTPError as e:
#         assert e.response.status_code in [400, 401, 500]

# def test_add_employer_without_token():
#     token = ''
#     com_id = company.last_active_company_id()
#     body_employer = {
#         'id': 0,
#         'firstName': 'Yarik',
#         'lastName': 'Pon',
#         'middleName': 'Vladich',
#         'companyId': com_id,
#         'email': 'test@mail.ru',
#         'url': 'string',
#         'birthdate': '2024-07-02T11:49:58.124Z',
#         'isActive': 'true'
#     }

#     # Попытка добавить сотрудника без токена (ожидаем ошибку 401)
#     try:
#         employer.add_new(token, body_employer)
#     except requests.exceptions.HTTPError as e:
#         assert e.response.status_code == 401

# def test_get_employer(get_token):
#     token = get_token
#     com_id = company.last_active_company_id()
#     list_employers = employer.get_list(com_id)
#     assert isinstance(list_employers, list)

# def test_get_list_employers_missing_company_id():
#     with pytest.raises(TypeError) as excinfo:
#         employer.get_list()
#     assert str(excinfo.value) == "Employer.get_list() missing 1 required positional argument: 'company_id'"

# def test_get_list_employers_invalid_company_id():
#     with pytest.raises(requests.exceptions.HTTPError):
#         employer.get_list('invalid_company_id')

# def test_change_employer_info(get_token):
#     token = get_token
#     com_id = company.last_active_company_id()
#     body_employer = {
#         'id': 0,
#         'firstName': 'Yarik',
#         'lastName': 'Pon',
#         'middleName': 'Vladich',
#         'companyId': com_id,
#         'email': 'test@mail.ru',
#         'url': 'string',
#         'birthdate': '2024-07-02T11:49:58.124Z',
#         'isActive': 'true'
#     }

#     # Добавление нового сотрудника
#     try:
#         just_employer = employer.add_new(token, body_employer)
#     except requests.exceptions.HTTPError as e:
#         assert e.response.status_code in [400, 401, 500]
#         just_employer = None

#     if just_employer:
#         # Попытка изменить информацию о сотруднике без обязательных полей (ожидаем ошибку 400)
#         body_change_employer = {}
#         try:
#             employer.change_info(token, just_employer['id'], body_change_employer)
#         except requests.exceptions.HTTPError as e:
#             assert e.response.status_code in [400, 401, 500]

#         # Обновление информации о сотруднике
#         body_employer_update = {
#             'id': just_employer['id'],
#             'firstName': 'UpdatedYarik',
#             'lastName': 'UpdatedPon',
#             'middleName': 'UpdatedVladich',
#             'companyId': com_id,
#             'email': 'updated_test@mail.ru',
#             'url': 'updated_string',
#             'birthdate': '2024-07-02T11:49:58.124Z',
#             'isActive': 'false'
#         }
#         try:
#             updated_employer = employer.change_info(token, just_employer['id'], body_employer_update)
#         except requests.exceptions.HTTPError as e:
#             assert e.response.status_code != 500  # Если возникла ошибка 500, это не нормально
#             raise

#         # Получение измененной информации о сотруднике
#         employer_changed = employer.get_info(just_employer['id'])
#         assert employer_changed['id'] == just_employer['id']
#         assert employer_changed['email'] == body_employer_update['email']

# def test_employers_missing_id_and_token():
#     with pytest.raises(TypeError) as excinfo:
#         employer.change_info()
#     assert str(excinfo.value) == "Employer.change_info() missing 3 required positional arguments: 'token', 'employee_id', and 'body'"

import pytest
import requests
from lesson_8.Employee import Employer, Company
from lesson_8.constants import X_client_URL

employer = Employer()
company = Company()

@pytest.fixture(scope='session')
def get_token():
    username = "raphael"
    password = "cool-but-crude"
    log_pass = {"username": username, "password": password}
    resp_token = requests.post(X_client_URL + "/auth/login", json=log_pass)
    resp_token.raise_for_status()
    token = resp_token.json()["userToken"]
    return token

def test_authorization(get_token):
    token = get_token
    assert token is not None
    assert isinstance(token, str)

def test_get_company_id():
    company_id = company.last_active_company_id()
    assert company_id is not None
    assert str(company_id).isdigit()


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

    # Попытка добавить сотрудника без токена (ожидаем ошибку 401)
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        employer.add_new(token, body_employer)
    assert excinfo.value.response.status_code == 401

def test_get_employer(get_token):
    token = get_token
    com_id = company.last_active_company_id()
    list_employers = employer.get_list(com_id)
    assert isinstance(list_employers, list)

def test_get_list_employers_missing_company_id():
    with pytest.raises(TypeError) as excinfo:
        employer.get_list()
    assert str(excinfo.value) == "Employer.get_list() missing 1 required positional argument: 'company_id'"

def test_get_list_employers_invalid_company_id():
    with pytest.raises(requests.exceptions.HTTPError):
        employer.get_list('invalid_company_id')


def test_employers_missing_id_and_token():
    with pytest.raises(TypeError) as excinfo:
        employer.change_info()
    assert str(excinfo.value) == "Employer.change_info() missing 3 required positional arguments: 'token', 'employee_id', and 'body'"
