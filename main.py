import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import math
import time

# -----------------------------
# Window
# -----------------------------

root = tk.Tk()
root.title("Contact Management System")
root.geometry("1200x700")
root.resizable(False, False)

# -----------------------------
# Colors
# -----------------------------

BG1 = "#240046"
BG2 = "#00C2FF"
CARD = "#1B1B2F"
ENTRY = "#2D2D44"
BTN = "#7B2FF7"
TEXT = "white"

# -----------------------------
# Database
# -----------------------------

FILE = "contacts.json"

contacts = []


def load_contacts():
    global contacts

    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                contacts = json.load(f)
        except:
            contacts = []
    else:
        contacts = []


def save_contacts():
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)


load_contacts()

# -----------------------------
# Background
# -----------------------------

canvas = tk.Canvas(root,
                   width=1200,
                   height=700,
                   highlightthickness=0)

canvas.place(x=0, y=0)


def gradient():

    canvas.delete("gradient")

    r1, g1, b1 = (36, 0, 70)
    r2, g2, b2 = (0, 194, 255)

    for i in range(700):

        r = int(r1 + (r2-r1)*i/700)
        g = int(g1 + (g2-g1)*i/700)
        b = int(b1 + (b2-b1)*i/700)

        color = "#%02x%02x%02x"%(r,g,b)

        canvas.create_line(
            0,
            i,
            1200,
            i,
            fill=color,
            tags="gradient"
        )

gradient()

# -----------------------------
# Floating Particles
# -----------------------------

particles=[]

for i in range(60):

    x=random.randint(0,1200)
    y=random.randint(0,700)
    r=random.randint(2,5)

    item=canvas.create_oval(
        x-r,
        y-r,
        x+r,
        y+r,
        fill="white",
        outline=""
    )

    particles.append([item,x,y,r])


def animate_particles():

    for p in particles:

        p[2]-=1

        if p[2]<0:
            p[2]=700
            p[1]=random.randint(0,1200)

        canvas.coords(
            p[0],
            p[1]-p[3],
            p[2]-p[3],
            p[1]+p[3],
            p[2]+p[3]
        )

    root.after(40,animate_particles)

animate_particles()

# -----------------------------
# Left Frame
# -----------------------------

left = tk.Frame(
    root,
    bg=CARD,
    width=320,
    height=650
)

left.place(x=20,y=20)

title=tk.Label(
    left,
    text="CONTACT\nMANAGER",
    font=("Arial",24,"bold"),
    bg=CARD,
    fg="cyan"
)

title.pack(pady=20)

clock=tk.Label(
    left,
    font=("Arial",16),
    bg=CARD,
    fg="white"
)

clock.pack()


def update_clock():

    clock.config(
        text=time.strftime("%H:%M:%S")
    )

    root.after(
        1000,
        update_clock
    )

update_clock()

style=("Arial",12)

tk.Label(
    left,
    text="Name",
    bg=CARD,
    fg="white",
    font=style
).pack(pady=(20,5))

name_entry=tk.Entry(
    left,
    width=28,
    font=style,
    bg=ENTRY,
    fg="white",
    insertbackground="white"
)

name_entry.pack()

tk.Label(
    left,
    text="Phone",
    bg=CARD,
    fg="white",
    font=style
).pack(pady=(15,5))

phone_entry=tk.Entry(
    left,
    width=28,
    font=style,
    bg=ENTRY,
    fg="white",
    insertbackground="white"
)

phone_entry.pack()

tk.Label(
    left,
    text="Email",
    bg=CARD,
    fg="white",
    font=style
).pack(pady=(15,5))

email_entry=tk.Entry(
    left,
    width=28,
    font=style,
    bg=ENTRY,
    fg="white",
    insertbackground="white"
)

email_entry.pack()

# -----------------------------
# Right Frame
# -----------------------------

right=tk.Frame(
    root,
    bg="#151530",
    width=820,
    height=650
)

right.place(x=360,y=20)

search_var=tk.StringVar()

tk.Label(
    right,
    text="Search Contact",
    bg="#151530",
    fg="cyan",
    font=("Arial",14,"bold")
).pack(pady=10)

search_entry=tk.Entry(
    right,
    textvariable=search_var,
    width=40,
    font=("Arial",12)
)

search_entry.pack()

listbox=tk.Listbox(
    right,
    width=50,
    height=18,
    font=("Arial",12),
    bg="#24243e",
    fg="white",
    selectbackground="#00C2FF"
)

listbox.pack(pady=20)

status=tk.Label(
    right,
    text="Total Contacts : 0",
    bg="#151530",
    fg="white",
    font=("Arial",13)
)

status.pack()
# ===========================================
# FUNCTIONS
# ===========================================

selected_index = None


def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


def refresh_list(data=None):
    listbox.delete(0, tk.END)

    if data is None:
        data = contacts

    for c in data:
        listbox.insert(tk.END, c["name"])

    status.config(text=f"Total Contacts : {len(contacts)}")


refresh_list()


def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or phone == "" or email == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields."
        )
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email
    })

    save_contacts()
    refresh_list()
    clear_entries()

    messagebox.showinfo(
        "Success",
        "Contact Added Successfully."
    )


def load_selected(event):

    global selected_index

    if not listbox.curselection():
        return

    selected_index = listbox.curselection()[0]

    contact = contacts[selected_index]

    clear_entries()

    name_entry.insert(0, contact["name"])
    phone_entry.insert(0, contact["phone"])
    email_entry.insert(0, contact["email"])


listbox.bind("<<ListboxSelect>>", load_selected)


def update_contact():

    global selected_index

    if selected_index is None:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    contacts[selected_index] = {
        "name": name_entry.get(),
        "phone": phone_entry.get(),
        "email": email_entry.get()
    }

    save_contacts()
    refresh_list()

    messagebox.showinfo(
        "Updated",
        "Contact Updated Successfully."
    )


def delete_contact():

    global selected_index

    if selected_index is None:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    answer = messagebox.askyesno(
        "Delete",
        "Delete this contact?"
    )

    if answer:

        contacts.pop(selected_index)

        selected_index = None

        save_contacts()

        refresh_list()

        clear_entries()


def search_contact(event=None):

    keyword = search_var.get().lower()

    listbox.delete(0, tk.END)

    for c in contacts:

        if keyword in c["name"].lower():

            listbox.insert(
                tk.END,
                c["name"]
            )


search_entry.bind(
    "<KeyRelease>",
    search_contact
)

# ===========================================
# BUTTONS
# ===========================================

button_frame = tk.Frame(
    left,
    bg=CARD
)

button_frame.pack(
    pady=25
)

add_btn = tk.Button(
    button_frame,
    text="➕ ADD",
    width=12,
    bg="#8A2BE2",
    fg="white",
    font=("Arial",11,"bold"),
    command=add_contact
)

add_btn.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

update_btn = tk.Button(
    button_frame,
    text="✏ UPDATE",
    width=12,
    bg="#2563EB",
    fg="white",
    font=("Arial",11,"bold"),
    command=update_contact
)

update_btn.grid(
    row=0,
    column=1,
    padx=5
)

delete_btn = tk.Button(
    button_frame,
    text="❌ DELETE",
    width=12,
    bg="#DC2626",
    fg="white",
    font=("Arial",11,"bold"),
    command=delete_contact
)

delete_btn.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

clear_btn = tk.Button(
    button_frame,
    text="🧹 CLEAR",
    width=12,
    bg="#0891B2",
    fg="white",
    font=("Arial",11,"bold"),
    command=clear_entries
)

clear_btn.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

# ===========================================
# BUTTON HOVER EFFECT
# ===========================================

button_colors = {
    add_btn: "#8A2BE2",
    update_btn: "#2563EB",
    delete_btn: "#DC2626",
    clear_btn: "#0891B2"
}


def hover_on(event):
    event.widget.config(
        bg="#00E5FF",
        fg="black"
    )


def hover_off(event):
    event.widget.config(
        bg=button_colors[event.widget],
        fg="white"
    )


for btn in button_colors:
    btn.bind("<Enter>", hover_on)
    btn.bind("<Leave>", hover_off)
   # ===========================================
# 3D STYLE CONTACT CARD
# ===========================================

card = tk.Canvas(
    right,
    width=500,
    height=220,
    bg="#151530",
    highlightthickness=0
)
card.pack(pady=15)

angle = 0


def draw_card():

    global angle

    card.delete("all")

    cx = 250
    cy = 110

    w = 180
    h = 110

    depth = int(25 * math.sin(math.radians(angle)))

    x1 = cx - w // 2
    y1 = cy - h // 2

    x2 = cx + w // 2
    y2 = cy + h // 2

    # Back face
    card.create_polygon(
        x1 + depth,
        y1 - depth,
        x2 + depth,
        y1 - depth,
        x2 + depth,
        y2 - depth,
        x1 + depth,
        y2 - depth,
        fill="#00C2FF",
        outline=""
    )

    # Side face
    card.create_polygon(
        x2,
        y1,
        x2 + depth,
        y1 - depth,
        x2 + depth,
        y2 - depth,
        x2,
        y2,
        fill="#0099CC",
        outline=""
    )

    # Front face
    card.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill="#7B2FF7",
        outline="cyan",
        width=3
    )

    if selected_index is not None and selected_index < len(contacts):

        c = contacts[selected_index]

        text = (
            f"Name : {c['name']}\n\n"
            f"Phone : {c['phone']}\n\n"
            f"Email : {c['email']}"
        )

    else:

        text = "Select a Contact"

    card.create_text(
        cx,
        cy,
        text=text,
        fill="white",
        font=("Arial", 12, "bold"),
        justify="center"
    )

    angle += 4

    if angle >= 360:
        angle = 0

    root.after(40, draw_card)


draw_card()

# ===========================================
# GLOWING TITLE
# ===========================================

glow = 80
direction = 1


def animate_title():

    global glow
    global direction

    glow += direction

    if glow >= 255:
        direction = -1

    if glow <= 80:
        direction = 1

    color = "#%02x%02x%02x" % (0, glow, 255)

    title.config(fg=color)

    root.after(40, animate_title)


animate_title()

# ===========================================
# KEYBOARD SHORTCUTS
# ===========================================

root.bind("<Control-n>", lambda e: clear_entries())
root.bind("<Control-s>", lambda e: add_contact())
root.bind("<Delete>", lambda e: delete_contact())

# ===========================================
# START
# ===========================================

refresh_list()

root.mainloop()
 