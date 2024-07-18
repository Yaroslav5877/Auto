import sqlalchemy
from lesson_9.Employee import Employer
from lesson_9.DataBase import DataBase

api = Employer("https://x-clients-be.onrender.com")
db = DataBase('postgresql+psycopg2://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx')



def test_get_list_of_employers():
    db.create_company('Yarik testers', 'cool_company') # Новая компания
    max_id = db.last_company_id() # Получение ID последней созданной компании
    print(max_id)
    db.create_employer(max_id, 'Yarik', 'Pon', 89998887766) # Добавление сотрудника
    db_employer_list = db.get_list_employer(max_id) # БД Список сотрудников последней созданной компании
    api_employer_list = api.get_list(max_id) # API Список сотрудников последней созданной компании
    assert len(db_employer_list) == len(api_employer_list) # Сравнение списков сотрудников полученных из БД и через API
    
    response = (api.get_list(max_id))[0] # Удаление сотрудника из компании для удаления компании
    employer_id = response["id"]
    db.delete_employer(employer_id)
    db.delete(max_id) # Удаление последней созданной компании
    
    
    # Добавление сотрудника для сравнения в БД с API имя, фамилию, статус
def test_add_new_employer():
    db.create_company('Yarik adding new employer', 'employer')
    max_id = db.last_company_id()
    db.create_employer(max_id, "Yarik", "Pon", 89998887766)
    response = (api.get_list(max_id))[0]
    employer_id = response['id']
    assert response['companyID'] == max_id # Сравнение ID компании
    assert response['firstName'] == "Yarik" # Сравнение имени сотрудника с заданным
    assert response['lastName'] == "Pon" # Сравнение фамилии сотрудника с заданным
    assert response['isActive'] == True # Проверяем статус сотрудника
    db.delete_employer(employer_id)
    db.delete(max_id)
    
    # Сравнение информации о сотруднике из API с указанной при создании сотрудника
    def test_assertion_data():
        db.create_company('Employer get id company', 'new')
        max_id = db.last_company_id()
        db.create_employer(max_id, "Yarik", "Pon", 89998887766)
        employer_id = db.get_employer_id(max_id)
        get_api_info = (api.get_info(employer_id)).json()
        assert get_api_info['firstName'] == 'Yarik'
        assert get_api_info['lastName'] == 'Pon'
        assert get_api_info['phone'] == '89998887766'
        db.delete_employer(employer_id)
        db.delete(max_id)
        
    # Сравнение информации о сотруднике из API с измененной информацией в БД 
    def test_update_user_info():
        db.create_company('New updating company', 'test')
        max_id = db.last_company_id()
        db.create_employer(max_id, "Yarik", "Pon", 89998887766)
        employer_id = db.get_employer_id(max_id)
        db.update_employer_info("Pop", employer_id)
        get_api_info = (api.get_info(employer_id)).json()
        assert get_api_info['firstName'] == 'Pop'
        assert get_api_info['lastName'] == 'Pon'
        assert get_api_info['isActive'] == True
        db.delete_employer(employer_id)
        db.delete(max_id)
    
    