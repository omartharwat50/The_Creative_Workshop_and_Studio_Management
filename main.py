from DatabaseManager import DatabaseManager
import tkinter as tk

# 1. Fetch Data First (keep it ready)
DB = DatabaseManager()
DB.connect()
rows = DB.getAll()
DB.disconnect()

# 2. Setup the Window
root = tk.Tk()
root.title("The Creative Workshop & Studio Management")
root.geometry("1200x800")


# 3. Define the Action
def on_button_click():
    # We move the loop INSIDE the function so it runs when clicked
    for row in rows:
        display_text = f"User: {row.first_name}"
        label = tk.Label(root, text=display_text, font=("Arial", 12))
        label.pack(pady=5)

    # Optional: Disable the button after click so you don't duplicate the list
    btn.config(state="disabled", text="Data Loaded")


# 4. Create the Button
btn = tk.Button(root, text="Show Users", command=on_button_click)
btn.pack(pady=20)

root.mainloop()