from DatabaseManager import DatabaseManager

class ToolManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        """Returns all tools: (ToolID, ToolName, ToolCondition)"""
        return self.db.query_fetch("SELECT ToolID, ToolName, ToolCondition FROM Tool")

    def add(self, tool_name, condition):
        sql = "INSERT INTO Tool (ToolName, ToolCondition) VALUES (?, ?)"
        return self.db.query_execute(sql, (tool_name, condition))

    def delete(self, tool_id):
        self.db.query_execute("DELETE FROM Rental WHERE ToolID = ?", (tool_id,))
        return self.db.query_execute("DELETE FROM Tool WHERE ToolID = ?", (tool_id,))

    def update_condition(self, tool_id, condition):
        sql = "UPDATE Tool SET ToolCondition = ? WHERE ToolID = ?"
        return self.db.query_execute(sql, (condition, tool_id))

    # ── Rentals ────────────────────────────────────────────────────────────────
    def get_rentals(self):
        sql = """
            SELECT r.RentalID,
                   m.Name     AS Member,
                   t.ToolName AS Tool,
                   r.PickupTime,
                   r.ReturnStatus
            FROM Rental r
            JOIN Member m ON r.MemberID = m.MemberID
            JOIN Tool   t ON r.ToolID   = t.ToolID
        """
        return self.db.query_fetch(sql)

    def add_rental(self, member_id, tool_id, return_status="Pending"):
        sql = """INSERT INTO Rental (MemberID, ToolID, PickupTime, ReturnStatus)
                 VALUES (?, ?, GETDATE(), ?)"""
        return self.db.query_execute(sql, (member_id, tool_id, return_status))

    def update_rental_status(self, rental_id, status):
        sql = "UPDATE Rental SET ReturnStatus = ? WHERE RentalID = ?"
        return self.db.query_execute(sql, (status, rental_id))

    def delete_rental(self, rental_id):
        return self.db.query_execute(
            "DELETE FROM Rental WHERE RentalID = ?", (rental_id,))