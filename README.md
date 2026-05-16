# 🎨 Arts Center Workshop & Studio Management System

A full-stack desktop management application built for an arts center that runs creative workshops, rents tools to members, and manages studios and materials inventory.

Built with **Python**, **Tkinter**, and **SQL Server**.

---

## 📸 Features

- 👥 **Members** — Add, view, and delete member subscriptions (Basic / Premium)
- 🎨 **Workshops** — Manage sessions with assigned artists and studios; handle member registrations
- 🔧 **Tools & Rentals** — Track tool inventory and member borrowing with return status
- 📦 **Inventory** — Manage raw materials and quantities used in workshops
- 🏛 **Studios** — Manage physical studio spaces and their capacities

---

## 🏗 Architecture

The app follows a clean 3-layer MVC architecture:

```
GUI.py  →  controller.py  →  models/*.py  →  DatabaseManager.py  →  SQL Server
```

| Layer | File | Role |
|---|---|---|
| View | `GUI.py` | Tabbed dark-themed GUI built with Tkinter |
| Controller | `controller.py` | Routes GUI actions to the correct model |
| Models | `models/*.py` | Business logic and SQL queries per entity |
| DB Access | `DatabaseManager.py` | Manages connections, queries, and transactions |

---

## 🗄 Database Schema

The database (`ArtsCenter`) contains **9 relational tables**:

```
Member                 — center subscribers
Studio                 — physical rooms
Artist                 — workshop instructors
Workshop               — sessions linking Artist + Studio
Material               — raw supplies (clay, ink, etc.)
Tool                   — borrowable equipment
Rental                 — Member ↔ Tool bookings
WorkshopRegistration   — Member ↔ Workshop signups
WorkshopMaterial       — Workshop ↔ Material usage tracking
```

---

## 🛠 Tech Stack

| Technology | Usage |
|---|---|
| Python 3 | Core language |
| Tkinter | Desktop GUI |
| pyodbc | SQL Server connectivity |
| SQL Server (Express) | Relational database |
| T-SQL | All queries written manually (no ORM) |

---

## 📁 Project Structure

```
│
├── GUI.py                    # Main application window (5 tabs)
├── controller.py             # Central controller
├── DatabaseManager.py        # DB connection, query_fetch, query_execute
│
└── models/
    ├── MemberManager.py
    ├── WorkshopManager.py
    ├── ToolManager.py
    ├── InventoryManager.py
    └── StudioManager.py
```

---

## ⚙️ Setup & Run

### 1. Prerequisites

- Python 3.8+
- SQL Server Express (or any SQL Server instance)
- `pyodbc` library

```bash
pip install pyodbc
```

### 2. Database Setup

Run the provided SQL script to create and populate the database:

```
SQLQuery2.sql
```

Open it in SQL Server Management Studio (SSMS) and execute it. This will create the `ArtsCenter` database with all tables and sample data.

### 3. Configure the Connection

In `DatabaseManager.py`, update the connection string to match your setup:

```python
self.conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\YOUR_INSTANCE;'   # ← change this
    'DATABASE=ArtsCenter;'
    'Trusted_Connection=yes;'
)
```

### 4. Run the App

```bash
python GUI.py
```

---

## 🔒 Technical Highlights

- All SQL queries use **parameterized `?` placeholders** — no SQL injection risk
- Write operations use **commit / rollback** transactions for data integrity
- Deletes handle **foreign key constraints** by removing child records first
- Database connection is **opened and closed per query** to avoid stale connections
- Dropdowns (artists, studios, conditions) are **loaded live from the database**

---

## 👤 Author

Made by **[Your Name]**  
📧 [your@email.com]  
🔗 [linkedin.com/in/yourprofile]
