from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

# Строка подключения к БД
db_connection_string = "postgresql+psycopg2://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx"

# Настройка подключения к базе данных
engine = create_engine(db_connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

employee_table = Table(
    'employee', metadata,
    autoload_with=engine
)

class Database:
    def __init__(self):
        """
        Инициализация класса Database.
        """
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.metadata = metadata
        self.employee_table = employee_table

    def create_session(self):
        """
        Создать сессию для работы с базой данных.

        :return: Сессия базы данных.
        :rtype: sqlalchemy.orm.session.Session
        """
        return self.SessionLocal()

    def get_all_employees(self, session):
        """
        Получить всех сотрудников из базы данных.

        :param session: Сессия базы данных.
        :type session: sqlalchemy.orm.session.Session
        :return: Список всех сотрудников.
        :rtype: list
        """
        statement = select(self.employee_table)
        statement_result = session.execute(statement)
        employees = statement_result.fetchall()
        return employees

    def add_employee(self, session, employee_data):
        """
        Добавить нового сотрудника в базу данных.

        :param session: Сессия базы данных.
        :type session: sqlalchemy.orm.session.Session
        :param employee_data: Данные нового сотрудника.
        :type employee_data: dict
        :return: None
        """
        new_employee = self.employee_table.insert().values(**employee_data)
        session.execute(new_employee)
        session.commit()

    def delete_employee(self, session, employee_id):
        """
        Удалить сотрудника из базы данных.

        :param session: Сессия базы данных.
        :type session: sqlalchemy.orm.session.Session
        :param employee_id: ID сотрудника.
        :type employee_id: int
        :return: None
        """
        delete_employee = self.employee_table.delete().where(self.employee_table.c.id == employee_id)
        session.execute(delete_employee)
        session.commit()

    def update_employee(self, session, employee_id, update_data):
        """
        Обновить данные сотрудника в базе данных.

        :param session: Сессия базы данных.
        :type session: sqlalchemy.orm.session.Session
        :param employee_id: ID сотрудника.
        :type employee_id: int
        :param update_data: Обновленные данные сотрудника.
        :type update_data: dict
        :return: None
        """
        update_statement = self.employee_table.update().where(self.employee_table.c.id == employee_id).values(**update_data)
        session.execute(update_statement)
        session.commit()

    def visualize_employees(self):
        """
        Визуализировать данные всех сотрудников.

        :return: None
        """
        session = self.create_session()
        employees = self.get_all_employees(session)
        for emp in employees:
            emp_dict = {col: val for col, val in zip(self.employee_table.columns.keys(), emp)}
            print(emp_dict)
        session.close()