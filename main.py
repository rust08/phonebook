import sqlite3
import tkinter as tk
from tkinter import ttk


# the main class
class Main(tk.Frame):
  # the init
  def __init__(self, root):
    super().__init__(root)
    self.init_main()
    self.db = db
    self.view_records()

  # setting up window
  def init_main(self):
    # toolbar
    toolbar = tk.Frame(bg='#d7d8e0', bd=2)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    # setting up button to add contact
    self.add_img = tk.PhotoImage(file='./img/add.png')
    btn_open_dialog = tk.Button(toolbar,
                                bg='#d7d8e0',
                                bd=0,
                                image=self.add_img,
                                command=self.open_dialog)
    btn_open_dialog.pack(side=tk.LEFT)

    # setting up the treeview
    self.tree = ttk.Treeview(self,
                             columns=('ID', 'name', 'number', 'gmail'),
                             height=45,
                             show='headings')
    self.tree.column("ID", width=30, anchor=tk.CENTER)
    self.tree.column("name", width=300, anchor=tk.CENTER)
    self.tree.column("number", width=150, anchor=tk.CENTER)
    self.tree.column("gmail", width=150, anchor=tk.CENTER)

    self.tree.heading('ID', text='ID')
    self.tree.heading('name', text='name')
    self.tree.heading('number', text='number')
    self.tree.heading('gmail', text='gmail')

    self.tree.pack(side=tk.LEFT)

    # setting up edit button
    self.update_img = tk.PhotoImage(file='./img/update.png')
    btn_edit_dialog = tk.Button(toolbar,
                                bg='#d7d8e0',
                                bd=0,
                                image=self.update_img,
                                command=self.open_update_dialog)
    btn_edit_dialog.pack(side=tk.LEFT)

    # setting up
    self.delete_img = tk.PhotoImage(file='./img/delete.png')
    btn_delete = tk.Button(toolbar,
                           bg='#d7d8e0',
                           bd=0,
                           image=self.delete_img,
                           command=self.delete_record)
    btn_delete.pack(side=tk.LEFT)

    # setting up search button
    self.search_img = tk.PhotoImage(file='./img/search.png')
    btn_search = tk.Button(toolbar,
                           bg='#d7d8e0',
                           bd=0,
                           image=self.search_img,
                           command=self.open_search_dialog)
    btn_search.pack(side=tk.LEFT)

    # setting up refresh button
    self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
    btn_refresh = tk.Button(toolbar,
                            bg='#d7d8e0',
                            bd=0,
                            image=self.refresh_img,
                            command=self.view_records)
    btn_refresh.pack(side=tk.LEFT)

  # add contact window command
  def open_dialog(self):
    Child()

  # command to add data into database
  def records(self, name, number, email):
    self.db.insert_data(name, number, email)

  # command that makes treeview work
  def view_records(self):
    self.db.cur.execute('SELECT * FROM db')

    [self.tree.delete(i) for i in self.tree.get_children()]

    [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

  # edit contact window command
  def open_update_dialog(self):
    Update()

  # command to edit data in database
  def update_record(self, name, number, gmail):
    self.db.cur.execute(
        '''UPDATE db SET name=?, number=?, email=? WHERE ID=?''',
        (name, number, gmail, self.tree.set(self.tree.selection()[0], '#1')))
    self.db.conn.commit()
    self.view_records()

  # command to delete data from database
  def delete_record(self):
    for selection_item in self.tree.selection():
      self.db.cur.execute('DELETE FROM db WHERE id=?',
                          (self.tree.set(selection_item, '#1')))
    self.db.conn.commit()
    self.view_records()

  # search window command
  def open_search_dialog(self):
    Search()

  # command that searches data that contains name in it
  def search_record(self, name):
    name = ('%' + name + '%')
    self.db.cur.execute('SELECT * FROM db WHERE name LIKE ?', (name, ))
    [self.tree.delete(i) for i in self.tree.get_children()]
    [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]


# add contact class
class Child(tk.Toplevel):
  # the init
  def __init__(self):
    super().__init__(root)
    self.init_child()
    self.view = app

  # setting up add contact window
  def init_child(self):
    self.title('Add contact')
    self.geometry('400x220')
    self.resizable(False, False)
    self.grab_set()
    self.focus_get()
    # setting up labels
    label_name = tk.Label(self, text='name')
    label_name.place(x=50, y=50)
    label_number = tk.Label(self, text='number')
    label_number.place(x=50, y=80)
    label_gmail = tk.Label(self, text='gmail')
    label_gmail.place(x=50, y=110)
    # setting up entries
    self.entry_name = ttk.Entry(self)
    self.entry_name.place(x=200, y=50)
    self.entry_number = ttk.Entry(self)
    self.entry_number.place(x=200, y=80)
    self.entry_gmail = ttk.Entry(self)
    self.entry_gmail.place(x=200, y=110)
    # cancel button aka second close button
    self.btn_cancel = ttk.Button(self, text='cancel', command=self.destroy)
    self.btn_cancel.place(x=300, y=170)
    # comfirm button
    self.btn_comfirm = ttk.Button(self, text='comfirm')
    self.btn_comfirm.place(x=220, y=170)
    # binding comfirm button to close window and update the treeview
    self.btn_comfirm.bind(
        '<Button-1>', lambda event: self.view.records(self.entry_name.get(
        ), self.entry_number.get(), self.entry_gmail.get()))
    self.btn_comfirm.bind('<Button-1>',
                          lambda event: self.view.view_records(),
                          add='+')
    self.btn_comfirm.bind('<Button-1>', lambda event: self.destroy(), add='+')


# edit contact class
class Update(Child):
  # the init
  def __init__(self):
    super().__init__()
    self.db = db
    self.view = app
    self.init_update()
    self.default_data()

  # setting up edit contact window
  def init_update(self):
    self.title('edit contact')
    btn_edit = ttk.Button(self, text='edit')
    btn_edit.place(x=180, y=170)
    btn_edit.bind(
        '<Button-1>',
        lambda event: self.view.update_record(self.entry_name.get(
        ), self.entry_number.get(), self.entry_number.get()))
    btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
    self.btn_comfirm.destroy()

  # default values
  def default_data(self):
    self.db.cur.execute(
        'SELECT * FROM db WHERE id=?',
        (self.view.tree.set(self.view.tree.selection()[0], '#1')))
    row = self.db.cur.fetchone()
    self.entry_name.insert(0, row[1])
    self.entry_number.insert(0, row[2])
    self.entry_gmail.insert(0, row[3])


# search contact window
class Search(tk.Toplevel):
  # the init
  def __init__(self):
    super().__init__()
    self.init_search()
    self.view = app

  # setting up window
  def init_search(self):
    self.title('search contact')
    self.geometry('300x200')
    self.resizable(False, False)
    # label
    label_search = tk.Label(self, text='name')
    label_search.place(x=50, y=20)
    # entry
    self.entry_search = ttk.Entry(self)
    self.entry_search.place(x=105, y=20, width=150)
    # cancel button
    btn_cancel = ttk.Button(self, text='cancel', command=self.destroy)
    btn_cancel.place(x=185, y=50)
    #setting up the button and binding it to search and close search contact window
    btn_search = ttk.Button(self, text='search')
    btn_search.place(x=105, y=50)
    btn_search.bind(
        '<Button-1>',
        lambda event: self.view.search_record(self.entry_search.get()))
    btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# database class
class DB():
  # setting up the database if it doesn't exist
  def __init__(self):
    self.conn = sqlite3.connect('db.db')
    self.cur = self.conn.cursor()
    self.cur.execute('''CREATE TABLE IF NOT EXISTS db (
          id INTEGER PRIMARY KEY,
          name TEXT,
          number TEXT,
          email TEXT
      )''')
    self.conn.commit()

  # command that inserts data
  def insert_data(self, name, number, gmail):
    self.cur.execute('INSERT INTO db (name, number, email) VALUES (?, ?, ?)',
                     (name, number, gmail))
    self.conn.commit()


# controlling the code so if the file isn't
if __name__ == '__main__':
  root = tk.Tk()
  db = DB()
  app = Main(root)
  app.pack()
  root.title('phonebook')
  root.geometry('685x450')
  root.resizable(False, False)
  root.mainloop()
