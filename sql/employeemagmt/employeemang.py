from PIL import Image, ImageTk

from customtkinter import*

root = CTk()
root.geometry("930x478")
root.title("Employee Management System")
# image=CTkImage(Image.open('Screenshot 2025-07-29 163605.png'),size=(930, 478))
# imagelabel = CTkLabel(root, image=image , text="")
# imagelabel.place(x=0, y=0)

def add_employee():
    print("Add Employee button clicked")


root.mainloop()