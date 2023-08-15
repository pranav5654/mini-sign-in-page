from tkinter import *
from sqlite3 import *
from tkinter import messagebox
from tkinter import font

conn = connect('userdata.db')
c = conn.cursor()


#uncommnet to run for the first time and create a database , after that comment for rest of the runs
'''c.execute("""CREATE TABLE userdata(
          username text,
          password text)
           """)

c.execute("""CREATE TABLE yesno(
          yesno integer)
           """)
c.execute("INSERT INTO yesno VALUES(:yesno)",
                {"yesno":0
                 })'''

conn.commit()
conn.close()


def logout():
    root.destroy()
    setting()
    conn = connect('userdata.db')
    c = conn.cursor()
    c.execute("INSERT INTO yesno VALUES(:yesno)",
              {"yesno": 0
               })
    conn.commit()
    conn.close()




def editaccount():
    global i
    global new_window_edit
    global username_entry_edit
    global password_entry_edit
    m_font = font.Font(family="Helvectica", size=20)
    my_font = font.Font(size=15)
    try:
        new_window_edit.destroy()
    except:
        print("")
    new_window_edit = Toplevel()
    new_window_edit.title("Edit  Account")
    Label(new_window_edit, text="EDIT ACCOUNT", font=m_font, bg="yellow", fg="green").grid(row=0, column=0,
                                                                                           columnspan=2)
    username_label_edit = Label(new_window_edit, text="Username ", font="Helvetica")
    username_label_edit.grid(row=1, column=0, padx=(50, 0))
    password_label_edit = Label(new_window_edit, text="Password ", font="Helvetica")
    password_label_edit.grid(row=2, column=0, padx=(50, 0))
    username_entry_edit = Entry(new_window_edit, bd=5)
    username_entry_edit.grid(row=1, column=1, ipadx=30)
    password_entry_edit = Entry(new_window_edit, bd=5)
    password_entry_edit.grid(row=2, column=1, ipadx=30)

    edit_account_button = Button(new_window_edit, text="Create", font=my_font, bg="red", command=edit)
    edit_account_button.grid(row=3, column=0, padx=(50, 0), ipadx=100, columnspan=2)

    username_entry_edit.insert(0, user)
    password_entry_edit.insert(0, pas)


def console_page():
    global root
    root = Tk()
    f = font.Font(family="Harlow Solid Italic", size=40)
    root.title("Menu")
    root.configure(bg="light green")
    root.geometry("1001x509")
    menu_bar = LabelFrame(root, pady=10, bg='#fed8b1')
    menu_bar.grid(row=0, column=0, columnspan=5)
    Button(menu_bar, text="Log Out", command=logout, bg="yellow").grid(row=0, column=1, ipadx=20, ipady=5, padx=(1, 0))
    Label(menu_bar, text="............C. O. N. S. O. L. E............", bg="blue", fg="white", font=f, padx=80,
          pady=20).grid(row=0, column=0, rowspan=2)
    Button(menu_bar, text="Edit Profile", command=editaccount, bg="#00FE0E", fg="#016017").grid(row=1, column=1,
                                                                                                ipadx=11, ipady=5,
                                                                                                padx=(1, 0))

    root.mainloop()


def sign_in():
    global root
    global user
    global pas
    conn = connect('userdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM userdata")
    a = c.fetchall()
    if (str(username_entry.get()), str(password_entry.get())) in a:
        user = username_entry.get()
        pas = password_entry.get()
        i = a.index((str(username_entry.get()), str(password_entry.get())))
        root.destroy()
        console_page()
        c.execute("INSERT INTO yesno VALUES(:yesno)",
                  {"yesno": 1
                   })
    else:
        messagebox.showerror("INVALID", "Username or password does not match")
    conn.commit()
    conn.close()


def create():
    conn = connect('userdata.db')
    c = conn.cursor()
    userlen = len(username_entry_create.get())
    passlen = len(password_entry_create.get())
    if 40 >= userlen >= 8 and 40 >= passlen >= 8:
        c.execute('INSERT INTO userdata VALUES(:username,:password)',
                  {"username": username_entry_create.get(),
                   "password": password_entry_create.get()}
                  )
        new_window_create.destroy()
        messagebox.showinfo("Account Created", "Your account has been successfully created")
        conn.commit()
        conn.close()
    else:
        messagebox.showwarning("INVALID", "Username and password must be 8 to 40 characters long")
        username_entry_create.focus()


def new_account():
    global new_window_create
    global username_entry_create
    global password_entry_create
    try:
        new_window_create.destroy()
    except:
        print("")
    new_window_create = Toplevel()
    new_window_create.title("Create Account")
    Label(new_window_create, text="CREATE NEW ACCOUNT", font=m_font, bg="yellow", fg="green").grid(row=0, column=0,
                                                                                                   columnspan=2)
    username_label_create = Label(new_window_create, text="Username ", font="Helvetica")
    username_label_create.grid(row=1, column=0, padx=(50, 0))
    password_label_create = Label(new_window_create, text="Password ", font="Helvetica")
    password_label_create.grid(row=2, column=0, padx=(50, 0))
    username_entry_create = Entry(new_window_create, bd=5)
    username_entry_create.grid(row=1, column=1, ipadx=30)
    password_entry_create = Entry(new_window_create, bd=5)
    password_entry_create.grid(row=2, column=1, ipadx=30)

    create_account_button = Button(new_window_create, text="Create", font=my_font, bg="red", command=create)
    create_account_button.grid(row=3, column=0, padx=(50, 0), ipadx=100, columnspan=2)


def delete():
    conn = connect('userdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM userdata")
    a = c.fetchall()
    if (str(username_entry_delete.get()), str(password_entry_delete.get())) in a:
        i = a.index((str(username_entry_delete.get()), str(password_entry_delete.get())))
        c.execute("SELECT *,oid FROM userdata")
        s = c.fetchall()
        c.execute("DELETE FROM userdata WHERE oid=" + str(s[i][2]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Account Deleted", "Your account has been successfully deleted")
    else:
        messagebox.showerror("INVALID", "Account does not exist")
        username_entry_delete.focus()


def delete_account():
    global new_window_delete
    global username_entry_delete
    global password_entry_delete
    try:
        new_window_delete.destroy()
    except:
        print("")
    new_window_delete = Toplevel()
    new_window_delete.title("Delete Account")
    Label(new_window_delete, text="      DELETE ACCOUNT     ", font=m_font, bg="yellow", fg="green").grid(row=0,
                                                                                                          column=0,
                                                                                                          columnspan=2)
    username_label_delete = Label(new_window_delete, text="Username ", font="Helvetica")
    username_label_delete.grid(row=1, column=0, padx=(50, 0))
    password_label_delete = Label(new_window_delete, text="Password ", font="Helvetica")
    password_label_delete.grid(row=2, column=0, padx=(50, 0))
    username_entry_delete = Entry(new_window_delete, bd=5)
    username_entry_delete.grid(row=1, column=1, ipadx=30)
    password_entry_delete = Entry(new_window_delete, bd=5)
    password_entry_delete.grid(row=2, column=1, ipadx=30)

    delete_account_button = Button(new_window_delete, text="Delete", font=my_font, bg="red", command=delete)
    delete_account_button.grid(row=3, column=0, padx=(50, 0), ipadx=100, columnspan=2)


def setting():
    global root
    global account_font
    global my_font
    global m_font
    global username_entry
    global password_entry
    root = Tk()
    root.geometry("345x180")
    root.config(bg="light green")
    root.title("CONSOLE")
    account_font = font.Font(size=8)
    my_font = font.Font(size=15)
    m_font = font.Font(family="Helvectica", size=20)
    title_label = Label(root, text="CONSOLE    ", bg="blue", fg="white", font="Helvectia", padx=20, pady=5)
    title_label.grid(row=0, column=0, columnspan=2, sticky=W + E)
    username_label = Label(root, text="Username", font="Helvectia")
    username_label.grid(row=1, column=0, padx=(45, 10))
    password_label = Label(root, text="Password", font="Helvectia")
    password_label.grid(row=2, column=0, padx=(45, 10))
    username_entry = Entry(root, bd=5)
    username_entry.grid(row=1, column=1, ipadx=30)
    password_entry = Entry(root, bd=5)
    password_entry.grid(row=2, column=1, ipadx=30)
    signin_button = Button(root, bg="yellow", text="Sign In", command=sign_in)
    signin_button.grid(row=3, column=0, padx=(50, 0), ipadx=120, columnspan=2, pady=7)
    new_account_button = Button(root, text="Don't have a account?\nCreate a new one here!", font=account_font,
                                fg="blue", command=new_account)
    new_account_button.grid(row=5, column=0, padx=(10, 10), ipadx=5)
    delete_account_button = Button(root, text="Delete account", font=account_font, fg="blue", command=delete_account)
    delete_account_button.grid(row=5, column=1, ipadx=5, pady=(5, 0))
    root.mainloop()


conn = connect('userdata.db')
c = conn.cursor()
c.execute("SELECT * FROM yesno")
a = c.fetchall()
print(a)
if a[-1][0] == 1:
    console_page()
else:
    setting()
conn.commit()
conn.close()
