from DatabaseManager import DatabaseManager

class MemberManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        """Returns all members: (MemberID, Name, Email, SubscriptionType)"""
        return self.db.query_fetch("SELECT MemberID, Name, Email, SubscriptionType FROM Member")

    # kept for backward-compat with controller.py
    def get_customers(self):
        return self.db.query_fetch("SELECT Name FROM Member")

    def add(self, name, email, subscription_type):
        sql = "INSERT INTO Member (Name, Email, SubscriptionType) VALUES (?, ?, ?)"
        return self.db.query_execute(sql, (name, email, subscription_type))

    def delete(self, member_id):
        sql = "DELETE FROM Member WHERE MemberID = ?"
        return self.db.query_execute(sql, (member_id,))

    def update(self, member_id, name, email, subscription_type):
        sql = """UPDATE Member
                 SET Name = ?, Email = ?, SubscriptionType = ?
                 WHERE MemberID = ?"""
        return self.db.query_execute(sql, (name, email, subscription_type, member_id))