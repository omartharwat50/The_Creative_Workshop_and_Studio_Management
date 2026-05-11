from controller import Controller
import tkinter as tk

# 1. Setup the Controller
my_controller = Controller()

# 2. Setup the Window
root = tk.Tk()
root.title("The Creative Workshop & Studio Management")
root.geometry("1200x800")


# 3. Define the Action (The "Callback")
def on_button_click():

    names = my_controller.get_customer_list()

    for name in names:
        label = tk.Label(root, text=name)
        label.pack()


# 4. Create the Button
# We link the command to our function name
btn = tk.Button(root, text="Show Users", command=on_button_click)
btn.pack(pady=20)

root.mainloop()