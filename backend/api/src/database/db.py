import mysql.connector
from config import getconfig_bd
from utils.logger import Logger
import os

class MySQLConnection:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port)
            if self.connection.is_connected():
                pass
                #print('Connected to MySQL database')
        except mysql.connector.Error as e:
            
            print(f"Error connecting to MySQL database: {e}")
            Logger.add_to_log( message_or_error= e)

    def cursor(self, *args, **kwargs):
        return self.connection.cursor(*args, **kwargs)
        
    def commit(self, *args, **kwargs):
        return self.connection.commit(*args, **kwargs)
    def rollback(self, *args, **kwargs):
        return self.connection.rollback(*args, **kwargs)
    
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            #print('Connection to MySQL database closed')

class MySQLConnectionManager:
    _instance = None
    config = getconfig_bd()
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connections = []
        return cls._instance
    def create_connection(self, host=None, database=None, user=None, password=None, port=None):
        if host is None: host = self.config['host']
        if database is None: database = self.config['database']
        if user is None: user = self.config['user']
        if password is None: password = self.config['password']
        if port is None: port = self.config['port']


        if host is None or database is None or user is None or password is None or port is None:
            print('hola este el Enviremot\n', os.environ)
            raise ValueError('No se ha definido la variable de entorno de BD')
        

        connection = MySQLConnection(host, database, user, password, port)
        connection.connect()
        self.connections.append(connection)
        return connection
    def close_connection(self, connection):
        connection.close()
        self.connections.remove(connection)







# Ejemplo de uso:
if __name__ == "__main__":
    manager = MySQLConnectionManager()
    manager2 = MySQLConnectionManager()

    print('esta es el bool de la igualdad',manager is manager2) 

    # Crear una conexión y agregarla a la lista de conexiones
    connection1 = manager.create_connection()
    connection2 = manager.create_connection()
    connection3 = manager.create_connection()
    connection4 = manager.create_connection()

    cursor = connection2.cursor()
    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    print(resultados)

    cursor3 = connection3.cursor()
    sql = "SELECT * FROM usuarios"
    cursor3.execute(sql)
    resultados = cursor3.fetchall()
    print(resultados)


    # Cerrar y eliminar la conexión de la lista
    manager.close_connection(connection1)
    manager.close_connection(connection2)
    manager.close_connection(connection3)
    manager.close_connection(connection4)
