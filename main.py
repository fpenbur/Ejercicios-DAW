import mysql.connector
from datetime import date,timedelta
from loan import Loan
from customer import Customer
from movie import Movie
from videoclub import Videoclub

DB_CONFIG = {
    'host':     '127.0.0.1',
    'user':     'usuario',
    'password': 'usuario',
    'database': 'videoclub',
    'port':     3306
}

def vincular(db_config=DB_CONFIG) -> None:
    con = mysql.connector.connect(**db_config)
    con.autocommit = True
    cursor = con.cursor(dictionary=True)
    Loan.con = con
    Loan.cursor = cursor
    Customer.con = con
    Customer.cursor = cursor
    Videoclub.con = con
    Videoclub.cursor = cursor
    Movie.con = con
    Movie.cursor = cursor
def create(db_config=DB_CONFIG):
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    total_copies INT NOT NULL DEFAULT 1,
    avaiable_copies INT NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loan(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    customer_id INT NOT NULL,
    loan_date VARCHAR(10) NOT NULL,
    due_date VARCHAR(10) NOT NULL,
    return_date VARCHAR(10),
    FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
def init(db_config=DB_CONFIG):
    vincular(db_config)
    create(db_config)
init()
videoclub = Videoclub()
while True:
    opcion = input("selecciona una opcion valida: ")
    match opcion:
        case "1":
            title = input("titulo: ")
            director = input("director: ")
            year = int(input("año: "))
            copies = int(input("copias: "))
            videoclub.add_movie(title,director,year,copies)
        case "2":
            name = input("nombre: ")
            phone = input("phone: ")
            videoclub.add_customer(name,phone)
        case "3":
            idpeli = int(input("idpeli: "))
            idcliente = int(input("idcliente: "))
            dias = int(input("dias: "))
            peli = videoclub.get_movie(idpeli)
            cliente = videoclub.get_customer(idcliente)
            prestamo = cliente.borrow(peli,dias)
        case "4":
            idcliente = int(input("idcliente: "))
            idprestamo = int(input("idprestamo: "))
            cliente = videoclub.get_customer(idcliente)
            cliente.return_movie(idprestamo)
        case "5":
            idcliente = int(input("idcliente: "))
            Movie.cursor.execute("SELECT movie.* FROM movie JOIN loan ON loan.movie_id = movie.id WHERE loan.customer_id = %s AND loan.return_date IS NULL ", (idcliente,))
            consulta = Movie.cursor.fetchall()
            for i in consulta:
                peli = Movie.from_db_row(i)
                print(peli.title)
        case "6":
            director = input("director: ")
            for peli in videoclub.search_by_director(director):
                print(f"- {peli.title} ({peli.year})")
        case "7":
            cuantas = int(input("cuantas: "))
            for peli in videoclub.top_rented(cuantas):
                print(f"- {peli.title} (Director: {peli.director})")