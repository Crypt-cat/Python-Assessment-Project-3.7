from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *


# Support class to store data for menu items
class MenuItem:
    """Represents a single food item on the menu."""

    def __init__(self, item_name, item_description, item_price):
        """Initialize a new MenuItem instance."""
        self.item_name = item_name
        self.item_description = item_description
        self.item_price = item_price


class OrderingSystem:
    """Main class for Tomi's Takeaways ordering system."""

    def __init__(self, parent):
        """Initialize the frames, data, widgets, etc."""
        self.total_cost = 0
        self.order_history = []  # Tracks costs of added items for the delete function

        # Data list containing all available menu items
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

        # Start frame setup
        self.start_frame = Frame(parent)
        self.start_frame.grid()

        Label(self.start_frame, text="Welcome to Tomi's Takeaways!", font=("TKDefault", 50, "bold"), wraplength=400).grid(row=0, padx=165, pady=30)
        Button(self.start_frame, text="Food Menu", font=("TKDefault", 50, "bold"), command=self.show_food_menu).grid(row=1, padx=165, pady=30)
        Button(self.start_frame, text="Exit", font=("TKDefault", 50, "bold"), command=exit).grid(row=2, padx=165, pady=30)

        # Menu frame setup
        self.food_menu = Frame(parent)

        Label(self.food_menu, text="Featured Items", font=("TKDefault", 30, "bold")).grid(row=0, column=1, columnspan=2)

        # Labels for cost and delivery info
        self.cost_label = Label(self.food_menu, text=f"Total cost: ${self.total_cost}", font=("TKDefault", 15, "bold"))
        self.cost_label.grid(row=16, column=1, columnspan=2, pady=(30, 0))
        Label(self.food_menu, text="Delivery fees apply (+$5.00). Free delivery for orders $20 or over!", font=("TKDefault", 11, "italic")).grid(row=17, column=1, columnspan=2)

        # Name entry section
        Label(self.food_menu, text="Please enter your name:", font=("TKDefault", 10, "bold")).grid(row=18, column=1, columnspan=2, pady=(30, 0))
        self.name_entry = Entry(self.food_menu)
        self.name_entry.grid(row=19, column=1, columnspan=2)
        Button(self.food_menu, text="Confirm Order", font=("TKDefault", 15, "bold"), command=self.confirm_order).grid(row=20, column=1, columnspan=2)

        # Navigation buttons
        Button(self.food_menu, text="Back to start", font=("TKDefault", 30, "bold"), command=self.show_start).grid(row=21, column=1, columnspan=2, pady=(30, 0))
        Label(self.food_menu, text="This will reset your order!", font=("TKDefault", 11, "italic")).grid(row=22, column=1, columnspan=2)

        self.quantity_entries = []  # Stores entry widgets to access user quantities

        # Loop through menu_data to dynamically create the format for each food item
        current_index = 0
        for item in self.menu_data:
            # The logic to arrange items in a 4 column grid
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

            Label(self.food_menu, text="Order Quantity:", font=("TKDefault", 8)).grid(row=start_row + 3, column=col)
            quantity_entry = Entry(self.food_menu, width=5)
            quantity_entry.insert(0, "1")
            quantity_entry.grid(row=start_row + 4, column=col)
            self.quantity_entries.append(quantity_entry)

            # Lambda used to pass the specific item and index to the function
            Button(self.food_menu, text=f"Add {item.item_name}", command=lambda i=item, index=current_index: self.add_to_order(i, index)).grid(row=start_row + 5, column=col)

            current_index += 1

        # Order receipt display
        Label(self.food_menu, text="Your Order:", font=("TKDefault", 12, "bold")).grid(row=13, column=1, columnspan=2, pady=(20, 0))
        self.receipt = ScrolledText(self.food_menu, width=45, height=8, state="disabled")
        self.receipt.grid(row=14, column=1, columnspan=2)
        Button(self.food_menu, text="Delete latest item", font=("TKDefault", 15, "bold"), command=self.delete_last).grid(row=15, column=1, columnspan=2)

        # Initialize focus and tracking for the last active entry box
        self.quantity_entries[0].focus_set()
        self.current_entry = self.quantity_entries[0]

        # Checkout frame setup
        self.checkout_frame = Frame(parent)

        Label(self.checkout_frame, text=f"Hi, please finalize your order.", font=("TKDefault", 20, "bold")).grid(row=0, column=1, columnspan=2, padx=180)

        # Radiobuttons for delivery selection
        self.order_type = StringVar(value="Takeaway")
        Label(self.checkout_frame, text="How would you like to receive your food?", font=("TKDefault", 15, "bold")).grid(row=1, column=1, columnspan=2, pady=(30, 0))

        Radiobutton(self.checkout_frame, text="Takeaway (Free)", variable=self.order_type, value="Takeaway", command=self.update_final_total).grid(row=2, column=1, columnspan=2)
        Radiobutton(self.checkout_frame, text="Delivery (+$5.00 or Free if eligible)", variable=self.order_type, value="Delivery", command=self.update_final_total).grid(row=3, column=1, columnspan=2)

        self.final_total_label = Label(self.checkout_frame, text="", font=("TKDefault", 15, "bold"))
        self.final_total_label.grid(row=4, column=1, columnspan=2, pady=20)

        # Dropdown menu for optional subscription
        self.subscribe_choice = StringVar(value="No")
        Label(self.checkout_frame, text="Would you like to subscribe to our mail?", font=("TKDefault", 12, "bold")).grid(row=5, column=1, columnspan=2, pady=(20))
        self.subscription_dropdown = OptionMenu(self.checkout_frame, self.subscribe_choice, "Yes", "No")
        self.subscription_dropdown.grid(row=6, column=1, columnspan=2)

        Button(self.checkout_frame, text="Place Final Order", font=("TKDefault", 20, "bold"), command=self.complete_order).grid(row=7, column=1, columnspan=2, pady=20)

    def add_to_order(self, item, index):
        """Validate input, calculate cost, and update the receipt."""
        self.current_entry = self.quantity_entries[index]
        user_input = self.current_entry.get()

        # Check for non-numeric or zero inputs
        if not user_input.isdigit() or int(user_input) <= 0:
            messagebox.showwarning("Warning", "Please only enter positive whole numbers.")
            self.current_entry.delete(0, END)
            self.current_entry.insert(0, "1")
            self.current_entry.focus_force()  # Used to combat Mac glitch where the window is not in focus
            return

        # Check for excessive quantities
        if int(user_input) > 99:
            messagebox.showwarning("Warning", "Please keep quantity at once under 100.")
            self.current_entry.delete(0, END)
            self.current_entry.insert(0, "1")
            self.current_entry.focus_force()
            return

        quantity = int(user_input)
        cost = item.item_price * quantity

        # Update totals and labels
        self.order_history.append(cost)
        self.total_cost += cost
        self.cost_label.config(text=f"Total cost: ${self.total_cost:.2f}")

        # Update ScrolledText receipt
        self.receipt.config(state="normal")
        self.receipt.insert(END, f"{quantity}x {item.item_name}: ${cost:.2f}\n")
        self.receipt.config(state="disabled")
        self.receipt.see(END)

    def delete_last(self):
        """Remove the most recent item added to the order history and receipt."""
        if not self.order_history:
            messagebox.showwarning("Warning", "No items to delete!")
            self.current_entry.focus_force()
            return

        # Undo the last cost addition
        last_cost = self.order_history.pop()
        self.total_cost -= last_cost
        self.cost_label.config(text=f"Total cost: ${self.total_cost:.2f}")

        # Remove the last line of text in the receipt
        self.receipt.config(state="normal")
        self.receipt.delete("end-2l", "end-1l")
        self.receipt.config(state="disabled")

        # Reset quantity box to default
        self.current_entry.delete(0, END)
        self.current_entry.insert(0, "1")

    def show_food_menu(self):
        """Switch display from start screen to the food menu."""
        self.start_frame.grid_forget()
        self.food_menu.grid()
        root.update_idletasks()
        self.quantity_entries[0].focus_set()

    def show_start(self):
        """Reset all order data and returns to the initial start screen."""
        self.order_history = []

        # Reset radiobuttons and dropdown menu
        self.order_type.set("Takeaway")
        self.update_final_total()
        self.subscribe_choice.set("No")

        # Clear receipt
        self.receipt.configure(state="normal")
        self.receipt.delete(1.0, END)
        self.receipt.configure(state="disabled")

        # Reset all entry widgets
        for entry in self.quantity_entries:
            entry.delete(0, END)
            entry.insert(0, "1")
        self.name_entry.delete(0, END)

        self.total_cost = 0
        self.cost_label.config(text=f"Total cost: ${self.total_cost:.2f}")

        # Switch frames
        self.food_menu.grid_forget()
        self.checkout_frame.grid_forget()
        self.start_frame.grid()
        root.update_idletasks()

    def update_final_total(self):
        """Calculate delivery fees and updates the final checkout price label."""
        delivery_fee = 0.00

        # Apply free delivery if order is $20 or more
        if self.order_type.get() == "Delivery":
            if self.total_cost < 20:
                delivery_fee = 5.00
            else:
                delivery_fee = 0.00

        final_amount = self.total_cost + delivery_fee

        # Update text based on whether delivery is free, charged, or not selected
        if delivery_fee == 0.00 and self.order_type.get() == "Delivery":
            msg = f"Final Total: ${final_amount:.2f} (Free Delivery applied!)"
        elif delivery_fee > 0:
            msg = f"Final Total: ${final_amount:.2f} (Includes $5 delivery)"
        else:
            msg = f"Final Total: ${final_amount:.2f}"

        self.final_total_label.config(text=msg)

    def confirm_order(self):
        """Validate name and total cost before allowing user to proceed to checkout."""
        customer_name = self.name_entry.get().strip()

        # Checks if the user has not entered a name
        if customer_name == "":
            messagebox.showwarning("Missing Info", "Please enter a name!")
            self.name_entry.focus_force()
            return

        # Checks for non-alphabetic characters but allows spaces
        if not customer_name.replace(" ", "").isalpha():
            messagebox.showwarning("Invalid Name", "Names can only contain letters!")
            self.name_entry.delete(0, END)
            self.name_entry.focus_force()
            return

        # Checks if the user has ordered anything
        if self.total_cost == 0:
            messagebox.showwarning("Empty Order", "Please add items to your order first.")
            self.quantity_entries[0].focus_force()
            return

        # Switch to checkout frame
        self.food_menu.grid_forget()
        self.checkout_frame.grid()
        root.update_idletasks()
        self.update_final_total()

    def complete_order(self):
        """Finalize the order, show a thank you message, and reset the app."""
        customer_name = self.name_entry.get().strip()
        messagebox.showinfo("Order Placed", f"Thank you, {customer_name}! Your order has been sent to the kitchen.")

        self.checkout_frame.grid_forget()
        root.update_idletasks()
        self.show_start()


# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("Tomi's Takeaways")
    screen_middle = (root.winfo_screenwidth() / 2) - 310  # Logic to center the window horizontally on the screen
    root.geometry(f"620x{root.winfo_screenheight()}+{int(screen_middle)}+0")
    root.update_idletasks()  # Required to fix framing issues on Mac
    root.resizable(False, False)
    gui = OrderingSystem(root)
    root.mainloop()
