from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

# Строка подключения к базе данных
db_connection_string = "postgresql+psycopg2://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx"

# Настройка подключения к базе данных
engine = create_engine(db_connection_string)  # Создаем объект engine для подключения к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Создаем фабрику сессий
metadata = MetaData()  # Создаем объект MetaData для управления схемой базы данных

# Определение таблицы employee
employee_table = Table(
    'employee', metadata,
    autoload_with=engine  # Автоматически загружаем структуру таблицы из базы данных
)

# Класс для работы с базой данных
class Database:
    def __init__(self):
        self.engine = engine  # Инициализация engine
        self.SessionLocal = SessionLocal  # Инициализация фабрики сессий
        self.metadata = metadata  # Инициализация MetaData
        self.employee_table = employee_table  # Инициализация таблицы employee

    # Создание новой сессии
    def create_session(self):
        return self.SessionLocal()

    # Получение всех сотрудников
    def get_all_employees(self, session):
        statement = select(self.employee_table)  # Создаем SQL-запрос для выбора всех записей из таблицы employee
        statement_result = session.execute(statement)  # Выполняем запрос
        employees = statement_result.fetchall()  # Извлекаем все строки результата запроса
        return employees

    # Добавление нового сотрудника
    def add_employee(self, session, employee_data):
        new_employee = self.employee_table.insert().values(**employee_data)  # Создаем SQL-запрос для вставки нового сотрудника
        session.execute(new_employee)  # Выполняем запрос
        session.commit()  # Фиксируем изменения в базе данных

    # Удаление сотрудника
    def delete_employee(self, session, employee_id):
        delete_employee = self.employee_table.delete().where(self.employee_table.c.id == employee_id)  # Создаем SQL-запрос для удаления сотрудника по ID
        session.execute(delete_employee)  # Выполняем запрос
        session.commit()  # Фиксируем изменения в базе данных

    # Обновление информации о сотруднике
    def update_employee(self, session, employee_id, update_data):
        update_statement = self.employee_table.update().where(self.employee_table.c.id == employee_id).values(
            **update_data)  # Создаем SQL-запрос для обновления информации о сотруднике по ID
        session.execute(update_statement)  # Выполняем запрос
        session.commit()  # Фиксируем изменения в базе данных

    # Визуализация всех сотрудников
    def visualize_employees(self):
        session = self.create_session()  # Создаем новую сессию
        employees = self.get_all_employees(session)  # Получаем всех сотрудников
        for emp in employees:
            emp_dict = {col: val for col, val in zip(self.employee_table.columns.keys(), emp)}  # Преобразуем строку результата в словарь
            print(emp_dict)  # Печатаем информацию о сотруднике
        session.close()  # Закрываем сессию