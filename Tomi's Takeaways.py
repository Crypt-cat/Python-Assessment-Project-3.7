from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *


class MenuItem:
    def __init__(self, item_name, item_description, item_price):
        self.item_name = item_name
        self.item_description = item_description
        self.item_price = item_price


class OrderingSystem:
    def __init__(self, parent):
        self.total_cost = 0

        self.menu_data = [
            MenuItem("Classic Burger", "100% pure beef patty with onion", 4.50),
            MenuItem("Cheese Burger", "Beef patty with delicious cheddar", 5.50),
            MenuItem("Deluxe Burger", "Beef patty with tomato, lettuce, and cheese", 9.00),
            MenuItem("Chicken Nuggets", "Tender, juicy 6 piece chicken nuggets", 6.00),
            MenuItem("Fries", "Salted fries from premium potatoes", 4.00),
            MenuItem("Sundae", "Soft vanilla with chocolate drizzle", 5.00),
            MenuItem("Coke", "Refreshing Coca-cola", 3.50),
            MenuItem("Sprite", "Fresh and classic Sprite", 3.50)
        ]

        self.start_frame = Frame(parent)
        self.start_frame.grid()

        Button(self.start_frame, text="Food Menu", font=("TKDefault", 50, "bold"), command=self.show_food_menu).grid(row=0, padx=165, pady=30, sticky="nesw")

        self.food_menu = Frame(parent)

        Label(self.food_menu, text="Featured Items", font=("TKDefault", 30, "bold")).grid(row=0, column=1, columnspan=2)
        self.cost_label = Label(self.food_menu, text=f"Total cost: ${self.total_cost}", font=("TKDefault", 15, "bold"))
        self.cost_label.grid(row=15, column=1, columnspan=2, pady=(50, 0))
        Button(self.food_menu, text="Back to start", font=("TKDefault", 30, "bold"), command=self.show_start).grid(row=16, column=1, columnspan=2, pady=(50, 0))
        Label(self.food_menu, text="This will reset your order!", font=("TKDefault", 11, "italic")).grid(row=17, column=1, columnspan=2)

        self.quantity_entries = []

        current_index = 0 
        for item in self.menu_data:
            if current_index < 2:
                col = 0
                start_row = (current_index * 6) + 1
            elif current_index < 4:
                col = 1
                start_row = ((current_index - 2) * 6) + 1
            elif current_index < 6:
                col = 2
                start_row = ((current_index - 4) * 6) + 1
            else:
                col = 3
                start_row = ((current_index - 6) * 6) + 1
            
            Label(self.food_menu, text=item.item_name, font=("TKDefault", 11, "bold")).grid(row=start_row, column=col, pady=(30, 0))
            Label(self.food_menu, text=item.item_description, font=("TKDefault", 8)).grid(row=start_row + 1, column=col)
            Label(self.food_menu, text=f"${item.item_price:.2f}", font=("TKDefault", 9, "italic")).grid(row=start_row + 2, column=col)

            Label(self.food_menu, text="Quantity you want to order:", font=("TKDefault", 8)).grid(row=start_row + 3, column=col)
            quantity_entry = Entry(self.food_menu, width=5)
            quantity_entry.insert(0, "1")
            quantity_entry.grid(row=start_row + 4, column=col)
            self.quantity_entries.append(quantity_entry)

            Button(self.food_menu, text=f"Add {item.item_name}", command=lambda i=item, index=current_index: self.add_to_order(i, index)).grid(row=start_row + 5, column=col)

            current_index += 1

        Label(self.food_menu, text="Your Order:", font=("TKDefault", 12, "bold")).grid(row=13, column=1, columnspan=2, pady=(20,0))
        self.receipt = ScrolledText(self.food_menu, width=45, height=8, state="disabled")
        self.receipt.grid(row=14, column=1, columnspan=2)

        self.quantity_entries[0].focus_set()

    
    def add_to_order(self, item, index):
        current_entry = self.quantity_entries[index]
        user_input = current_entry.get()
    
        if not user_input.isdigit() or int(user_input) <= 0:
            messagebox.showerror("Error", "Please only enter positive whole numbers.")
            current_entry.focus_set()
            current_entry.delete(0, END)
            current_entry.insert(0, "1")
            current_entry.focus_force()
            return 
        
        if int(user_input) > 99:
            messagebox.showwarning("Warning", "Please keep quantity at once under 100.")
            current_entry.focus_set()
            current_entry.delete(0, END)
            current_entry.insert(0, "1")
            current_entry.focus_force()
            return

        quantity = int(user_input)
        cost = item.item_price * quantity
    
        self.total_cost += cost
        self.cost_label.config(text=f"Total cost: ${self.total_cost}")

        self.receipt.config(state="normal")
        self.receipt.insert(END, f"{quantity}x {item.item_name}: ${cost:.2f}\n")
        self.receipt.config(state="disabled")
        self.receipt.see(END)


    def show_food_menu(self):
        self.start_frame.grid_forget()
        self.food_menu.grid()
        root.update_idletasks()
        self.quantity_entries[0].focus_set()


    def show_start(self):
        self.order_list = []

        self.receipt.configure(state="normal")
        self.receipt.delete(1.0, END)
        self.receipt.configure(state="disabled")
    
        for entry in self.quantity_entries:
            entry.delete(0, END)
            entry.insert(0, "1")

        self.total_cost = 0
        self.cost_label.config(text=f"Total cost: ${self.total_cost}")

        self.food_menu.grid_forget()
        self.start_frame.grid()
        root.update_idletasks()


if __name__ == "__main__":
    root = Tk()
    root.title("Tomi's Takeaways")
    screen_middle = (root.winfo_screenwidth() / 2) - 310  # comment
    root.geometry(f"620x{root.winfo_screenheight()}+{int(screen_middle)}+0")  # comment
    root.update_idletasks()  # comment resizing was broken
    root.resizable(False, False)  # comment
    gui = OrderingSystem(root)
    root.mainloop() 