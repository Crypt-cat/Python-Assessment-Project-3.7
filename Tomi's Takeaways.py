from tkinter import *
from tkinter import messagebox

class MenuItem:
    def __init__(self, item_name, item_description, item_price, item_image);
        self.item_name = item_name
        self.item_description = item_description
        self.item_price = item_price
        self.item_image = item_image

        menu_data = [
            MenuItem("Classic Burger", "100% pure beef patty with onion", 4.50, "Burger.png"),
            MenuItem("Cheese Burger", "Classic burger with delicious cheddar", 5.50, "CheeseBurger.png"),
            MenuItem("Deluxe Burger", "100% pure beef patty with tomato, lettuce, and cheese", 9.00, "DeluxeBurger.png"),
            MenuItem("Chicken Nuggets", "Tender, juicy 6 piece chicken nuggets", 6.00, "Nuggets.png"),
            MenuItem("Fries", "Salted fries made with premium potatoes", 4.00, "Fries.png"),
            MenuItem("Sundae", "Soft vanilla with chocolate drizzle", 5.00, "Sundae.png"),
            MenuItem("Coke", "Refreshing, classic Coca-cola", 3.50, "Coke.png"),
            MenuItem("Sprite", "Fresh and clean Sprite", 3.50, "Sprite.png")
        ]

class OrderingSystem:
    def __init__(self, parent):
        self.order_list = []

        self.start_frame = Frame(parent)
        self.start_frame.grid()

        Button(self.start_frame, text="Food Menu", font=("TKDefault", 30, "bold"), command=self.show_food_menu).grid(row=1, padx=140, pady=150, sticky="nesw")
        Button(self.start_frame, text="Combo Menu", font=("TKDefault", 30, "bold"), command=self.show_combo_menu).grid(row=2, padx=140, pady=150, sticky="nesw")

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
    screen_middle = (root.winfo_screenwidth() / 2) - 250  # comment
    root.geometry(f"500x{root.winfo_screenheight()}+{int(screen_middle)}+0")  # comment
    root.update_idletasks()  # comment resizing was broken
    root.resizable(False, False)  # comment
    gui = OrderingSystem(root)
    root.mainloop() 