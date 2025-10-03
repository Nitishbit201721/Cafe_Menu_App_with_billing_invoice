from customtkinter import*
from PIL import Image, ImageTk


root = CTk()
root.geometry("930x478")
root.title("Employee Management System")
image=CTkImage(Image.open('employee.png'),size=(930, 478))
imagelabel = CTkLabel(root, image=image , text="")
imagelabel.place(x=0, y=0)

def add_employee():
    print("Add Employee button clicked")


root.mainloop()