from customtkinter import *
from tkinter import *
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import sqlite3
import pymysql
import hashlib
import ctypes


scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
set_appearance_mode("dark")
set_default_color_theme("green")  #"my_colors.json")

global_schemas = []
global_schema_name = []
global_tables = []
global_table_names = []
global_table_columns = []

host_ip, host_port, host_user, host_password = [None,None,None,None]
def connection():  
    conn=pymysql.connect(
        host=host_ip, 
        port=host_port, user=host_user, 
        password=host_password 
    )
    return conn 


root = CTk()
# CHANGE TITLE!!!
root.title("Lightweight SQLworkbench")

def centerWindow():
    root.update()
    scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    w = root.winfo_width()//scale_factor
    print(root.winfo_width())   
    h = root.winfo_height()//scale_factor
    print(root.winfo_height())
    screen_width = root.winfo_screenwidth()*scale_factor  # Width of the screen
    print(screen_width)
    screen_height = root.winfo_screenheight()*scale_factor # Height of the screen
    print(screen_height)
    x = (screen_width/2) - (w)
    y = (screen_height/2) - (h)
    
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


    print(root.winfo_width())  
    print(root.winfo_height())



def login_page():
    root.geometry("1080x720")
    centerWindow()
    # root.eval("tk::PlaceWindow . center")
    def forward_to_admin_page():
        login_frame.destroy()
        root.update()
        admin_page()
    
    def verify():
        conn = sqlite3.connect('authenticate.db')   # Usename = Admin, Password = admin
        table_create_query = '''CREATE TABLE IF NOT EXISTS authentication
                (Uname VARCHAR(200) NOT NULL,
                Pwd STR(200) NOT NULL,
                PRIMARY KEY (UNAME))'''
        conn.execute(table_create_query)
        return conn

    def hash_password():
        # Hash the password using a secure hashing algorithm
        hashed_password = hashlib.sha256(password_ent.get().encode()).hexdigest()
        return hashed_password

    def login():
        # print("Test")
        username = username_ent.get()
        hashed_password = hash_password()
        conn=verify()
        cursor = conn.cursor()
        query = "SELECT Pwd FROM authentication WHERE Uname = ?"  # '%s'" % username
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            stored_password = result[0]
            if hashed_password == stored_password:
                forward_to_admin_page()
                return
            else:
                messagebox.showwarning(title= "Error", message="Incorrect password!")
        else:
            messagebox.showwarning(title= "Error", message="User not found!")

    login_frame = CTkFrame(master=root)
    login_frame.pack(pady=20, padx=60, fill="both", expand=True)
    
    label = CTkLabel(master=login_frame, text="Admin Login", font=("Roboto", 24))
    label.pack(pady=12, padx=10)
    label.place(x=402.5 , y=120)

    username_ent = CTkEntry(master=login_frame, placeholder_text="Username")
    username_ent.pack(pady=12, padx=10)
    username_ent.place(x=402.5, y=170)

    password_ent = CTkEntry(master=login_frame, placeholder_text="Password", show="*")
    password_ent.bind("<Return>", lambda event: login_btn.invoke())
    password_ent.pack(pady=12, padx=10)
    password_ent.place(x=402.5, y=210)

    login_btn = CTkButton(master=login_frame, text="Login", text_color="white" ,command=login)
    login_btn.pack(pady=12, padx=10)
    login_btn.place(x=402.5, y=250)

    id_info_lb = CTkLabel(master=login_frame, text='''Warning!
this program only
works with mariaDB.''')
    id_info_lb.place(x=410, y=290)


def admin_page():
    # tkinter hub skal inn og må tilpasses customtkinter
    def return_to_login_page():
        options_frame.destroy()
        main_frame.destroy()
        root.update()
        login_page()

    root.geometry("1080x720")
    root.title('Tkinter Hub')


    def home_page():
        delete_pages()

        def db_connection():
            global host_ip, host_port, host_user, host_password
            global global_schemas
            global_schemas = None
            host_ip = db_ip_ent.get()  #
            host_port = int(db_port_ent.get())
            host_user = db_username_ent.get()
            host_password = db_password_ent.get()
            conn_lb = CTkLabel(db_login_frame, text="Attempting to connect...", text_color="#F80", font=("Roboto", 20))
            conn_lb.place(x=360, y=45)
            root.update()
            try:
                conn=connection()
                 
                # conn_lb.destroy()
                conn_lb.configure(text="Connection successfull!", text_color="#00ad32", font=("Roboto", 20))   # = CTkLabel(db_login_frame, text="Connection successfull!", text_color="#00ad32")
                # conn_lb.place(x=360, y=45)
                return conn 
            except:
                # conn_lb.destroy()

                conn_lb.configure(text="Connection timed out....", text_color="#ff0000", font=("Roboto", 20))       # = CTkLabel(db_login_frame, text="Connection failed!", text_color="#ff0000")
                # conn_lb.place(x=361, y=45)
                

        def schema():
            global global_schemas
            conn=db_connection()
            cursor=conn.cursor()
            cursor.execute("SELECT schema_name FROM information_schema.SCHEMATA;")
            schemas=cursor.fetchall()
            conn.commit()
            conn.close()
            global_schemas = results = [schema[0] for schema in schemas]
            insert_text = "\n".join(results)
            text = Text(db_login_frame, height=30, width=40, font=("Roboto", 15), wrap=WORD, fg="white", bg="gray14")
            scroll = CTkScrollbar(db_login_frame)
            text.configure(yscrollcommand=scroll.set)
            text.place(x=465, y= 150)
                        
            text.insert(END, insert_text)
            




        db_login_frame = CTkFrame(master=main_frame)
        db_login_frame.pack(side=LEFT)
        db_login_frame.pack_propagate(False)
        db_login_frame.configure(width=930, height=720)
        # db_login_frame.pack(pady=20)


        db_login_lb = CTkLabel(master=db_login_frame, text='Please logg in to your mariaDB', font=("Roboto", 24))
        db_login_lb.pack(pady=10)
        # db_login_ent = CTkEntry()


        db_ip_lb = CTkLabel(master=db_login_frame, text='Please enter IP address:', font=("Roboto", 14), justify=LEFT)

        db_ip_lb.place(x=20, y=45)

        db_ip_ent = CTkEntry(master=db_login_frame, placeholder_text="IP-Address")
        db_ip_ent.bind("<Return>", lambda event: db_login_btn.invoke())
        db_ip_ent.place(x=20, y=70)

    
        db_port_lb = CTkLabel(master=db_login_frame, text='Enter port:', font=("Roboto", 14))
        db_port_lb.place(x=20, y=105)

        db_port_ent = CTkEntry(master=db_login_frame, placeholder_text="Port")
        db_port_ent.bind("<Return>", lambda event: db_login_btn.invoke())
        db_port_ent.place(x=20, y=130)


        db_username_lb = CTkLabel(master=db_login_frame, text='Server username:', font=("Roboto", 14))
        db_username_lb.place(x=20, y=165)

        db_username_ent = CTkEntry(master=db_login_frame, placeholder_text="Username")
        db_username_ent.bind("<Return>", lambda event: db_login_btn.invoke())
        db_username_ent.place(x=20, y=190)


        db_password_lb = CTkLabel(master=db_login_frame, text='Server password:', font=("Roboto", 14))
        db_password_lb.place(x=20, y=225)

        db_password_ent = CTkEntry(master=db_login_frame, placeholder_text="Password")
        db_password_ent.bind("<Return>", lambda event: db_login_btn.invoke())
        db_password_ent.place(x=20, y=250)


        db_login_btn = CTkButton(master=db_login_frame, text="Login", text_color="white" ,command=schema)
        db_login_btn.place(x=20, y=310)


        # textbox = CTkTextbox(db_login_frame)

        # textbox.insert("0.0", "new text to insert")  # insert at line 0 character 0
        # # text = textbox.get("0.0", "end")  # get text from line 0 character 0 till the end
        # textbox.delete("0.0", "end")  # delete all text
        # textbox.configure(state="disabled")  # configure textbox to be read-only


  



    def menu_page():    ### <----- WORKING HERE ATM!!!
        delete_pages()
        menu_frame = CTkFrame(master=main_frame)
        menu_frame.pack(side=LEFT)
        menu_frame.pack_propagate(False)
        menu_frame.configure(width=930, height=720)


        # welcome_lb = CTkLabel(master=menu_frame, text='Please enter IP address:', font=("Roboto", 14), justify=LEFT)
        # # db_ip_lb.pack()
        # welcome_lb.place(x=20, y=50)
        def table():
            global global_schema_name
            global global_table_names
            conn=connection()
            global_schema_name = schema_name = schema_name_combobox.get()
            cursor=conn.cursor()
            print(schema_name)
            cursor.execute("SHOW tables FROM `{}`;".format(schema_name))
            global_table_names = tables=cursor.fetchall()
            conn.commit()
            conn.close()
            results = [table[0] for table in tables]
            insert_text = "\n".join(results)
            text = Text(menu_frame, height=30, width=40, font=("Roboto", 15), wrap=WORD, fg="white", bg="gray14")
            scroll = CTkScrollbar(menu_frame)
            text.configure(yscrollcommand=scroll.set)
            text.place(x=465, y= 150)
                        
            text.insert(END, insert_text)

        # # Multiple line query entry box
        # query_ent = scrolledtext.ScrolledText(menu_frame, font=("Roboto", 14), wrap=WORD, width=50, height=20)
        # query_ent.place(x=120, y= 180)


        schema_name_label = CTkLabel(menu_frame, text="Please select scema from dropdown", font=("Roboto", 14), justify=LEFT)
        schema_name_label.place(x=20, y=50)
        schema_name_combobox = ttk.Combobox(menu_frame, font=("Roboto", 14), values=global_schemas)
        schema_name_combobox.place(x=400, y=75)

        db_table_btn = CTkButton(master=menu_frame, text="Get tables", text_color="white" ,command=table)
        db_table_btn.place(x=20, y=310)

        # text_area = scrolledtext.ScrolledText(root, wrap=WORD,
        #                                     width=40, height=8,
        #                                     font=("Times New Roman", 15))
        # text_area.grid(column=0, row=2, pady=10, padx=10)
        # text_area.place(x=100, y=100)


    def contact_page():
        delete_pages()
        table_frame = CTkFrame(main_frame)
        table_frame.pack(side=LEFT)
        table_frame.pack_propagate(False)
        table_frame.configure(width=930, height=720)

        def columns():
            global global_schema_name
            global global_table_columns
            conn=connection()
            table_name = table_name_combobox.get()
            cursor=conn.cursor()
            print(table_name)
            cursor.execute("Select * FROM `{}`.`{}`;".format(global_schema_name, table_name))
            global_table_columns = tables=cursor.fetchall()
            name_results = [i[0] for i in cursor.description]
            conn.commit()
            conn.close()
            results = [table for table in tables]
            insert_text = results  #"\n".join(results)
            text = Text(table_frame, height=30, width=40, font=("Roboto", 15), wrap=WORD, fg="white", bg="gray14")
            scroll = CTkScrollbar(table_frame)
            text.configure(yscrollcommand=scroll.set)
            text.place(x=465, y= 150)
                        
            text.insert(END, insert_text)
            print(name_results)
        # # Multiple line query entry box
        # query_ent = scrolledtext.ScrolledText(table_frame, font=("Roboto", 14), wrap=WORD, width=50, height=20)
        # query_ent.place(x=120, y= 180)


        table_name_label = CTkLabel(table_frame, text="Please select table from dropdown", font=("Roboto", 14), justify=LEFT)
        table_name_label.place(x=20, y=50)
        table_name_combobox = ttk.Combobox(table_frame, font=("Roboto", 14), values=global_table_names)
        table_name_combobox.place(x=400, y=75)

        db_table_btn = CTkButton(master=table_frame, text="Get tables", text_color="white" ,command=columns)
        db_table_btn.place(x=20, y=310)




    def about_page():
        delete_pages()
        about_frame = CTkFrame(main_frame)

        lb = CTkLabel(about_frame, text='About Page\n\nPage: 4', font=("Roboto", 24))
        lb.pack()

        about_frame.pack(pady=20)


    def delete_pages():
        for frame in main_frame.winfo_children():
            frame.destroy()



    # Menu frame
    options_frame = CTkFrame(master=root)
    options_frame.pack(side=LEFT)
    options_frame.pack_propagate(False)
    options_frame.configure(width=160, height=720)

    # Menu buttons
    home_btn = CTkButton(options_frame, text='Server login', font=("Roboto", 15), command=home_page)
    home_btn.place(x=10, y=50)

    menu_btn = CTkButton(options_frame, text='Schema', font=("Roboto", 15), command=menu_page)
    menu_btn.place(x=10, y=100)

    contact_btn = CTkButton(options_frame, text='Tables', font=("Roboto", 15), command=contact_page)
    contact_btn.place(x=10, y=150)

    about_btn = CTkButton(options_frame, text='About', font=("Roboto", 15), command=about_page)
    about_btn.place()

    logout_btn = CTkButton(options_frame, text="Logout", font=("Roboto", 15), command=return_to_login_page)
    logout_btn.place(x=10, y=680)


    # Main frame
    main_frame = CTkFrame(root)
    main_frame.pack(side=LEFT)
    main_frame.pack_propagate(False)
    main_frame.configure(width=930, height=720)






# Testing for now
login_page()
# admin_page()


root.bind("<Escape>", lambda event: root.destroy())
root.mainloop()