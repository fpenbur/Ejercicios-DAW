import mysql.connector
from mysql.connector.connection import MySQLConnection #type: ignore
from mysql.connector.cursor import MySQLCursorDict #type: ignore
class Movie:
    con: MySQLConnection = None #type: ignore
    cursor: MySQLCursorDict = None #type: ignore
    def __init__(self, title:str, director: str, year: int, total_copies: int = 1, avaiable_copies: int = -1, movie_id: int = 0):
        self.title = title
        self.director = director
        self.year = year
        self.total_copies = total_copies
        if avaiable_copies > 0:
            self.__avaiable_copies = avaiable_copies
        else:
            self.__avaiable_copies = total_copies
        self.movie_id = movie_id
    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self,title):
        self.__title = title
    @property
    def director(self):
        return self.__director
    @director.setter
    def director(self,director):
        self.__director = director
    @property
    def year(self):
        return self.__year
    @year.setter
    def year(self,year):
        self.__year = year
    @property
    def total_copies(self):
        return self.__total_copies
    @total_copies.setter
    def total_copies(self,total_copies):
        self.__total_copies = total_copies
    @property
    def avaiable_copies(self):
        return self.__avaiable_copies
    @avaiable_copies.setter
    def avaiable_copies(self,avaiable_copies):
        self.__avaiable_copies = avaiable_copies
    @property
    def movie_id(self):
        return self.__movie_id
    @movie_id.setter
    def movie_id(self,movie_id):
        self.__movie_id = movie_id
    def save(self) -> None:
        self.cursor.execute("INSERT INTO movie (title, director, year, total_copies, avaiable_copies) VALUES (%s,%s,%s,%s,%s)", (self.title,self.director,self.year,self.total_copies,self.avaiable_copies,))
        self.movie_id = self.cursor.lastrowid
        
    def update(self) -> None:
        self.cursor.execute("UPDATE movie SET title = %s, director = %s, year = %s, total_copies = %s, avaiable_copies = %s WHERE id = %s", (self.title,self.director,self.year,self.total_copies,self.avaiable_copies,self.movie_id,))
    @property
    def is_avaiable(self) -> bool:
        if self.avaiable_copies > 0:
            return True
        return False
    def __repr__(self):
        if self.avaiable_copies > 0:
            return f'[✓] {self.title} ({self.year}) - {self.director} (id={self.movie_id})'
        else:
            return f'[✗] {self.title} ({self.year}) - {self.director} (id={self.movie_id})'
    @classmethod
    def from_db_row(cls, row: dict):
        return cls (
            title=row["title"],
            year=row["year"],
            director=row["director"],
            total_copies=row["total_copies"],
            avaiable_copies=row["avaiable_copies"],
            movie_id=row["id"]
        )
    @classmethod
    def get(cls, movie_id: int) -> None:
        cls.cursor.execute("SELECT * FROM movie WHERE id=%s",(movie_id,))
        consulta = cls.cursor.fetchone()
        if consulta is None:
            return None
        else:
            return cls.from_db_row(consulta)