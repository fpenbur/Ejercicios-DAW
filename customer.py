import mysql.connector
from mysql.connector.connection import MySQLConnection #type: ignore
from mysql.connector.cursor import MySQLCursorDict #type: ignore
from datetime import date,timedelta
from loan import Loan
from movie import Movie
class VideoclubError(Exception):
    pass
class Customer:
    con: MySQLConnection = None #type: ignore
    cursor: MySQLCursorDict = None #type: ignore
    def __init__(self, name: str, phone: str, customer_id: int = 0):
        self.name = name
        self.phone = phone
        self.customer_id = customer_id
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name
    @property
    def phone(self):
        return self.__phone
    @phone.setter
    def phone(self,phone):
        self.__phone = phone
    @property
    def customer_id(self):
        return self.__customer_id
    @customer_id.setter
    def customer_id(self,customer_id):
        self.__customer_id = customer_id
    def save(self) -> None:
        self.cursor.execute("INSERT INTO customer (name, phone) VALUES (%s,%s)",(self.name,self.phone,))
        self.customer_id = self.cursor.lastrowid
    def borrow(self, movie, days: int = 7):
        if movie.avaiable_copies < 0:
            raise VideoclubError (f"Movie {movie.title} is not avaiable")
        loan_date = date.today()
        due_date  = loan_date + timedelta(days=days)
        prestamo = Loan(
            movie_id=movie.movie_id,
            customer_id=self.customer_id,
            loan_date=loan_date,
            due_date=due_date,
            return_date=None
        )
        prestamo.save()
        movie.avaiable_copies -= 1
        movie.update()
    def return_movie(self, loan_id: int) -> None:
        loan = Loan.get(loan_id)
        if loan is None:
            raise VideoclubError (f"Loan with id {loan_id} does not exist")
        elif loan.return_date is not None:
            raise VideoclubError (f"Loan with id {loan_id} is already returned")
        loan.return_date = date.today()
        loan.update()
        peli = Movie.get(loan.movie_id)
        peli.avaiable_copies += 1
        peli.update()
    @property
    def active_loans(self):
        self.cursor.execute("SELECT * FROM loan WHERE customer_id = %s AND return_date IS NULL", (self.customer_id,))
        consulta = self.cursor.fetchall()
        for i in consulta:
            yield Loan.from_db_row(i)
    def __repr__(self):
        return f'{self.name} ({self.phone}) (id={self.customer_id})'
    @classmethod
    def from_db_row(cls, row: dict):
        return cls (
            name = row["name"],
            phone = row["phone"],
            customer_id = row["id"]
        )
    @classmethod
    def get(cls, customer_id: int) -> None:
        cls.cursor.execute("SELECT * FROM customer WHERE id=%s", (customer_id,))
        consulta = cls.cursor.fetchone()
        if consulta is None:
            return None
        else:
            return cls.from_db_row(consulta)