from DatabaseManager import DatabaseManager


class MemberManager:

    def __init__(self):
        self.db = DatabaseManager()


    def get_customers(self):
        query = "SELECT first_name FROM customers"

        results = self.db.query_fetch(query)

        return results



