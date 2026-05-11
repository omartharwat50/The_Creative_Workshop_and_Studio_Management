from DatabaseManager import DatabaseManager
from models.MemberManager import MemberManager
from models.WorkshopManager import Workshop
from models.ToolManager import ToolManager
from models.InventoryManager import InventoryManager
from models.StudioManager import StudioManager


class Controller:
    def __init__(self):

        self.member_mgr = MemberManager()



    def get_customer_list(self):
        raw_data = self.member_mgr.get_customers()

        clean_names = [row[0] for row in raw_data]
        return clean_names


