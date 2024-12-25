from tkinter import *
import sqlite3
from hashlib import sha256

with sqlite3.connect('data.db') as connection:
    cursor = connection.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT,
        auth TEXT,
        role TEXT
    );
    '''

    cursor.execute(create_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        authorId INTEGER,
        report TEXT,
        level INTEGER
    );
    '''

    cursor.execute(create_table_query)

    connection.commit()

root = Tk()

def page3(root):
    global admin
    global user
    root.title("report management applciation")
    root.geometry('960x540')

    wellbl = Label(root, text = ("welcome user id:" + str(user[0])) + ", role:" + str(user[3]))
    wellbl.place(relx=0.5, rely=0.35, anchor=CENTER)

    rptlbl = Label(root, text = "mange reports")
    rptlbl.place(relx=0.5, rely=0.4, anchor=CENTER)
      
    scroll_bar = Scrollbar(root) 
    
    scroll_bar.pack( side = RIGHT, 
                    fill = Y ) 
    
    mylist = Listbox(root,  
                    yscrollcommand = scroll_bar.set ) 
    
    mylist.pack( side = LEFT, fill = BOTH ) 

    mylist.place(relx=0.5, rely=0.6, width=500, height=300, anchor=CENTER)
    
    scroll_bar.config( command = mylist.yview ) 

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()

        selectQuery = "SELECT * FROM Reports;"

        cursor.execute(selectQuery)

        data = cursor.fetchall()

        for i in data: 
            mylist.insert(END, str(i[1]) + " level:" + str(i[4]) + " id:" + str(i[0]) + "\n" + str(i[3]))
    def deleate():
        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            delQuery = '''
                DELETE FROM Reports WHERE id = ''' + DelEntry.get() + '''
            '''

            cursor.execute(delQuery)

            connection.commit()

    delEntryLabel = Label(root, text = "enter id")
    delEntryLabel.place(relx=0.85, rely=0.45, anchor=CENTER)

    DelEntry = Entry(root, width=10)
    DelEntry.place(relx=0.85, width=50, rely=0.55, anchor=CENTER)

    deleatebtn = Button(root, text = "deleate report" ,
                       bg = "lightgrey", command=deleate)
    deleatebtn.place(relx=0.85, rely=0.6, anchor=CENTER)

    def toReport():
        changepage(2)


    toreportbtn = Button(root, text = "back" ,
                       bg = "lightgrey", command=toReport)
    toreportbtn.place(relx=0.15, rely=0.2, anchor=CENTER)

def page2(root):
    global admin
    global user
    root.title("report management applciation")
    root.geometry('960x540')

    wellbl = Label(root, text = ("welcome user id:" + str(user[0])) + ", role:" + str(user[3]))
    wellbl.place(relx=0.5, rely=0.35, anchor=CENTER)

    rptlbl = Label(root, text = "make report")
    rptlbl.place(relx=0.5, rely=0.4, anchor=CENTER)

    nameEntry = Entry(root, width=10)
    nameEntry.grid(column =1, row =0)
    nameEntry.place(relx=0.5, width=300, rely=0.45, anchor=CENTER)

    nameEntryLabel = Label(root, text = "report name")
    nameEntryLabel.grid()
    nameEntryLabel.place(relx=0.2, rely=0.45, anchor=W)

    levelEntry = Entry(root, width=10)
    levelEntry.grid(column =1, row =0)
    levelEntry.place(relx=0.5, width=300, rely=0.5, anchor=CENTER)

    levelEntryLabel = Label(root, text = "severity level 1-10")
    levelEntryLabel.grid()
    levelEntryLabel.place(relx=0.2, rely=0.5, anchor=W)

    ReportEntry = Entry(root, width=10)
    ReportEntry.grid(column =1, row =0)
    ReportEntry.place(relx=0.5, width=300, rely=0.55, anchor=CENTER)

    ReportEntryLabel = Label(root, text = "report description")
    ReportEntryLabel.grid()
    ReportEntryLabel.place(relx=0.2, rely=0.55, anchor=W)

    def send():
        with sqlite3.connect('data.db') as connection:
                cursor = connection.cursor()

                insertQuery = '''
                INSERT INTO Reports (name, authorId, report, level) 
                VALUES (?, ?, ?, ?);
                '''

                reportData = (str(nameEntry.get()), str(user[0]), str(ReportEntry.get()), str(levelEntry.get()))

                cursor.execute(insertQuery, reportData)

                connection.commit()

    def report():
        changepage(3)


    reportbtn = Button(root, text = "send report" ,
                       bg = "lightgreen", command=send)
    reportbtn.grid(column=2, row=0)
    reportbtn.place(relx=0.5, rely=0.6, anchor=CENTER)

    def toStart():
        changepage(1)


    tostartbtn = Button(root, text = "back" ,
                       bg = "lightgrey", command=toStart)
    tostartbtn.grid(column=2, row=0)
    tostartbtn.place(relx=0.15, rely=0.2, anchor=CENTER)


    if user[2] == admin:
        adminbtn = Button(root, text = "mange reports" ,
                          bg = "grey", command=report)
        adminbtn.grid(column=2, row=0)
        adminbtn.place(relx=0.5, rely=0.7, anchor=CENTER)

    

def page1(root):
    root.title("report management applciation")
    root.geometry('960x540')

    lbl = Label(root, width=20, height=20, text = "sign in or create account")
    lbl.place(relx=0.5, rely=0.4, anchor=CENTER)

    txt = Entry(root, width=10)
    txt.grid(column =1, row =0)
    txt.place(relx=0.5, width=100, rely=0.45, anchor=CENTER)

    namelbl = Label(root, text = "user id")
    namelbl.grid()
    namelbl.place(relx=0.35, rely=0.45, anchor=W)

    passtxt = Entry(root, show="*", width=10)
    passtxt.grid(column =1, row =0)
    passtxt.place(relx=0.5, width=100, rely=0.5, anchor=CENTER)

    passlbl = Label(root, text = "password")
    passlbl.grid()
    passlbl.place(relx=0.35, rely=0.5, anchor=W)

    def login():
        global user
        with sqlite3.connect('data.db') as connection:
                cursor = connection.cursor()

                select_query = "SELECT * FROM Users WHERE id='" + txt.get() + "';"

                cursor.execute(select_query)

                user = cursor.fetchone()

                if str(sha256(passtxt.get().encode('utf-8')).hexdigest()) == user[1]:
                    print("corect password")
                    changepage(2)
                else:
                    print("incrorect password or id")

    def create():
        global createdOnce
        global codetxt
        global roletxt
        if createdOnce == False:
            codetxt = Entry(root, show="*", width=10)
            codetxt.grid(column =1, row =0)
            codetxt.place(relx=0.65, rely=0.45, anchor=CENTER)

            codelbl = Label(root, text = "auth code")
            codelbl.grid()
            codelbl.place(relx=0.55, rely=0.45, anchor=W)

            roletxt = Entry(root, width=10)
            roletxt.grid(column =1, row =0)
            roletxt.place(relx=0.65, rely=0.5, anchor=CENTER)

            rolelbl = Label(root, text = "user role")
            rolelbl.grid()
            rolelbl.place(relx=0.55, rely=0.5, anchor=W)
            createdOnce = True
        else:
            with sqlite3.connect('data.db') as connection:
                cursor = connection.cursor()

                insertQuery = '''
                INSERT INTO Users (password, auth, role) 
                VALUES (?, ?, ?);
                '''

                userData = (str(sha256(passtxt.get().encode('utf-8')).hexdigest()), str(codetxt.get()), str(roletxt.get()))

                cursor.execute(insertQuery, userData)

                connection.commit()

    loginbtn = Button(root, text = "login" ,
                      bg = "lightgreen", command=login)
    loginbtn.grid(column=2, row=0)
    loginbtn.place(relx=0.525, rely=0.6, anchor=CENTER)

    signupbtn = Button(root, text = "sign up" ,
                       bg = "grey", command=create)
    signupbtn.grid(column=2, row=0)
    signupbtn.place(relx=0.475, rely=0.6, anchor=CENTER)

def changepage(pagenum):
    global root
    for widget in root.winfo_children():
        widget.destroy()
    if pagenum == 2:
        page2(root)
        pagenum = 2
    elif pagenum == 1:
        page1(root)
        pagenum = 1
    elif pagenum == 3:
        page3(root)
        pagenum = 3

user = []
createdOnce = False
admin = "4dm1n"

page1(root)
root.mainloop()
