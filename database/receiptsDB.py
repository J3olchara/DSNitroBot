import psycopg2 as ps
import os
from datetime import datetime
def startdb_receipts():
	global cur, base
	base = ps.connect(os.environ.get('DATABASE_URL'), sslmode = 'require')
	cur = base.cursor()
	if base:
		print("-------------------------------RECEIPTS DATABASE CONNECTED-------------------------------")
	cur.execute("CREATE TABLE IF NOT EXISTS receipts(paymentID INTEGER PRIMARY KEY, telegramID INTEGER, username TEXT, moneyamount INTEGER, bill_id TEXT, billdate TEXT)")
	base.commit()
async def SafeShutdown_receipts():
	base.commit()
	print("-------------------------------RECEIPTS DB SAVED-------------------------------")
async def TakeNewPaymentID():
	cur.execute("SELECT * FROM receipts ORDER BY paymentID DESC LIMIT 1")
	LastPaymentID = cur.fetchone()[0]
	base.commit()
	if LastPaymentID == None:
		NewPaymentID = 0
	else: 
		NewPaymentID = LastPaymentID + 1
	return NewPaymentID
async def InsertingBillInformation(NewPaymentID, ID, username, amount, bill_id):
	cur.execute("INSERT INTO receipts VALUES(%s, %s, %s, %s, %s, %s)", (NewPaymentID, ID, username, amount, bill_id, datetime.now()))
	base.commit()