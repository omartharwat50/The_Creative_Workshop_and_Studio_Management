from DatabaseManager import DatabaseManager

class Workshop:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        """Returns workshops joined with artist and studio names."""
        sql = """
            SELECT w.WorkshopID, w.Title, w.Date, w.CraftType,
                   a.Name AS Artist, s.Name AS Studio
            FROM Workshop w
            JOIN Artist  a ON w.ArtistID  = a.ArtistID
            JOIN Studio  s ON w.StudioID  = s.StudioID
        """
        return self.db.query_fetch(sql)

    def add(self, title, date, craft_type, artist_id, studio_id):
        sql = """INSERT INTO Workshop (Title, Date, CraftType, ArtistID, StudioID)
                 VALUES (?, ?, ?, ?, ?)"""
        return self.db.query_execute(sql, (title, date, craft_type, artist_id, studio_id))

    def delete(self, workshop_id):
        # remove registrations first (FK constraint)
        self.db.query_execute(
            "DELETE FROM WorkshopRegistration WHERE WorkshopID = ?", (workshop_id,))
        self.db.query_execute(
            "DELETE FROM WorkshopMaterial WHERE WorkshopID = ?", (workshop_id,))
        return self.db.query_execute(
            "DELETE FROM Workshop WHERE WorkshopID = ?", (workshop_id,))

    # ── Registrations ──────────────────────────────────────────────────────────
    def get_registrations(self):
        sql = """
            SELECT wr.RegistrationID,
                   m.Name  AS Member,
                   w.Title AS Workshop
            FROM WorkshopRegistration wr
            JOIN Member   m ON wr.MemberID   = m.MemberID
            JOIN Workshop w ON wr.WorkshopID = w.WorkshopID
        """
        return self.db.query_fetch(sql)

    def register_member(self, member_id, workshop_id):
        sql = """INSERT INTO WorkshopRegistration (MemberID, WorkshopID)
                 VALUES (?, ?)"""
        return self.db.query_execute(sql, (member_id, workshop_id))

    def unregister(self, registration_id):
        return self.db.query_execute(
            "DELETE FROM WorkshopRegistration WHERE RegistrationID = ?",
            (registration_id,))

    # ── Helpers for dropdowns ──────────────────────────────────────────────────
    def get_artists(self):
        return self.db.query_fetch("SELECT ArtistID, Name FROM Artist")

    def get_studios(self):
        return self.db.query_fetch("SELECT StudioID, Name FROM Studio")