import json
from datetime import datetime, date

import pytest
import requests
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
    print(*resp_token)
    resp_token.raise_for_status()
    token = resp_token.json()["userToken"]
    return token


@pytest.fixture(scope='function')
def db_session():
    session = database.create_session()
    yield session
    session.close()


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


# Новый тест для получения всех сотрудников
def test_get_all_employees_from_db(db_session):
    # Получаем всех сотрудников из базы данных
    result = database.get_all_employees(db_session)
    # Печатаем всех сотрудников для визуализации
    print_employees(result, "All Employees")

    # Проверяем, что результат - это список
    assert isinstance(result, list)

    # Преобразуем каждую строку в словарь с помощью метода `mappings()`
    employees = [dict(row._mapping) for row in result]

    # Определяем необходимые столбцы
    required_columns = ['id', 'is_active', 'create_timestamp', 'change_timestamp', 'first_name', 'last_name',
                        'middle_name', 'phone', 'email', 'birthdate', 'avatar_url', 'company_id']

    # Проверяем, что каждый сотрудник имеет все необходимые столбцы
    for employee in employees:
        assert all(column in employee for column in required_columns)



# Новый тест для проверки, что список сотрудников не пустой
def test_get_all_employees_not_empty(db_session):
    # Получаем всех сотрудников из базы данных
    employees = database.get_all_employees(db_session)
    # Проверяем, что список сотрудников не пустой
    assert len(employees) > 0


# Новый тест для добавления нового сотрудника
def test_add_employee(db_session):
    # Создаем данные для нового сотрудника
    new_employee = {
        'is_active': True,
        'create_timestamp': '2024-07-02 11:49:58.124',
        'change_timestamp': '2024-07-02 11:49:58.124',
        'first_name': 'Test',
        'last_name': 'User',
        'middle_name': 'Middle',
        'phone': '1234567890',
        'email': 'testuser@example.com',
        'birthdate': '1990-01-01',
        'avatar_url': 'http://example.com/avatar.png',
        'company_id': company.last_active_company_id()
    }

    # Добавляем нового сотрудника в базу данных
    database.add_employee(db_session, new_employee)
    # Получаем обновленный список сотрудников
    employees = database.get_all_employees(db_session)

    # Проверяем, что сотрудник с заданным email существует
    assert any(employee.email == 'testuser@example.com' for employee in employees)

    # Проверяем, что сотрудник с заданным email находится в конце списка
    last_employee = employees[-1]
    assert last_employee.email == 'testuser@example.com'


# Новый тест для удаления сотрудника
def test_delete_employee(db_session):
    # Создаем данные для нового сотрудника
    new_employee = {
        'is_active': True,
        'create_timestamp': '2024-07-02 11:49:58.124',
        'change_timestamp': '2024-07-02 11:49:58.124',
        'first_name': 'Test',
        'last_name': 'User',
        'middle_name': 'Middle',
        'phone': '1234567890',
        'email': 'testuser@example.com',
        'birthdate': '1990-01-01',
        'avatar_url': 'http://example.com/avatar.png',
        'company_id': company.last_active_company_id()
    }

    # Добавляем нового сотрудника в базу данных
    database.add_employee(db_session, new_employee)

    # Получаем обновленный список сотрудников
    employees = database.get_all_employees(db_session)
    # Находим ID сотрудника с заданным email
    employee_id = next(employee.id for employee in employees if employee.email == 'testuser@example.com')

    # Удаляем сотрудника из базы данных
    database.delete_employee(db_session, employee_id)
    # Получаем обновленный список сотрудников
    employees = database.get_all_employees(db_session)

    # Проверяем, что сотрудника с данным ID больше нет в базе данных
    assert not any(employee.id == employee_id for employee in employees)


# Новый тест для изменения информации о сотруднике
def test_update_employee(db_session):
    # Создаем данные для нового сотрудника
    new_employee = {
        'is_active': True,
        'create_timestamp': '2024-07-02 11:49:58.124',
        'change_timestamp': '2024-07-02 11:49:58.124',
        'first_name': 'Test',
        'last_name': 'User',
        'middle_name': 'Middle',
        'phone': '1234567890',
        'email': 'testuser@example.com',
        'birthdate': '1990-01-01',
        'avatar_url': 'http://example.com/avatar.png',
        'company_id': company.last_active_company_id()
    }

    # Добавляем нового сотрудника в базу данных
    database.add_employee(db_session, new_employee)
    # Получаем обновленный список сотрудников
    employees = database.get_all_employees(db_session)
    # Находим ID сотрудника с заданным email
    employee_id = next(employee.id for employee in employees if employee.email == 'testuser@example.com')

    # Создаем данные для обновления сотрудника
    updated_employee = {
        'first_name': 'Updated',
        'last_name': 'User'
    }

    # Обновляем информацию о сотруднике в базе данных
    database.update_employee(db_session, employee_id, updated_employee)
    # Получаем обновленный список сотрудников
    employees = database.get_all_employees(db_session)
    # Находим обновленного сотрудника по ID
    database_updated_employee = next(employee for employee in employees if employee.id == employee_id)

    # Проверяем, что информация о сотруднике была обновлена
    assert database_updated_employee.first_name == 'Updated'
    assert database_updated_employee.last_name == 'User'
