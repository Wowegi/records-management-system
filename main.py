from cs50 import SQL
from tkinter import *
import login

        
def main():
    
    # Initialize database
    db = SQL("sqlite:///files.db")
    
    window = Tk()
    login.Page(window, db)
    window.mainloop()

if __name__ == '__main__':
    main() 