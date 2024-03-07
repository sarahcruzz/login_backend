from mysql import connector

def conectar():
    return connector.connect(
        host='localhost',
        user='root',
        password='SENAI',
        database = 'pwbe_escola'
    )