from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as mb
from pathlib import Path
import os
import logging
logging.getLogger('PIL').setLevel(logging.WARNING)

class mainMenu:
    def __init__(self, window, db):
        self.window = window
        self.db = db
        
        # Frames
        self.frame = Frame(self.window, bg='#202020', width=950, height=600)
        self.frame.place(x=0, y=0)
                       
        # Heading
        self.heading = Label(self.frame, text="DASHBOARD", font=('yu gothic ui', 25, "bold"), bg="#004d00",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=0, y=0, width=950, height=80)

        # Configure the style Treeview widget
        s = ttk.Style()
        s.theme_use('clam')
        #s.configure('Treeview.Heading', background="#E8E8E8", font=('Calibri', 13,'bold'))
        s.configure("Treeview", background="#4dffa6", fieldbackground="#ccccb3", foreground="#ebebe0")
        #s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        
        # Tree
        self.tree = ttk.Treeview(self.frame, height=500, selectmode=BROWSE, 
                   columns=('ID', "Filename", "File Type", "Timestamp"))
        X_scroller = Scrollbar(self.tree, orient=HORIZONTAL, command=self.tree.xview)
        Y_scroller = Scrollbar(self.tree, orient=VERTICAL, command=self.tree.yview)
        X_scroller.pack(side=BOTTOM, fill=X)
        Y_scroller.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
        self.tree.heading('ID', text='ID', anchor=CENTER, )
        self.tree.heading('Filename', text='Filename', anchor=CENTER)
        self.tree.heading('File Type', text='File Type', anchor=CENTER)
        self.tree.heading('Timestamp', text='Timestamp', anchor=CENTER)
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('#1', width=30, stretch=NO)
        self.tree.column('#2', width=350, stretch=NO)
        self.tree.column('#3', width=80, stretch=NO)
        self.tree.place(y=80, relwidth=0.7, relheight=0.865, relx=0)    
        
        self.display_records()

        # Add pdf button
        self.pdf = Button(self.frame, text='Add pdf', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#006600', cursor='hand2', activebackground='#006600', fg='white', command=self.selectpdf)
        self.pdf.place(x=700, y=120)

        # Add photo button
        self.photo = Button(self.frame, text='Add Photo', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#006600', cursor='hand2', activebackground='#006600', fg='white', command=self.selectphoto)
        self.photo.place(x=700, y=180)

        # View file button
        self.view = Button(self.frame, text='View File', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#006600', cursor='hand2', activebackground='#006600', fg='white', command=self.view)
        self.view.place(x=700, y=300)

        # Delete file button
        self.d = Button(self.frame, text='Delete File', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#006600', cursor='hand2', activebackground='#006600', fg='red', command=self.delete)
        self.d.place(x=700, y=360)

    def selectpdf(self):
        """Choose pdf file"""
        filetypes = (
            ('pdf', '*.pdf'),
            ('png', '*.png'),
            ('jpg', '*.jpg'),
            ('All files', '*.*')
        )

        filenames = filedialog.askopenfilenames(
            title='Open file',
            initialdir='/',
            filetypes=filetypes
        )

        self.save(filenames, "pdf")

    def selectphoto(self):
        """Choose png file"""
        filetypes = (
            ('png', '*.png'),
            ('All files', '*.*')
        )

        filenames = filedialog.askopenfilenames(
            title='Open file',
            initialdir='/',
            filetypes=filetypes
        )

        self.save(filenames, "png")
 
    def save(self, filenames, filetype):
        """Save file to the database"""
        for file in list(filenames):
            with open(file, "rb") as input_file:
                ablob = input_file.read()
                try:
                    self.db.execute("INSERT INTO files (filename, filetype, file) VALUES(?, ?, ?)", Path(file).name, filetype, ablob)
                except:
                    mb.showerror('Error!', "Couldn't add file")

        self.display_records()

    def delete(self):
        """Delete file from database"""
        if not self.tree.selection():
            mb.showerror('Error!', 'Please select a file to delete')
            return
       
        row = self.tree.focus()
        temp = self.tree.item(row, 'values')
        id  = int(temp[0])
        try:
            self.db.execute("DELETE FROM files WHERE id = ?", id)
            mb.showinfo('File deleted', "File was successfully deleted")
            self.display_records()
        except:
            mb.showerror('Error!', "Couldn't delete file")
    
    def view(self):
        """View a file from the database"""
        if not self.tree.selection():
            mb.showerror('Error!', 'Please select a file to view')
            return
        
        row = self.tree.focus()
        temp = self.tree.item(row, 'values')
        id  = int(temp[0])

        file = self.db.execute("SELECT filename, filetype, file FROM files WHERE id = ?", id)
        with open(f"output\output.{file[0]['filetype']}", "wb") as output_file:
            output_file.write(file[0]["file"])
        os.system(f"output\output.{file[0]['filetype']}")
        """try:
            file = self.db.execute("SELECT filetype, file FROM files WHERE id = ?", id)
            with open(f"ouput\{file[0]['filename']}.{file[0]['filetype']}", "wb") as output_file:
                    output_file.write(file[0]["file"])
            os.system(f"ouput\{file[0]['filename']}.{file[0]['filetype']}")
        except:
            mb.showerror('Error!', "Couldn't retrieve file")"""
        

    def display_records(self):
        """Display files in the database"""
        self.tree.delete(*self.tree.get_children())
        records = self.db.execute("SELECT id, filename, filetype , time FROM files")
        for record in reversed(records):
            record = tuple(record.values())
            self.tree.insert('', END, values=record)