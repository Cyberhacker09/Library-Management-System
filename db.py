import mysql.connector
from mysql.connector import Error

# Global connection and cursor
connection = None
cursor = None

def connect_db():
    global connection, cursor
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Password#",# use your own password for mySQL login
            database="#database", # use your own Database you set up for this
            auth_plugin="mysql_native_password"  # ✅ Fix: force plugin
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            print("✅ Database connected successfully!")
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")

def get_cursor():
    """Return cursor for queries"""
    global cursor
    if cursor is None:
        connect_db()
    return cursor

def get_connection():
    """Return connection object for commits"""
    global connection
    if connection is None:
        connect_db()
    return connection

# Automatically connect on import
connect_db()
