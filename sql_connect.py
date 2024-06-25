import psycopg2


#konfigurációs adatok
config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}

#csatlakozás az szerverhez és kurzor létrhozása
def connect():
    try:
        conn = psycopg2.connect(**config) 
        cur = conn.cursor()
        return conn, cur
    except (psycopg2.DatabaseError, Exception) as err:
        print(err)
        return None, None



