import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",          
        user="admin_nodo",               
        password="1234",  
        database="nodo"
    )
