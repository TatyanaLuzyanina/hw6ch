import psycopg2

conn = psycopg2.connect(database="Project1", user="postgres", password="Belik67306")
cur = conn.cursor()

def CreatTable(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Client(
    	    client_id SERIAL PRIMARY KEY,
    	    firstname VARCHAR(30) NOT NULL,
    	    lastname VARCHAR(30) NOT NULL,
    	    email VARCHAR(30) UNIQUE 
    	);
            """)
    cursor.execute("""
     	CREATE TABLE IF NOT EXISTS Client_Phone(
            client_id INTEGER REFERENCES Client(client_id),
    	    phone CHAR(11) UNIQUE
        );""")
    conn.commit()

def AddClient(cursor, firstname, lastname, email):
    cursor.execute("""
     	INSERT INTO Client(firstname, lastname, email)
     	VALUES(%s, %s , %s)
     	RETURNING client_id, firstname, lastname, email
     	""", (firstname, lastname, email))
    print(cursor.fetchone())

def AddPhone(cursor, phone, client_id):
    cursor.execute("""
        INSERT INTO Client_Phone(client_id, phone)
        VALUES(%s, %s)
        RETURNING client_id, phone;
        """, (client_id, phone))
    print(cursor.fetchone())

def Change_Client(cursor, client_id, firstname = None, lastname = None, email = None):
    cursor.execute("""
    	UPDATE Client
    	SET firstname=%s, lastname=%s, email=%s
    	WHERE client_id=%s
    	RETURNING client_id, firstname, lastname, email;
    	""", (firstname, lastname, email, client_id))
    print(cursor.fetchone())

def Delete_Phone(cursor, phone, client_id):
    cursor.execute("""
		DELETE FROM Client_Phone
		WHERE client_id=%s AND phone=%s;
		""", (client_id, phone))
    print(cursor.fetchone())

def Delete_Client(cursor, client_id):
    cursor.execute("""
    		DELETE FROM Client
    		WHERE client_id=%s;
    		""", (client_id))
    print(cursor.fetchone())
    cursor.execute("""
        		DELETE FROM Client_Phone
        		WHERE client_id=%s;
        		""", (client_id))
    print(cursor.fetchone())

def Find_Client (cursor, firstname=None, lastname=None, email=None, phone=None):
	cursor.execute("""
		SELECT firstname, lastname, email, phone FROM Client c
		LEFT JOIN Client_Phone cp ON c.client_id = cp.client_id
		WHERE firstname=%s OR lastname=%s OR email=%s OR phone=%s;
		""", (firstname, lastname, email, phone))
	print(cursor.fetchone()[0])

CreatTable(cur)
AddClient(cur, "Oleg", "Bush", "uhfuiehf@gmail.com")
AddPhone(cur, "364574", 1)
Change_Client(cur, "Oleg", "Push", "dshfihfdl@yandex.ru")
Delete_Phone(cur, "364574", 1)
Find_Client(cur, "Oleg", "Gush","dhgffhsddghf@gmail.com", "364574")
Delete_Client(cur, 1)

cur.close()
conn.close()