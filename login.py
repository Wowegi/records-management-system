from tkinter import *
import menu
from werkzeug.security import check_password_hash, generate_password_hash
import tkinter.messagebox as mb
from PIL import ImageTk, Image
import logging
logging.getLogger('PIL').setLevel(logging.WARNING)

class Page:
    def __init__(self, window, db):
        self.window = window
        self.window.geometry('950x600')
        self.window.resizable(0, 0)
        self.window.title('School Records Management System')
        self.db = db
                
        # Frames
        self.frame = Frame(self.window, bg='#101010', width=950, height=600)
        self.frame.place(x=0, y=0)
        self.login_frame = Frame(self.frame, bg="#000000", width=400, height=530)
        self.login_frame.place(x=260, y=30)
        
        # User Image
        self.user_image = Image.open('images\\user.png')
        photo = ImageTk.PhotoImage(self.user_image)
        self.user_image_label = Label(self.login_frame, image=photo, bg='#000000')
        self.user_image_label.image = photo
        self.user_image_label.place(x=80, y=0) 

        # Username
        self.username_label = Label(self.login_frame, text="Username", bg="#000000", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=60, y=240)
        self.username_entry = Entry(self.login_frame, highlightthickness=0, relief=FLAT, bg="#000000", fg="#D3D3D3",
                                    font=("yu gothic ui ", 12), insertbackground="#FFFFFF")
        self.username_entry.place(x=60, y=270, width=285)
        self.username_line = Canvas(self.login_frame, width=285, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=60, y=295)  
        
 
        # Password
        self.password_label = Label(self.login_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=60, y=325)
        self.password_entry = Entry(self.login_frame, highlightthickness=0, relief=FLAT, bg="#000000", fg="#D3D3D3",
                                    font=("yu gothic ui", 12), show="*", insertbackground="#FFFFFF")
        self.password_entry.place(x=60, y=355, width=285)
        self.password_line = Canvas(self.login_frame, width=285, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=60, y=380)
        
        # Show/Hide password
        self.show_image = ImageTk.PhotoImage(file='images\\show.png')
        self.hide_image = ImageTk.PhotoImage(file='images\\hide.png')
        self.show_button = Button(self.login_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=320, y=355)
        
        # Login button
        self.login = Button(self.login_frame, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=28, bd=0,
                            bg='#006600', cursor='hand2', activebackground='#006600', fg='white', command=self.submitact)
        self.login.place(x=60, y=430)
        
    def show(self):
        """Display the password"""
        self.hide_button = Button(self.login_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=320, y=355)
        self.password_entry.config(show='')
        
    def hide(self):
        """Hide the password"""
        self.show_button = Button(self.login_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=320, y=355)
        self.password_entry.config(show='*')

    def submitact(self):
        """ Submit username and password"""
        user = self.username_entry.get()
        password = self.password_entry.get()

        # Check for username and password
        if len(user) == 0:
            mb.showerror('Error!', "Please Enter your username")
            return
        if password == "":
            mb.showerror('Error!', "Please Enter your password")
            return

        #self.db.execute("INSERT INTO users (username, password) VALUES(?, ?)", user, generate_password_hash(password))

        # Query database for username
        rows = self.db.execute("SELECT * FROM users WHERE username = ?", user)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            mb.showerror('Error!', "Invalid username or password")
            return
        
        self.destroy()

    def destroy(self):
        self.frame.destroy()
        menu.mainMenu(self.window, self.db)