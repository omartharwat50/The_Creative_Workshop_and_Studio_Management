from DatabaseManager import DatabaseManager

class StudioManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        """Returns all studios: (StudioID, Name, Capacity)"""
        return self.db.query_fetch("SELECT StudioID, Name, Capacity FROM Studio")

    def add(self, name, capacity):
        sql = "INSERT INTO Studio (Name, Capacity) VALUES (?, ?)"
        return self.db.query_execute(sql, (name, int(capacity)))

    def delete(self, studio_id):
        return self.db.query_execute(
            "DELETE FROM Studio WHERE StudioID = ?", (studio_id,))

    def update(self, studio_id, name, capacity):
        sql = "UPDATE Studio SET Name = ?, Capacity = ? WHERE StudioID = ?"
        return self.db.query_execute(sql, (name, int(capacity), studio_id))