
import psycopg2, csv

# Connect to the database
conn = psycopg2.connect(
    host='localhost',
    dbname='phonebook',
    user='postgres',
    password='kukamerey26',
)
cur = conn.cursor()
def disentry(page):
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    cur.close()
    i = 0
    limit = 10 * page
    for row in rows:
        if i < limit and i >= limit - 10:
            print(row)
        i+=1
    print(f"Page 1 / {len(rows) // 10 + 1}")
    page = input("Enter page or Q for quit: ")
    if page == "Q" or page == "q":
        page = 1000
    if 1 <= int(page) <= len(rows) // 10 + 1:
        disentry(page)

def update(name, number):
    cur.execute("SELECT COUNT(*) FROM phonebook WHERE name = %s", (name,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO phonebook (name, number) VALUES (%s, %s)", (name, number,))
    else:
        cur.execute("UPDATE phonebook SET number = %s WHERE name = %s", (number, name,))
    conn.commit()
    cur.close()

while True:
    print("1 - insert csv, 2 - insert console, 3 - update, 4 - search, 5 - search part, 6 - select, 7 - delete, 8 - exit")
    n = input()
    if n == '1':
        file = input("File name:")
        with open(file+".csv", "r") as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                    cur.execute("""INSERT INTO PhoneBook VALUES(%s,%s) returning *;""", row)
                conn.commit()
    elif n == '2':
        name = input("Enter name: ")
        number = input("Enter phone number: ")
        cur.execute("INSERT INTO phonebook (name, number) VALUES (%s, %s)", (name, number))
        conn.commit()
    elif n == '3':
        name = input("Enter name: ")
        number = input("Enter phone number: ")
        update(name, number)
    elif n == '4':
        name = input("Enter name to search: ")
        cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (name,))
        rows = cur.fetchall()
        for r in rows:
            print(r)
        conn.commit()
    elif n == '5':
        part = input("Enter part to search: ")
        cur.execute(f"SELECT * FROM phonebook WHERE name ILIKE %s OR number ILIKE %s", ('%'+part+'%', '%'+part+'%'))
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            print(row)
        conn.commit()
    elif n == '6':
        disentry(1)
    elif n == '7':  
        part = input("delete name of part or phone:")
        cur.execute("DELETE FROM phonebook WHERE name ILIKE %s OR number ILIKE %s", ('%'+part+'%', '%'+part+'%',))
        conn.commit()
    elif n == '8':
        break
    else:
        print("Please try again, your server is loser")

conn.close()