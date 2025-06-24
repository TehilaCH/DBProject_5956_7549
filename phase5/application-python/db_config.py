import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname='IIDF',
        user='chaho',
        password='Hodaya2002',
        host='localhost',
        port='5432'
    )