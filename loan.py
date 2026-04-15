import mysql.connector
from mysql.connector.connection import MySQLConnection #type: ignore
from mysql.connector.cursor import MySQLCursorDict #type: ignore
from datetime import date,timedelta
class Loan:
    con: MySQLConnection = None #type: ignore
    cursor: MySQLCursorDict = None #type: ignore
    def __init__(self, movie_id: int, customer_id: int, loan_date: str, due_date: str, return_date: str | None = None, loan_id: int = 0):
        self.movie_id = movie_id
        self.customer_id = customer_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date
        self.loan_id = loan_id
    @property
    def movie_id(self):
        return self.__movie_id
    @movie_id.setter
    def movie_id(self,movie_id):
        self.__movie_id = movie_id
    @property
    def customer_id(self):
        return self.__customer_id
    @customer_id.setter
    def customer_id(self,customer_id):
        self.__customer_id = customer_id
    @property
    def loan_date(self):
        return self.__loan_date
    @loan_date.setter
    def loan_date(self,loan_date):
        self.__loan_date = loan_date
    @property
    def due_date(self):
        return self.__due_date
    @due_date.setter
    def due_date(self,due_date):
        self.__due_date = due_date
    @property
    def return_date(self):
        return self.__return_date
    @return_date.setter
    def return_date(self,return_date):
        self.__return_date = return_date
    @property
    def loan_id(self):
        return self.__loan_id
    @loan_id.setter
    def loan_id(self,loan_id):
        self.__loan_id = loan_id
    def save(self) -> None:
        self.cursor.execute("INSERT INTO loan (movie_id, customer_id, loan_date, due_date, return_date) VALUES (%s,%s,%s,%s,%s)",(self.__movie_id,self.customer_id,self.loan_date,self.due_date,self.return_date,))
        self.loan_id = self.cursor.lastrowid
    def update(self) -> None:
        self.cursor.execute("UPDATE loan SET return_date = %s WHERE id = %s",(self.return_date,self.loan_id,))
    @property
    def is_overdue(self) -> bool:
        self.cursor.execute("SELECT * FROM loan WHERE  id = %s",(self.loan_id,))
        consulta = self.cursor.fetchone()
        if consulta["return_date"] is None and date.today() > date.fromisoformat(self.due_date):
            return True
        return False
    def __repr__(self):
        if self.return_date is None and date.today() < date.fromisoformat(self.due_date):
            return f'Préstamo #{self.loan_id} | Película: {self.movie_id} | Cliente: {self.customer_id} | ACTIVO'
        elif self.return_date is None and date.today() > date.fromisoformat(self.due_date):
            return f'Préstamo #{self.loan_id} | Película: {self.movie_id} | Cliente: {self.customer_id} | VENCIDO'
        elif self.return_date is not None:
            return f'Préstamo #{self.loan_id} | Película: {self.movie_id} | Cliente: {self.customer_id} | DEVUELTO'
    @classmethod
    def from_db_row(cls, row: dict):
        return cls (
            movie_id=row["movie_id"],
            customer_id=row["customer_id"],
            loan_date=row["loan_date"],
            due_date=row["due_date"],
            return_date=row["return_date"],
            loan_id=row["id"]
        )
    @classmethod
    def get(cls, loan_id: int):
        cls.cursor.execute("SELECT * FROM loan WHERE id = %s",(loan_id,))
        consulta = cls.cursor.fetchone()
        if consulta is None:
            return None
        else:
            return cls.from_db_row(consulta)