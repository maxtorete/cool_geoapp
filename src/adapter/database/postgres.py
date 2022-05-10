import psycopg2


# Connect to your postgres DB
def pg_connection():
    return psycopg2.connect('host=postgres dbname=postgres user=postgres password=mysecretpassword')

