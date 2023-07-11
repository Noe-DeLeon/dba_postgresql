import psycopg2
from tabulate import tabulate

if __name__ == "__main__":
    try:
        url = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format('localhost', 'postgres', 'postgres', 'root')


        conn = psycopg2.connect(url)


        cursor = conn.cursor()

        sql = """SELECT 
        pg_database.datname, 
        usename, 
        pg_size_pretty(pg_database_size(pg_database.datname))
        FROM pg_user
        INNER JOIN pg_database 
        ON pg_database.datdba = usesysid;
	"""

        cursor.execute(sql)
        t = [];
        for row in cursor:
            t.append([row[0], row[1], row[2]])
        
        cursor.close()
        print(tabulate(t, headers = ["Base de datos", "User", "Tamaño"]))
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
