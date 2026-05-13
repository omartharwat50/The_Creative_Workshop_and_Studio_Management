import tkinter as tk
from tkinter import ttk, messagebox
from controller import Controller

# ─── Palette ──────────────────────────────────────────────────────────────────
BG        = "#1e1e2e"
PANEL     = "#2a2a3e"
ACCENT    = "#7c5cbf"
ACCENT2   = "#5b8dee"
TEXT      = "#e0e0f0"
MUTED     = "#888aaa"
ENTRY_BG  = "#12121f"
ROW_ODD   = "#252535"
ROW_EVEN  = "#1e1e2e"
SEL       = "#4a3a7a"
BTN_DEL   = "#b04060"
BTN_OK    = "#3a7a50"

FONT      = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_H    = ("Segoe UI", 13, "bold")

ctrl = Controller()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def styled_frame(parent, **kw):
    return tk.Frame(parent, bg=PANEL, **kw)

def styled_label(parent, text, font=FONT, fg=TEXT, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=PANEL, **kw)

def styled_entry(parent, width=22):
    e = tk.Entry(parent, font=FONT, bg=ENTRY_BG, fg=TEXT,
                 insertbackground=TEXT, relief="flat", bd=4, width=width)
    return e

def accent_btn(parent, text, cmd, color=ACCENT, width=14):
    return tk.Button(parent, text=text, command=cmd,
                     font=FONT_BOLD, fg="white", bg=color,
                     activebackground=color, activeforeground="white",
                     relief="flat", bd=0, padx=10, pady=5, width=width,
                     cursor="hand2")

def make_tree(parent, columns, heights=18):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=ROW_ODD, foreground=TEXT,
                    fieldbackground=ROW_ODD, rowheight=heights,
                    font=FONT, borderwidth=0)
    style.configure("Custom.Treeview.Heading",
                    background=ACCENT, foreground="white",
                    font=FONT_BOLD, relief="flat")
    style.map("Custom.Treeview",
              background=[("selected", SEL)],
              foreground=[("selected", TEXT)])

    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True, padx=8, pady=8)

    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")

    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        yscrollcommand=vsb.set, xscrollcommand=hsb.set,
                        style="Custom.Treeview")
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    col_w = max(80, 700 // len(columns))
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=col_w, minwidth=60, anchor="w")

    tree.tag_configure("odd",  background=ROW_ODD)
    tree.tag_configure("even", background=ROW_EVEN)

    vsb.pack(side="right",  fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)
    return tree

def fill_tree(tree, rows):
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tag = "even" if i % 2 == 0 else "odd"
        tree.insert("", "end", values=[str(v) for v in row], tags=(tag,))

def get_sel_id(tree):
    """Return first value (ID) of selected row, or None."""
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Select", "Please select a row first.")
        return None
    return tree.item(sel[0])["values"][0]

def section_header(parent, text):
    tk.Label(parent, text=text, font=FONT_H, fg=ACCENT2,
             bg=BG, anchor="w").pack(fill="x", padx=12, pady=(12, 4))
    tk.Frame(parent, bg=ACCENT, height=2).pack(fill="x", padx=12)

# ─── Root window ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Creative Workshop & Studio — Management System")
root.geometry("1100x720")
root.configure(bg=BG)
root.resizable(True, True)

# ─── Notebook ─────────────────────────────────────────────────────────────────
nb_style = ttk.Style()
nb_style.theme_use("clam")
nb_style.configure("TNotebook",        background=BG,    borderwidth=0)
nb_style.configure("TNotebook.Tab",    background=PANEL, foreground=MUTED,
                   font=FONT_BOLD,     padding=[14, 6])
nb_style.map("TNotebook.Tab",
             background=[("selected", ACCENT)],
             foreground=[("selected", "white")])

notebook = ttk.Notebook(root, style="TNotebook")
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — MEMBERS
# ══════════════════════════════════════════════════════════════════════════════
tab_members = tk.Frame(notebook, bg=BG)
notebook.add(tab_members, text="👥  Members")

section_header(tab_members, "Members")

member_tree = make_tree(tab_members, ["ID", "Name", "Email", "Subscription"])

def refresh_members():
    fill_tree(member_tree, ctrl.get_members())

# — Form ——
mf = styled_frame(tab_members)
mf.pack(fill="x", padx=10, pady=6)

styled_label(mf, "Name").grid(row=0, column=0, padx=6, pady=4, sticky="w")
e_m_name = styled_entry(mf)
e_m_name.grid(row=0, column=1, padx=6, pady=4)

styled_label(mf, "Email").grid(row=0, column=2, padx=6, pady=4, sticky="w")
e_m_email = styled_entry(mf)
e_m_email.grid(row=0, column=3, padx=6, pady=4)

styled_label(mf, "Subscription").grid(row=0, column=4, padx=6, pady=4, sticky="w")
cb_m_sub = ttk.Combobox(mf, values=["Basic", "Premium"], font=FONT, width=10, state="readonly")
cb_m_sub.set("Basic")
cb_m_sub.grid(row=0, column=5, padx=6, pady=4)

def add_member():
    n, em, s = e_m_name.get().strip(), e_m_email.get().strip(), cb_m_sub.get()
    if not n or not em:
        messagebox.showwarning("Input", "Name and Email are required.")
        return
    if ctrl.add_member(n, em, s):
        refresh_members()
        e_m_name.delete(0, "end"); e_m_email.delete(0, "end")
    else:
        messagebox.showerror("Error", "Could not add member.")

def delete_member():
    mid = get_sel_id(member_tree)
    if mid and messagebox.askyesno("Delete", f"Delete member #{mid}?"):
        ctrl.delete_member(mid); refresh_members()

bf = styled_frame(tab_members)
bf.pack(fill="x", padx=10, pady=2)
accent_btn(bf, "➕ Add Member",    add_member,    BTN_OK).pack(side="left", padx=4)
accent_btn(bf, "🗑 Delete Member", delete_member, BTN_DEL).pack(side="left", padx=4)
accent_btn(bf, "🔄 Refresh",       refresh_members).pack(side="left", padx=4)

refresh_members()

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — WORKSHOPS
# ══════════════════════════════════════════════════════════════════════════════
tab_workshops = tk.Frame(notebook, bg=BG)
notebook.add(tab_workshops, text="🎨  Workshops")

section_header(tab_workshops, "Workshops")
ws_tree = make_tree(tab_workshops, ["ID", "Title", "Date", "Craft", "Artist", "Studio"])

def refresh_workshops():
    fill_tree(ws_tree, ctrl.get_workshops())

# — Form ——
wf = styled_frame(tab_workshops)
wf.pack(fill="x", padx=10, pady=6)

styled_label(wf, "Title").grid(row=0, column=0, padx=5, pady=4, sticky="w")
e_ws_title = styled_entry(wf, 18)
e_ws_title.grid(row=0, column=1, padx=5)

styled_label(wf, "Date (YYYY-MM-DD)").grid(row=0, column=2, padx=5, sticky="w")
e_ws_date = styled_entry(wf, 13)
e_ws_date.grid(row=0, column=3, padx=5)

styled_label(wf, "Craft").grid(row=0, column=4, padx=5, sticky="w")
e_ws_craft = styled_entry(wf, 14)
e_ws_craft.grid(row=0, column=5, padx=5)

styled_label(wf, "Artist").grid(row=1, column=0, padx=5, pady=4, sticky="w")
cb_ws_artist = ttk.Combobox(wf, font=FONT, width=16, state="readonly")
cb_ws_artist.grid(row=1, column=1, padx=5)

styled_label(wf, "Studio").grid(row=1, column=2, padx=5, sticky="w")
cb_ws_studio = ttk.Combobox(wf, font=FONT, width=16, state="readonly")
cb_ws_studio.grid(row=1, column=3, padx=5)

_artists, _studios = {}, {}

def load_ws_dropdowns():
    global _artists, _studios
    artists = ctrl.get_workshop_artists()
    studios = ctrl.get_workshop_studios()
    _artists = {name: aid for aid, name in artists}
    _studios = {name: sid for sid, name in studios}
    cb_ws_artist["values"] = list(_artists.keys())
    cb_ws_studio["values"] = list(_studios.keys())
    if _artists: cb_ws_artist.current(0)
    if _studios: cb_ws_studio.current(0)

def add_workshop():
    t, d, c = e_ws_title.get().strip(), e_ws_date.get().strip(), e_ws_craft.get().strip()
    an, sn  = cb_ws_artist.get(), cb_ws_studio.get()
    if not all([t, d, c, an, sn]):
        messagebox.showwarning("Input", "All fields are required."); return
    if ctrl.add_workshop(t, d, c, _artists[an], _studios[sn]):
        refresh_workshops()
        for e in (e_ws_title, e_ws_date, e_ws_craft): e.delete(0, "end")
    else:
        messagebox.showerror("Error", "Could not add workshop.")

def delete_workshop():
    wid = get_sel_id(ws_tree)
    if wid and messagebox.askyesno("Delete", f"Delete workshop #{wid}?"):
        ctrl.delete_workshop(wid); refresh_workshops()

wbf = styled_frame(tab_workshops)
wbf.pack(fill="x", padx=10, pady=2)
accent_btn(wbf, "➕ Add Workshop",    add_workshop,    BTN_OK).pack(side="left", padx=4)
accent_btn(wbf, "🗑 Delete Workshop", delete_workshop, BTN_DEL).pack(side="left", padx=4)
accent_btn(wbf, "🔄 Refresh",         refresh_workshops).pack(side="left", padx=4)

# — Registrations sub-section ——
section_header(tab_workshops, "Registrations")
reg_tree = make_tree(tab_workshops, ["RegID", "Member", "Workshop"])

def refresh_regs():
    fill_tree(reg_tree, ctrl.get_registrations())

rf = styled_frame(tab_workshops)
rf.pack(fill="x", padx=10, pady=4)

styled_label(rf, "Member ID").grid(row=0, column=0, padx=5)
e_reg_mid = styled_entry(rf, 8)
e_reg_mid.grid(row=0, column=1, padx=5)

styled_label(rf, "Workshop ID").grid(row=0, column=2, padx=5)
e_reg_wid = styled_entry(rf, 8)
e_reg_wid.grid(row=0, column=3, padx=5)

def register():
    mid, wid = e_reg_mid.get().strip(), e_reg_wid.get().strip()
    if not mid or not wid:
        messagebox.showwarning("Input", "Both IDs required."); return
    if ctrl.register_member(int(mid), int(wid)):
        refresh_regs(); e_reg_mid.delete(0,"end"); e_reg_wid.delete(0,"end")
    else:
        messagebox.showerror("Error", "Registration failed.")

def unregister():
    rid = get_sel_id(reg_tree)
    if rid and messagebox.askyesno("Remove", f"Remove registration #{rid}?"):
        ctrl.unregister(rid); refresh_regs()

rbf = styled_frame(tab_workshops)
rbf.pack(fill="x", padx=10, pady=2)
accent_btn(rbf, "➕ Register",   register,   BTN_OK).pack(side="left", padx=4)
accent_btn(rbf, "🗑 Unregister", unregister, BTN_DEL).pack(side="left", padx=4)
accent_btn(rbf, "🔄 Refresh",    refresh_regs).pack(side="left", padx=4)

load_ws_dropdowns()
refresh_workshops()
refresh_regs()

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — TOOLS & RENTALS
# ══════════════════════════════════════════════════════════════════════════════
tab_tools = tk.Frame(notebook, bg=BG)
notebook.add(tab_tools, text="🔧  Tools")

section_header(tab_tools, "Tools")
tool_tree = make_tree(tab_tools, ["ID", "Tool Name", "Condition"])

def refresh_tools():
    fill_tree(tool_tree, ctrl.get_tools())

tf = styled_frame(tab_tools)
tf.pack(fill="x", padx=10, pady=6)

styled_label(tf, "Tool Name").grid(row=0, column=0, padx=5)
e_t_name = styled_entry(tf)
e_t_name.grid(row=0, column=1, padx=5)

styled_label(tf, "Condition").grid(row=0, column=2, padx=5)
cb_t_cond = ttk.Combobox(tf, values=["Excellent", "Good", "Needs Maintenance"],
                          font=FONT, width=16, state="readonly")
cb_t_cond.set("Good")
cb_t_cond.grid(row=0, column=3, padx=5)

styled_label(tf, "New Condition (update sel.)").grid(row=0, column=4, padx=5)
cb_t_newcond = ttk.Combobox(tf, values=["Excellent", "Good", "Needs Maintenance"],
                              font=FONT, width=16, state="readonly")
cb_t_newcond.set("Good")
cb_t_newcond.grid(row=0, column=5, padx=5)

def add_tool():
    n, c = e_t_name.get().strip(), cb_t_cond.get()
    if not n:
        messagebox.showwarning("Input", "Tool name required."); return
    if ctrl.add_tool(n, c):
        refresh_tools(); e_t_name.delete(0,"end")
    else:
        messagebox.showerror("Error", "Could not add tool.")

def delete_tool():
    tid = get_sel_id(tool_tree)
    if tid and messagebox.askyesno("Delete", f"Delete tool #{tid}?"):
        ctrl.delete_tool(tid); refresh_tools()

def update_condition():
    tid = get_sel_id(tool_tree)
    if tid:
        ctrl.update_tool_condition(tid, cb_t_newcond.get()); refresh_tools()

tbf = styled_frame(tab_tools)
tbf.pack(fill="x", padx=10, pady=2)
accent_btn(tbf, "➕ Add Tool",         add_tool,         BTN_OK).pack(side="left", padx=4)
accent_btn(tbf, "🗑 Delete Tool",      delete_tool,      BTN_DEL).pack(side="left", padx=4)
accent_btn(tbf, "✏ Update Condition",  update_condition, ACCENT2).pack(side="left", padx=4)
accent_btn(tbf, "🔄 Refresh",          refresh_tools).pack(side="left", padx=4)

# — Rentals ——
section_header(tab_tools, "Rentals")
rental_tree = make_tree(tab_tools, ["RentalID", "Member", "Tool", "Pickup", "Status"])

def refresh_rentals():
    fill_tree(rental_tree, ctrl.get_rentals())

rnf = styled_frame(tab_tools)
rnf.pack(fill="x", padx=10, pady=4)

styled_label(rnf, "Member ID").grid(row=0, column=0, padx=5)
e_rn_mid = styled_entry(rnf, 8)
e_rn_mid.grid(row=0, column=1, padx=5)

styled_label(rnf, "Tool ID").grid(row=0, column=2, padx=5)
e_rn_tid = styled_entry(rnf, 8)
e_rn_tid.grid(row=0, column=3, padx=5)

styled_label(rnf, "Update Status").grid(row=0, column=4, padx=5)
cb_rn_status = ttk.Combobox(rnf, values=["Pending", "Returned", "Overdue"],
                              font=FONT, width=12, state="readonly")
cb_rn_status.set("Pending")
cb_rn_status.grid(row=0, column=5, padx=5)

def add_rental():
    mid, tid = e_rn_mid.get().strip(), e_rn_tid.get().strip()
    if not mid or not tid:
        messagebox.showwarning("Input", "Both IDs required."); return
    if ctrl.add_rental(int(mid), int(tid)):
        refresh_rentals(); e_rn_mid.delete(0,"end"); e_rn_tid.delete(0,"end")
    else:
        messagebox.showerror("Error", "Rental failed.")

def update_rental():
    rid = get_sel_id(rental_tree)
    if rid:
        ctrl.update_rental_status(rid, cb_rn_status.get()); refresh_rentals()

def delete_rental():
    rid = get_sel_id(rental_tree)
    if rid and messagebox.askyesno("Delete", f"Delete rental #{rid}?"):
        ctrl.delete_rental(rid); refresh_rentals()

rnbf = styled_frame(tab_tools)
rnbf.pack(fill="x", padx=10, pady=2)
accent_btn(rnbf, "➕ Rent Tool",       add_rental,    BTN_OK).pack(side="left", padx=4)
accent_btn(rnbf, "✏ Update Status",   update_rental, ACCENT2).pack(side="left", padx=4)
accent_btn(rnbf, "🗑 Delete Rental",   delete_rental, BTN_DEL).pack(side="left", padx=4)
accent_btn(rnbf, "🔄 Refresh",         refresh_rentals).pack(side="left", padx=4)

refresh_tools()
refresh_rentals()

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — INVENTORY (Materials)
# ══════════════════════════════════════════════════════════════════════════════
tab_inv = tk.Frame(notebook, bg=BG)
notebook.add(tab_inv, text="📦  Inventory")

section_header(tab_inv, "Materials Inventory")
inv_tree = make_tree(tab_inv, ["ID", "Material", "Qty Available"])

def refresh_inv():
    fill_tree(inv_tree, ctrl.get_inventory())

inf = styled_frame(tab_inv)
inf.pack(fill="x", padx=10, pady=6)

styled_label(inf, "Material Name").grid(row=0, column=0, padx=5)
e_inv_name = styled_entry(inf)
e_inv_name.grid(row=0, column=1, padx=5)

styled_label(inf, "Quantity").grid(row=0, column=2, padx=5)
e_inv_qty = styled_entry(inf, 8)
e_inv_qty.grid(row=0, column=3, padx=5)

styled_label(inf, "New Qty (update sel.)").grid(row=0, column=4, padx=5)
e_inv_newqty = styled_entry(inf, 8)
e_inv_newqty.grid(row=0, column=5, padx=5)

def add_material():
    n, q = e_inv_name.get().strip(), e_inv_qty.get().strip()
    if not n or not q:
        messagebox.showwarning("Input", "Name and quantity required."); return
    if ctrl.add_material(n, int(q)):
        refresh_inv(); e_inv_name.delete(0,"end"); e_inv_qty.delete(0,"end")
    else:
        messagebox.showerror("Error", "Could not add material.")

def delete_material():
    mid = get_sel_id(inv_tree)
    if mid and messagebox.askyesno("Delete", f"Delete material #{mid}?"):
        ctrl.delete_material(mid); refresh_inv()

def update_qty():
    mid = get_sel_id(inv_tree)
    nq  = e_inv_newqty.get().strip()
    if mid and nq:
        ctrl.update_material_qty(mid, int(nq))
        refresh_inv(); e_inv_newqty.delete(0,"end")

inbf = styled_frame(tab_inv)
inbf.pack(fill="x", padx=10, pady=2)
accent_btn(inbf, "➕ Add Material",    add_material,   BTN_OK).pack(side="left", padx=4)
accent_btn(inbf, "✏ Update Qty",      update_qty,     ACCENT2).pack(side="left", padx=4)
accent_btn(inbf, "🗑 Delete Material", delete_material, BTN_DEL).pack(side="left", padx=4)
accent_btn(inbf, "🔄 Refresh",         refresh_inv).pack(side="left", padx=4)

refresh_inv()

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — STUDIOS
# ══════════════════════════════════════════════════════════════════════════════
tab_studios = tk.Frame(notebook, bg=BG)
notebook.add(tab_studios, text="🏛  Studios")

section_header(tab_studios, "Studios")
studio_tree = make_tree(tab_studios, ["ID", "Studio Name", "Capacity"])

def refresh_studios():
    fill_tree(studio_tree, ctrl.get_studios())

sf = styled_frame(tab_studios)
sf.pack(fill="x", padx=10, pady=6)

styled_label(sf, "Studio Name").grid(row=0, column=0, padx=5)
e_s_name = styled_entry(sf)
e_s_name.grid(row=0, column=1, padx=5)

styled_label(sf, "Capacity").grid(row=0, column=2, padx=5)
e_s_cap = styled_entry(sf, 8)
e_s_cap.grid(row=0, column=3, padx=5)

def add_studio():
    n, c = e_s_name.get().strip(), e_s_cap.get().strip()
    if not n or not c:
        messagebox.showwarning("Input", "Name and capacity required."); return
    if ctrl.add_studio(n, c):
        refresh_studios(); e_s_name.delete(0,"end"); e_s_cap.delete(0,"end")
    else:
        messagebox.showerror("Error", "Could not add studio.")

def delete_studio():
    sid = get_sel_id(studio_tree)
    if sid and messagebox.askyesno("Delete", f"Delete studio #{sid}?"):
        ctrl.delete_studio(sid); refresh_studios()

sbf = styled_frame(tab_studios)
sbf.pack(fill="x", padx=10, pady=2)
accent_btn(sbf, "➕ Add Studio",    add_studio,    BTN_OK).pack(side="left", padx=4)
accent_btn(sbf, "🗑 Delete Studio", delete_studio, BTN_DEL).pack(side="left", padx=4)
accent_btn(sbf, "🔄 Refresh",       refresh_studios).pack(side="left", padx=4)

refresh_studios()

# ─── Run ──────────────────────────────────────────────────────────────────────
root.mainloop()