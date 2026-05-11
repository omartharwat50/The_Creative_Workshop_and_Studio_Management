import pyodbc

class DatabaseManager:

    def __init__(self):
        self.conn = None
        self.cursor = None
    def connect(self):
        #connection setup
        self.conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=localhost\\SQLEXPRESS04;' 
                'DATABASE=Mydatabase;'
                'Trusted_Connection=yes;'
            )
        self.cursor = self.conn.cursor()
    def disconnect(self):
        self.conn.close()

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)  # params makes it safe
            self.conn.commit()
            return True  # success signal

        except Exception as e:
            self.conn.rollback()  # undo if something went wrong
            print(f"Query failed: {e}")
            return False

    def fetch(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def getAll(self):
        return self.fetch("SELECT * FROM customers")