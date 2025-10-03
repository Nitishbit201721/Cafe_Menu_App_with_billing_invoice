import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# --- Menu Items ---
menu = {
    "Bruschetta": 6.50, "Mozzarella Sticks": 7.25, "Chicken Wings": 9.50, "Spring Rolls": 5.75,
    "Garlic Bread": 4.50, "Stuffed Mushrooms": 8.00, "Calamari Fritti": 9.25, "Nachos Supreme": 8.75,
    "Spinach Artichoke Dip": 7.50, "Shrimp Cocktail": 10.00, "Potato Skins": 6.75, "Hummus Platter": 6.25,
    "Fried Pickles": 5.50, "Cheese Platter": 12.00, "Onion Rings": 4.75, "Caesar Salad": 6.75,
    "Greek Salad": 7.00, "Cobb Salad": 8.50, "Caprese Salad": 7.25, "House Salad": 5.50,
    "Waldorf Salad": 7.75, "Spinach Salad": 6.50, "Kale Quinoa Salad": 8.00, "Arugula Pear Salad": 7.50,
    "Chef's Salad": 9.00, "Classic Cheeseburger": 8.99, "Bacon BBQ Burger": 10.50, "Veggie Burger": 8.25,
    "Grilled Chicken Sandwich": 9.00, "Philly Cheesesteak": 10.25, "BLT Sandwich": 7.50,
    "Turkey Club": 8.75, "Pulled Pork Sandwich": 9.25, "Fish Tacos": 10.00, "Portobello Mushroom Burger": 8.50,
    "Margherita Pizza": 12.50, "Pepperoni Pizza": 13.75, "Supreme Pizza": 15.00, "Veggie Pizza": 13.25,
    "Hawaiian Pizza": 14.00, "Buffalo Chicken Pizza": 14.50, "White Pizza": 13.00, "Spaghetti Carbonara": 14.25,
    "Fettuccine Alfredo": 13.50, "Penne Arrabbiata": 12.75, "Lasagna": 15.50, "Pesto Pasta": 13.25,
    "Seafood Linguine": 16.75, "Ravioli with Marinara": 14.00, "Grilled Salmon": 18.50,
    "Chicken Parmesan": 15.75, "Beef Stir-Fry": 14.50, "Roasted Lamb Chops": 22.00, "Pork Tenderloin": 16.25,
    "Vegetable Curry": 13.00, "Steak Ribeye": 24.00, "BBQ Ribs": 19.50, "Tofu Stir-Fry": 12.75,
    "Shrimp Scampi": 17.50, "French Fries": 3.50, "Sweet Potato Fries": 4.25, "Mashed Potatoes": 3.75,
    "Coleslaw": 2.75, "Steamed Broccoli": 3.25, "Garlic Mashed Cauliflower": 4.00, "Mac and Cheese": 4.50,
    "Sauteed Spinach": 3.50, "Roasted Veggies": 4.00, "Chocolate Lava Cake": 6.50, "New York Cheesecake": 6.00,
    "Tiramisu": 6.75, "Apple Pie": 5.50, "Creme Brulee": 6.25, "Ice Cream Sundae": 4.50, "Brownie": 4.00,
    "Key Lime Pie": 5.75, "Soda": 2.50, "Iced Tea": 2.75, "Lemonade": 3.00, "Coffee": 2.25,
    "Espresso": 3.50, "Bottled Water": 2.00, "Orange Juice": 3.25, "Milkshake": 4.75, "Smoothie": 5.00
}

# --- Categories ---
categories = {
    "Appetizers": ["Bruschetta", "Mozzarella Sticks", "Chicken Wings", "Spring Rolls", "Garlic Bread",
                   "Stuffed Mushrooms", "Calamari Fritti", "Nachos Supreme", "Spinach Artichoke Dip",
                   "Shrimp Cocktail", "Potato Skins", "Hummus Platter", "Fried Pickles", "Cheese Platter",
                   "Onion Rings"],
    "Salads": ["Caesar Salad", "Greek Salad", "Cobb Salad", "Caprese Salad", "House Salad",
               "Waldorf Salad", "Spinach Salad", "Kale Quinoa Salad", "Arugula Pear Salad", "Chef's Salad"],
    "Burgers and Sandwiches": ["Classic Cheeseburger", "Bacon BBQ Burger", "Veggie Burger",
                               "Grilled Chicken Sandwich", "Philly Cheesesteak", "BLT Sandwich",
                               "Turkey Club", "Pulled Pork Sandwich", "Fish Tacos", "Portobello Mushroom Burger"],
    "Pizzas": ["Margherita Pizza", "Pepperoni Pizza", "Supreme Pizza", "Veggie Pizza",
               "Hawaiian Pizza", "Buffalo Chicken Pizza", "White Pizza"],
    "Pastas": ["Spaghetti Carbonara", "Fettuccine Alfredo", "Penne Arrabbiata", "Lasagna",
               "Pesto Pasta", "Seafood Linguine", "Ravioli with Marinara"],
    "Entrees": ["Grilled Salmon", "Chicken Parmesan", "Beef Stir-Fry", "Roasted Lamb Chops",
                "Pork Tenderloin", "Vegetable Curry", "Steak Ribeye", "BBQ Ribs",
                "Tofu Stir-Fry", "Shrimp Scampi"],
    "Sides": ["French Fries", "Sweet Potato Fries", "Mashed Potatoes", "Coleslaw", "Steamed Broccoli",
              "Garlic Mashed Cauliflower", "Mac and Cheese", "Sauteed Spinach", "Roasted Veggies"],
    "Desserts": ["Chocolate Lava Cake", "New York Cheesecake", "Tiramisu", "Apple Pie",
                 "Creme Brulee", "Ice Cream Sundae", "Brownie", "Key Lime Pie"],
    "Beverages": ["Soda", "Iced Tea", "Lemonade", "Coffee", "Espresso", "Bottled Water",
                  "Orange Juice", "Milkshake", "Smoothie"]
}

# --- Main Application Class ---
class CafeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Café Menu & Billing")
        self.root.geometry("1000x700")  # Increased window size for better layout
        self.order = {}
        self.dark_mode = tk.BooleanVar()
        self.search_var = tk.StringVar()

        # Café Logo/Title
        self.logo_label = ttk.Label(root, text="Café Delight", font=("Georgia", 24, "bold"), foreground="#8B4513")  # SaddleBrown
        self.logo_label.pack(pady=10)

        # Search Bar & Dark Mode
        top_frame = ttk.Frame(root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(top_frame, text="Search:").pack(side=tk.LEFT)
        ttk.Entry(top_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Search", command=self.search_item).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(top_frame, text="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode).pack(side=tk.RIGHT)

        # Main content frame with two columns
        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Menu Frame (Left Column)
        self.menu_frame = ttk.Frame(self.content_frame)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.canvas = tk.Canvas(self.menu_frame)
        self.scrollbar = ttk.Scrollbar(self.menu_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.display_menu()

        # Order Display Frame (Right Column)
        self.order_display_frame = ttk.Frame(self.content_frame, relief=tk.GROOVE, borderwidth=2)
        self.order_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Create the current order label and text box
        ttk.Label(self.order_display_frame, text="Current Order", style="Category.TLabel").pack(pady=5)
        self.current_order_text = scrolledtext.ScrolledText(self.order_display_frame, height=15, width=40, state='disabled', font=("Courier", 10))
        self.current_order_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Order Control Buttons
        order_buttons_frame = ttk.Frame(self.order_display_frame)
        order_buttons_frame.pack(fill=tk.X, pady=5)
        ttk.Button(order_buttons_frame, text="Clear Order", command=self.clear_order).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(order_buttons_frame, text="Generate Invoice", command=self.generate_invoice).pack(side=tk.LEFT, expand=True, padx=5)

        # Quantity input for direct add if needed for more than 1 (though clicks are usually for 1)
        self.qty_frame = ttk.Frame(order_buttons_frame)
        self.qty_frame.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.qty_frame, text="Add Qty:").pack(side=tk.LEFT)
        self.qty_var = tk.StringVar(value="1")
        ttk.Entry(self.qty_frame, textvariable=self.qty_var, width=5).pack(side=tk.LEFT)

        # Set theme after all widgets are created
        self.set_theme()

        self.update_order_display()  # Initial update

    def set_theme(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Define default light mode colors
        light_bg = "#F8F8F8"  # Very light grey/off-white for a clean look
        light_text = "#333333"  # Dark grey for text
        light_category_text = "#005b96"  # Blue for categories
        light_button_bg = "#005b96"  # Blue for main buttons
        light_button_fg = "white"
        light_menu_item_bg = "#E0E0E0"  # Light grey for menu item buttons
        light_menu_item_fg = "#333333"

        self.root.config(bg=light_bg)
        style.configure("TFrame", background=light_bg)
        style.configure("TLabel", background=light_bg, foreground=light_text)
        style.configure("Category.TLabel", font=("Segoe UI", 12, "bold"), foreground=light_category_text)
        style.configure("TButton", background=light_button_bg, foreground=light_button_fg)
        style.map("TButton", background=[("active", "#003f63")])  # Darker blue on hover

        # Style for clickable menu items
        style.configure("MenuItem.TButton", background=light_menu_item_bg, foreground=light_menu_item_fg, font=("Segoe UI", 10))
        style.map("MenuItem.TButton", background=[("active", "#C0C0C0")])  # Darker grey on hover

        # Specific color for the logo label
        self.logo_label.config(background=light_bg, foreground="#8B4513")  # Ensure logo background matches root

        # Text widget colors
        self.current_order_text.config(bg="white", fg="black", insertbackground="black")

    def toggle_dark_mode(self):
        style = ttk.Style()
        if self.dark_mode.get():
            dark_bg = "#2E2E2E"  # Dark grey
            dark_text = "#FFFFFF"  # White text
            dark_category_text = "#6495ED"  # CornflowerBlue for categories
            dark_button_bg = "#4682B4"  # SteelBlue for main buttons
            dark_button_fg = "white"
            dark_menu_item_bg = "#444444"  # Darker grey for menu item buttons
            dark_menu_item_fg = "#FFFFFF"

            self.root.config(bg=dark_bg)
            style.configure("TFrame", background=dark_bg)
            style.configure("TLabel", background=dark_bg, foreground=dark_text)
            style.configure("Category.TLabel", foreground=dark_category_text)
            style.configure("TButton", background=dark_button_bg, foreground=dark_button_fg)
            style.map("TButton", background=[("active", "#36709E")])  # Darker steelblue on hover
            style.configure("MenuItem.TButton", background=dark_menu_item_bg, foreground=dark_menu_item_fg)
            style.map("MenuItem.TButton", background=[("active", "#555555")])  # Even darker grey on hover

            self.logo_label.config(background=dark_bg, foreground="#D2B48C")  # Tan for logo in dark mode
            self.current_order_text.config(bg="#444", fg="white", insertbackground="white")
        else:
            self.set_theme()  # Revert to light mode settings

    def display_menu(self):
        # Clear existing menu items before displaying
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for category, items in categories.items():
            ttk.Label(self.scrollable_frame, text=category, style="Category.TLabel").pack(anchor="w", pady=5)
            for item in items:
                # Create a button for each menu item, making it clickable
                item_button = ttk.Button(self.scrollable_frame,
                                         text=f"{item}: ${menu[item]:.2f}",
                                         command=lambda i=item: self.add_item_from_menu_click(i),
                                         style="MenuItem.TButton")
                item_button.pack(anchor="w", padx=10, fill=tk.X)

    def search_item(self):
        keyword = self.search_var.get().lower()
        # Clear current menu display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if keyword:
            found_items = {cat: [] for cat in categories}
            for cat, items in categories.items():
                for item in items:
                    if keyword in item.lower():
                        found_items[cat].append(item)
            
            displayed_any = False
            for category, items_in_cat in found_items.items():
                if items_in_cat:
                    ttk.Label(self.scrollable_frame, text=category, style="Category.TLabel").pack(anchor="w", pady=5)
                    for item in items_in_cat:
                        item_button = ttk.Button(self.scrollable_frame,
                                                 text=f"{item}: ${menu[item]:.2f}",
                                                 command=lambda i=item: self.add_item_from_menu_click(i),
                                                 style="MenuItem.TButton")
                        item_button.pack(anchor="w", padx=10, fill=tk.X)
                    displayed_any = True
            if not displayed_any:
                ttk.Label(self.scrollable_frame, text="No items found matching your search.", foreground="red").pack(pady=10)
        else:
            self.display_menu()  # Re-display full menu if search is cleared

    def add_item_from_menu_click(self, item_name):
        try:
            quantity_to_add = int(self.qty_var.get())
            if quantity_to_add <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a positive number.")
            return

        self.order[item_name] = self.order.get(item_name, 0) + quantity_to_add
        self.update_order_display()
        messagebox.showinfo("Item Added", f"Added {quantity_to_add} x {item_name} to order.")

    def update_order_display(self):
        self.current_order_text.config(state='normal')
        self.current_order_text.delete(1.0, tk.END)
        if not self.order:
            self.current_order_text.insert(tk.END, "Your order is empty.")
        else:
            order_summary = "--- Your Current Order ---\n"
            for item, qty in self.order.items():
                order_summary += f"{item} (x{qty}): ${menu[item] * qty:.2f}\n"
            self.current_order_text.insert(tk.END, order_summary)
        self.current_order_text.config(state='disabled')

    def clear_order(self):
        if messagebox.askyesno("Confirm", "Clear entire order?"):
            self.order.clear()
            self.update_order_display()
            messagebox.showinfo("Cleared", "Order cleared.")

    def generate_invoice(self):
        if not self.order:
            messagebox.showwarning("Warning", "Order is empty.")
            return

        invoice_win = tk.Toplevel(self.root)
        invoice_win.title("Invoice")
        invoice_win.geometry("600x400")
        if self.dark_mode.get():
            invoice_win.config(bg="#2e2e2e")

        text = scrolledtext.ScrolledText(invoice_win, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        if self.dark_mode.get():
            text.config(bg="#444", fg="white", insertbackground="white")

        invoice_text = self.generate_invoice_text()
        text.insert(tk.END, invoice_text)
        text.config(state="disabled")

        ttk.Button(invoice_win, text="Save Invoice", command=lambda: self.save_invoice(invoice_text)).pack(pady=5)

    def generate_invoice_text(self):
        subtotal = sum(menu[item] * qty for item, qty in self.order.items())
        tax = subtotal * 0.08
        total = subtotal + tax
        lines = [
            f"=== Café Invoice ===",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "----------------------------------------------",
            f"{'Item':<25}{'Qty':<5}{'Price':<8}{'Total'}",
            "-" * 50
        ]
        for item, qty in self.order.items():
            lines.append(f"{item:<25}{qty:<5}${menu[item]:<8.2f}${menu[item] * qty:.2f}")
        lines += [
            "-" * 50,
            f"{'Subtotal':<40}${subtotal:.2f}",
            f"{'Tax (8%)':<40}${tax:.2f}",
            f"{'Total':<40}${total:.2f}",
            "----------------------------------------------",
            "Thank you for dining with us!"
        ]
        return "\n".join(lines)

    def save_invoice(self, text):
        filename = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, "w") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Invoice saved as '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CafeApp(root)
    root.mainloop()