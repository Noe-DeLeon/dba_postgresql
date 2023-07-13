import psycopg2
import sys
from tabulate import tabulate

if __name__ == "__main__":
	try:
		args = sys.argv
		bd = args[1]
		url = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format('localhost', bd, 'postgres', 'root')


		conn = psycopg2.connect(url)
		cursor = conn.cursor()

		sql = """SELECT pg_database.datname, pg_user.usename, table_name, 
	        pg_size_pretty(pg_total_relation_size('"' || table_schema || '"."' || table_name || '"')), 
	        pg_total_relation_size('"' || table_schema || '"."' || table_name || '"') 
			FROM information_schema.tables
			INNER JOIN pg_database ON pg_database.datname = table_catalog
			INNER JOIN pg_user ON pg_user.usesysid = pg_database.datdba
			WHERE table_type = 'BASE TABLE'
			{0}""".format(
				"" if bd == 'postgres' else "and table_schema NOT IN('pg_catalog','information_schema')")

		cursor.execute(sql)
		t = []

		for row in cursor:			
			pt = ""
			if int(row[4]) >= 100000:
				pt = '✔'
			t.append([row[0], row[1], row[2], row[3], row[4], pt])
	
		cursor.close()
		print(tabulate(t, tablefmt = 'psql', stralign = 'center', headers = ["Base de datos", "Usuario", "Tabla", "Tamaño", "Tamaño SF", "Partition"]))
	except (Exception, psycopg2.DatabaseError) as e:
	 	print(e)