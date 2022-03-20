import psycopg2 as ps
import os
from datetime import datetime

def startdb_products():
    global base, cur 
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode = 'require')
    cur = base.cursor()
    if base:
        print("-------------------------------PRODUCTS DATABASE CONNECTED-------------------------------")
    cur.execute("CREATE TABLE IF NOT EXISTS ProductsList(supplier TEXT, supplydate TEXT, ProductKey TEXT PRIMARY KEY, ProductType TEXT,\
    BuyerID TEXT, BuyerUsername TEXT, BuyingDate TEXT)")
    base.commit()

async def InsertProducts(supplier, Product, ProductType):
    DuplicatedKeys = []
    try:
        cur.execute("INSERT INTO ProductsList VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (str(supplier), str(datetime.now()), str(Product), str(ProductType), "null", "null", "null"))
    except:
        DuplicatedKeys.append(str(Product))
    base.commit()
    return
async def TakeProductsList(ProductType):
    try:
        cur.execute("SELECT ProductKey FROM ProductsList WHERE BuyingDate = 'null' AND ProductType = %s", (ProductType,))
        products = cur.fetchall()
        products = [product[0] for product in products]
        return products 
    except:
        return []
async def AllProductList(ProductType):
    cur.execute("SELECT ProductKey from ProductsList WHERE ProductType = %s", (ProductType,))
    AllProducts = cur.fetchall()
    AllProducts = [product[0] for product in AllProducts]
    return AllProducts
async def buying_product(ID, username, ProductType):
    cur.execute("SELECT ProductKey FROM ProductsList WHERE BuyingDate = %s AND ProductType = %s", ('null', ProductType))
    ProductKey = cur.fetchone()[0]
    cur.execute("UPDATE ProductsList SET BuyerID = %s WHERE ProductKey = %s", (ID, ProductKey))
    cur.execute("UPDATE ProductsList SET BuyerUsername = %s WHERE ProductKey = %s", (f"@{username}", ProductKey))
    cur.execute("UPDATE ProductsList SET BuyingDate = %s WHERE ProductKey = %s", (datetime.now(), ProductKey))
    base.commit()
    return ProductKey
async def SafeShutdown_products():
    base.commit()
    print("-------------------------------PRODUCT DB SAVED-------------------------------")