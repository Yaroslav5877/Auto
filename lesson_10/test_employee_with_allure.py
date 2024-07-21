import json
from datetime import datetime, date

import pytest
import requests
import allure
from Employee import Employer, Company
from constants import X_client_URL
from Database import Database

employer = Employer()
company = Company()
database = Database()


@pytest.fixture(scope='session')
def get_token():
    username = "raphael"
    password = "cool-but-crude"
    log_pass = {"username": username, "password": password}
    resp_token = requests.post(X_client_URL + "/auth/login", json=log_pass)
    resp_token.raise_for_status()
    token = resp_token.json()["userToken"]
    return token


@pytest.fixture(scope='function')
def db_session():
    session = database.create_session()
    yield session
    session.close()


@allure.title("Тест авторизации")
@allure.description("Проверка получения токена авторизации")
@allure.feature("Авторизация")
@allure.severity(allure.severity_level.CRITICAL)
def test_authorization(get_token):
    token = get_token
    assert token is not None
    assert isinstance(token, str)


@allure.title("Тест получения ID компании")
@allure.description("Проверка получения последнего активного ID компании")
@allure.feature("Компания")
@allure.severity(allure.severity_level.NORMAL)
def test_get_company_id():
    company_id = company.last_active_company_id()
    assert company_id is not None
    assert str(company_id).isdigit()


@allure.title("Тест добавления сотрудника без токена")
@allure.description("Проверка ошибки при попытке добавления сотрудника без токена")
@allure.feature("Сотрудник")
@allure.severity(allure.severity_level.NORMAL)
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

    with allure.step("Попытка добавить сотрудника без токена"):
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            employer.add_new(token, body_employer)
        assert excinfo.value.response.status_code == 401


@allure.title("Тест получения списка сотрудников компании")
@allure.description("Проверка получения списка сотрудников компании")
@allure.feature("Сотрудник")
@allure.severity(allure.severity_level.NORMAL)
def test_get_employer(get_token):
    token = get_token
    com_id = company.last_active_company_id()
    list_employers = employer.get_list(com_id)
    assert isinstance(list_employers, list)


@allure.title("Тест ошибки при отсутствии ID компании")
@allure.description("Проверка ошибки при отсутствии ID компании в запросе списка сотрудников")
@allure.feature("Сотрудник")
@allure.severity(allure.severity_level.NORMAL)
def test_get_list_employers_missing_company_id():
    with pytest.raises(TypeError) as excinfo:
        employer.get_list()
    assert str(excinfo.value) == "Employer.get_list() missing 1 required positional argument: 'company_id'"


@allure.title("Тест ошибки при неверном ID компании")
@allure.description("Проверка ошибки при неверном ID компании в запросе списка сотрудников")
@allure.feature("Сотрудник")
@allure.severity(allure.severity_level.NORMAL)
def test_get_list_employers_invalid_company_id():
    with pytest.raises(requests.exceptions.HTTPError):
        employer.get_list('invalid_company_id')


@allure.title("Тест ошибки при отсутствии ID и токена")
@allure.description("Проверка ошибки при отсутствии ID и токена в запросе изменения информации о сотруднике")
@allure.feature("Сотрудник")
@allure.severity(allure.severity_level.NORMAL)
def test_employers_missing_id_and_token():
    with pytest.raises(TypeError) as excinfo:
        employer.change_info()
    assert str(
        excinfo.value) == "Employer.change_info() missing 3 required positional arguments: 'token', 'employee_id', and 'body'"


def datetime_converter(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


# Метод для визуализации
def print_employees(employees, title="Employees"):
    print(f"\n--- {title} ---")
    for emp in employees:
        emp_dict = {col: (val.isoformat() if isinstance(val, datetime) else val) for col, val in emp._mapping.items()}
        print(json.dumps(emp_dict, indent=4, default=datetime_converter))
    print(f"--- End of {title} ---\n")


@allure.title("Тест получения всех сотрудников из базы данных")
@allure.description("Проверка получения всех сотрудников из базы данных и соответствие колонок")
@allure.feature("База данных")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_all_employees_from_db(db_session):
    result = database.get_all_employees(db_session)
    print_employees(result, "All Employees")

    assert isinstance(result, list)

    employees = [dict(row._mapping) for row in result]

    required_columns = ['id', 'is_active', 'create_timestamp', 'change_timestamp', 'first_name', 'last_name',
                        'middle_name', 'phone', 'email', 'birthdate', 'avatar_url', 'company_id']

    for employee in employees:
        assert all(column in employee for column in required_columns)


@allure.title("Тест проверки, что список сотрудников не пустой")
@allure.description("Проверка, что список сотрудников не пустой")
@allure.feature("База данных")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_all_employees_not_empty(db_session):
    employees = database.get_all_employees(db_session)
    assert len(employees) > 0


@allure.title("Тест добавления нового сотрудника")
@allure.description("Проверка добавления нового сотрудника и его наличия в базе данных")
@allure.feature("База данных")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_employee(db_session):
    new_employee = {
        'is_active': True,
        'create_timestamp': '2024-07-02T11:49:58.124',
        'change_timestamp': '2024-07-02T11:49:58.124',
        'first_name': 'Test',
        'last_name': 'User',
        'middle_name': 'Middle',
        'phone': '1234567890',
        'email': 'testuser@example.com',
        'birthdate': '1990-01-01',
        'avatar_url': 'http://example.com/avatar.png',
        'company_id': company.last_active_company_id()
    }

    database.add_employee(db_session, new_employee)
    employees = database.get_all_employees(db_session)

    assert any(employee.email == 'testuser@example.com' for employee in employees)

    last_employee = employees[-1]

    assert last_employee.email == 'testuser@example.com'


@allure.title("Тест удаления сотрудника")
@allure.description("Проверка удаления сотрудника из базы данных")
@allure.feature("База данных")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_employee(db_session):
    new_employee = {
        'is_active': True,
        'create_timestamp': '2024-07-02T11:49:58.124',
        'change_timestamp': '2024-07-02T11:49:58.124',
        'first_name': 'Test',
        'last_name': 'User',
        'middle_name': 'Middle',
        'phone': '1234567890',
        'email': 'testuser@example.com',
        'birthdate': '1990-01-01',
        'avatar_url': 'http://example.com/avatar.png',
        'company_id': company.last_active_company_id()
    }

    database.add_employee(db_session, new_employee)

    employees = database.get_all_employees(db_session)
    employee_id = next(employee.id for employee in employees if employee.email == 'testuser@example.com')

    database.delete_employee(db_session, employee_id)
    employees = database.get_all_employees(db_session)

    assert not any(employee.id == employee_id for employee in employees)


@allure.title("Тест обновления информации о сотруднике")
@allure.description("Проверка обновления информации о сотруднике в базе данных")
@allure.feature("База данных")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_employee(db_session):
    new_employee = {
        'is_active': True,
        'create_timestamp': '2024-07-02T11:49:58.124',
        'change_timestamp': '2024-07-02T11:49:58.124',
        'first_name': 'Test',
        'last_name': 'User',
        'middle_name': 'Middle',
        'phone': '1234567890',
        'email': 'testuser@example.com',
        'birthdate': '1990-01-01',
        'avatar_url': 'http://example.com/avatar.png',
        'company_id': company.last_active_company_id()
    }

    database.add_employee(db_session, new_employee)
    employees = database.get_all_employees(db_session)
    employee_id = next(employee.id for employee in employees if employee.email == 'testuser@example.com')

    updated_employee = {
        'first_name': 'Updated',
        'last_name': 'User'
    }

    database.update_employee(db_session, employee_id, updated_employee)
    employees = database.get_all_employees(db_session)
    database_updated_employee = next(employee for employee in employees if employee.id == employee_id)

    assert database_updated_employee.first_name == 'Updated'
    assert database_updated_employee.last_name == 'User'
