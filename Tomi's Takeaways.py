from tkinter import *
from tkinter import messagebox

# class MenuItem:
#    def __init__(self, item_name, item_description, item_price)

class OrderingSystem:
    def __init__(self, parent):
        self.order_list = []

        self.start_frame = Frame(parent)
        self.start_frame.grid()

        Button(self.start_frame, text="Food Menu", font=("TKDefault", 30, "bold"), command=self.show_food_menu).grid(columnspan=2, sticky="nesw")
        Button(self.start_frame, text="Combo Menu", font=("TKDefault", 30, "bold"), command=self.show_combo_menu).grid(columnspan=2, sticky="nesw")

        self.food_menu = Frame(parent)
        Label(self.food_menu, text="Featured Items").grid()


        self.combo_menu = Frame(parent)

    
    def show_food_menu(self):
        self.start_frame.grid_forget()
        self.food_menu.grid()

    
    def show_combo_menu(self):
        self.start_frame.grid_forget()
        self.combo_menu.grid()


if __name__ == "__main__":
    root = Tk()
    root.title("Tomi's Takeaways")
    screen_middle = (root.winfo_screenwidth() / 2) - 250
    root.geometry(f"500x{root.winfo_screenheight()}+{int(screen_middle)}+0")
    root.resizable(False, False)
    gui = OrderingSystem(root)
    root.mainloop() 