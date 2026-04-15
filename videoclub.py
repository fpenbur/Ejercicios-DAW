import mysql.connector
from mysql.connector.connection import MySQLConnection #type: ignore
from mysql.connector.cursor import MySQLCursorDict #type: ignore
from movie import Movie
from customer import Customer
class VideoclubError(Exception):
    pass
class Videoclub:
    con: MySQLConnection = None #type: ignore
    cursor: MySQLCursorDict = None #type: ignore
    def add_movie(self, title: str, director: str, year: int, copies: int = 1):
        peli = Movie(title,director,year,copies)
        peli.save()
    def add_customer(self, name: str, phone: str):
        customer = Customer(name,phone)
        customer.save()
    def get_movie(self, movie_id: int):
        peli = Movie.get(movie_id)
        if peli is None:
            raise ValueError (f"Movie with id {movie_id} does not exist")
        return peli
    def get_customer(self, customer_id: int):
        customer = Customer.get(customer_id)
        if customer is None:
            raise ValueError (f"Customer with id {customer_id} does not exist")
        return customer
    def search_by_director(self, director: str):
        self.cursor.execute("SELECT * FROM movie WHERE director LIKE %s",(f'%{director}%',))
        consulta = self.cursor.fetchall()
        for i in consulta:
            yield Movie.from_db_row(i)
    def top_rented(self, n: int = 5):
        self.cursor.execute("SELECT movie.*,COUNT(loan.id) as l FROM movie JOIN loan ON movie.id = loan.movie_id GROUP BY movie_id ORDER BY l DESC LIMIT %s",(n,))
        consulta = self.cursor.fetchall()
        for i in consulta:
            yield Movie.from_db_row(i)