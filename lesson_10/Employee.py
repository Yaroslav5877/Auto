import requests
import json
from constants import X_client_URL
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# URL для авторизации и работы с API
path = "/employee/"

class Company:
    def __init__(self, url=X_client_URL):
        self.url = url

    # Последняя активная компания
    def last_active_company_id(self):
        active_params = {"active": "true"}
        response = requests.get(self.url + '/company', params=active_params)
        response.raise_for_status()
        return response.json()[-1]['id']

class Employer:
    def __init__(self, url=X_client_URL):
        self.url = url

    # Список сотрудников компании
    def get_list(self, company_id: int):
        company = {'company': company_id}
        response = requests.get(self.url + '/employee', params=company)
        response.raise_for_status()
        return response.json()

    # Добавление сотрудника в компанию
    def add_new(self, token: str, body: dict):
        headers = {'x-client-token': token}
        logging.debug(f"Добавление нового сотрудника с телом запроса: {body}")
        response = requests.post(self.url + '/employee', headers=headers, json=body)
        logging.debug(f"Ответ сервера: {response.status_code} {response.text}")
        response.raise_for_status()
        return response.json()

    # Получение информации о сотруднике
    def get_info(self, employee_id: int):
        response = requests.get(self.url + path + str(employee_id))
        response.raise_for_status()
        return response.json()

    # Изменение информации о сотруднике
    def change_info(self, token: str, employee_id: int, body: dict):
        headers = {'x-client-token': token}
        response = requests.patch(self.url + path + str(employee_id), headers=headers, json=body)
        response.raise_for_status()
        return response.json()