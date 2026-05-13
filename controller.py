from DatabaseManager import DatabaseManager
from models.MemberManager   import MemberManager
from models.WorkshopManager import Workshop
from models.ToolManager     import ToolManager
from models.InventoryManager import InventoryManager
from models.StudioManager   import StudioManager


class Controller:
    def __init__(self):
        self.member_mgr    = MemberManager()
        self.workshop_mgr  = Workshop()
        self.tool_mgr      = ToolManager()
        self.inventory_mgr = InventoryManager()
        self.studio_mgr    = StudioManager()

    # ── Members ────────────────────────────────────────────────────────────────
    def get_customer_list(self):
        """Legacy: returns just names (used by old GUI)."""
        return [row[0] for row in self.member_mgr.get_customers()]

    def get_members(self):
        return self.member_mgr.get_all()          # (ID, Name, Email, Sub)

    def add_member(self, name, email, sub):
        return self.member_mgr.add(name, email, sub)

    def delete_member(self, member_id):
        return self.member_mgr.delete(member_id)

    def update_member(self, member_id, name, email, sub):
        return self.member_mgr.update(member_id, name, email, sub)

    # ── Workshops ──────────────────────────────────────────────────────────────
    def get_workshops(self):
        return self.workshop_mgr.get_all()        # (ID, Title, Date, Craft, Artist, Studio)

    def add_workshop(self, title, date, craft, artist_id, studio_id):
        return self.workshop_mgr.add(title, date, craft, artist_id, studio_id)

    def delete_workshop(self, workshop_id):
        return self.workshop_mgr.delete(workshop_id)

    def get_workshop_artists(self):
        return self.workshop_mgr.get_artists()    # (ArtistID, Name)

    def get_workshop_studios(self):
        return self.workshop_mgr.get_studios()    # (StudioID, Name)

    def get_registrations(self):
        return self.workshop_mgr.get_registrations()

    def register_member(self, member_id, workshop_id):
        return self.workshop_mgr.register_member(member_id, workshop_id)

    def unregister(self, registration_id):
        return self.workshop_mgr.unregister(registration_id)

    # ── Tools ──────────────────────────────────────────────────────────────────
    def get_tools(self):
        return self.tool_mgr.get_all()            # (ID, Name, Condition)

    def add_tool(self, name, condition):
        return self.tool_mgr.add(name, condition)

    def delete_tool(self, tool_id):
        return self.tool_mgr.delete(tool_id)

    def update_tool_condition(self, tool_id, condition):
        return self.tool_mgr.update_condition(tool_id, condition)

    def get_rentals(self):
        return self.tool_mgr.get_rentals()        # (ID, Member, Tool, Pickup, Status)

    def add_rental(self, member_id, tool_id):
        return self.tool_mgr.add_rental(member_id, tool_id)

    def update_rental_status(self, rental_id, status):
        return self.tool_mgr.update_rental_status(rental_id, status)

    def delete_rental(self, rental_id):
        return self.tool_mgr.delete_rental(rental_id)

    # ── Inventory ──────────────────────────────────────────────────────────────
    def get_inventory(self):
        return self.inventory_mgr.get_all()       # (ID, Name, Qty)

    def add_material(self, name, qty):
        return self.inventory_mgr.add(name, qty)

    def delete_material(self, material_id):
        return self.inventory_mgr.delete(material_id)

    def update_material_qty(self, material_id, qty):
        return self.inventory_mgr.update_quantity(material_id, qty)

    # ── Studios ────────────────────────────────────────────────────────────────
    def get_studios(self):
        return self.studio_mgr.get_all()          # (ID, Name, Capacity)

    def add_studio(self, name, capacity):
        return self.studio_mgr.add(name, capacity)

    def delete_studio(self, studio_id):
        return self.studio_mgr.delete(studio_id)

    def update_studio(self, studio_id, name, capacity):
        return self.studio_mgr.update(studio_id, name, capacity)