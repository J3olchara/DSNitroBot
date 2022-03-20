import psycopg2 as ps
import os
def startdb_admins():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode = 'require')
    cur = base.cursor()
    if base:
        print("-------------------------------ADMINS DATABASE CONNECTED-------------------------------")
    cur.execute("CREATE TABLE IF NOT EXISTS admins(username TEXT, telegramID INTEGER PRIMARY KEY)")
    base.commit()
async def insert_admin(username, ID):
    return cur.execute("INSERT INTO admins(username, telegramID) VALUES(%s, %s)", (username, ID))
async def take_admins_id():
    cur.execute("SELECT telegramID FROM admins")
    admins = cur.fetchall()
    adminlist = [admin[0] for admin in admins]
    base.commit()
    return adminlist

async def SafeShutdown_admins():
    base.commit()
    print("-------------------------------ADMIN DB SAVED-------------------------------")