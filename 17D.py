import sqlite3

con = sqlite3.connect('infoDB')
cur = con.cursor()

cur.execute("SELECT * FROM employees")
records = cur.fetchall()

new_data = {"name": "mmd", "code": 14131, "job": "Data manager"}
new_data = tuple(new_data.values())

def save(data):
    command = f"INSERT INTO employees(name, code, job) VALUES {data};"
    cur.execute(command)

users = [i[1:] for i in records]

if new_data in users:
    print("User already exists")
else:
    save(new_data)
    print("User has been added")

print(f"{len(records)} users exist in the database")

con.commit()
con.close()
print('Done')