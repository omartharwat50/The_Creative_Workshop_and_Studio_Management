from DatabaseManager import DatabaseManager

class InventoryManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        """Returns all materials: (MaterialID, MaterialName, QuantityAvailable)"""
        return self.db.query_fetch(
            "SELECT MaterialID, MaterialName, QuantityAvailable FROM Material")

    def add(self, name, quantity):
        sql = "INSERT INTO Material (MaterialName, QuantityAvailable) VALUES (?, ?)"
        return self.db.query_execute(sql, (name, quantity))

    def delete(self, material_id):
        self.db.query_execute(
            "DELETE FROM WorkshopMaterial WHERE MaterialID = ?", (material_id,))
        return self.db.query_execute(
            "DELETE FROM Material WHERE MaterialID = ?", (material_id,))

    def update_quantity(self, material_id, quantity):
        sql = "UPDATE Material SET QuantityAvailable = ? WHERE MaterialID = ?"
        return self.db.query_execute(sql, (quantity, material_id))