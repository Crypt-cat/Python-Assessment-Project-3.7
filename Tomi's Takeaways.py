from tkinter import *
from tkinter import messagebox

# class MenuItem:
#    def __init__(self, item_name, item_description, item_price)

class OrderingSystem:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Tomi's Takeaways")

        self.order_list = []

        self.start_frame = Frame(parent)
        self.start_frame.grid()

        Button(self.start_frame, text="Food Menu", command=self.show_food_menu)
        Button(self.start_frame, text="Combo Menu", command=self.show_combo_menu)
    
    def show_food_menu(self):

    
    def show_combo_menu(self):

if __name__ == "__main__":
    root = Tk()
    gui = OrderingSystem(root)
    root.mainloop()