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
                'DATABASE=DataBasePh3;'
                'Trusted_Connection=yes;'
            )
        self.cursor = self.conn.cursor()
    def disconnect(self):
        self.conn.close()



    """Automatically connects, fetches data, and cleans up."""
    def query_fetch(self, sql, params=()):
            self.connect()
            try:
                self.cursor.execute(sql, params)
                return self.cursor.fetchall()
            finally:
                self.disconnect()



    """Automatically connects, saves changes, and cleans up."""
    def query_execute(self, sql, params=()):
            self.connect()
            try:
                self.cursor.execute(sql, params)
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Error: {e}")
                self.conn.rollback()
                return False
            finally:
                self.disconnect()

  