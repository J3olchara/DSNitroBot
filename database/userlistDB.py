import psycopg2 as ps
import os

def startdb_users():
	global base, cur
	base = ps.connect(os.environ.get('DATABASE_URL'), sslmode = 'require')
	cur = base.cursor()
	if base:
		print("-------------------------------USERS DATABASE CONNECTED-------------------------------")
	cur.execute("CREATE TABLE IF NOT EXISTS userlist(username TEXT, telegramID TEXT PRIMARY KEY, balance INTEGER, discount TEXT)")
	base.commit()
async def SafeShutdown_users():
	base.commit()
	print("-------------------------------USERS DB SAVED-------------------------------")


async def get_users_id():
	cur.execute("SELECT telegramID FROM userlist")
	userlist = cur.fetchall()
	userlist = [userid[0] for userid in userlist]
	base.commit()
	return userlist
async def InsertNewUser(username, ID):
	username = str(username)
	ID = str(ID)
	cur.execute("INSERT INTO userlist(username, telegramID, balance, discount) VALUES (%s, %s, %s, %s)", (username, ID, 0, str(1.00)))
	base.commit()
async def ProfileData(currentuser):
	cur.execute("SELECT * FROM userlist WHERE telegramID = %s", (currentuser,))
	userdata = cur.fetchone()
	base.commit()
	return userdata
async def InsertBalance(currentuser, amount):
	userdata = await ProfileData(currentuser)
	userbalance = userdata[2]
	balance = userbalance
	newbalance = balance + amount
	cur.execute("UPDATE userlist SET balance = %s WHERE telegramID = %s", (newbalance, currentuser))
	base.commit()
async def BuyerBalanceUpdate(ID, cost):
	ID = str(ID)
	cur.execute("SELECT balance FROM userlist WHERE telegramID = %s", (ID,))
	balance = cur.fetchone()[0]
	newbalance = balance - cost
	cur.execute("UPDATE userlist SET balance = %s WHERE telegramID = %s", (newbalance, ID))
	base.commit()

async def BuyerBalanceCheck(ID, cost):
	ID = str(ID)
	cur.execute("SELECT balance FROM userlist WHERE telegramID = %s", (ID,))
	balance = cur.fetchone()[0]
	newbalance = balance - cost
	if newbalance >= 0:
		base.commit()
		return True
	else:
		base.commit()
		return False