import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import ttk, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define color codes for UI design
green_color = "#299617"  # Green color for buttons and frames
blue_color = "#6c8aa6"   # Blue color, unused in the current version
grey_color = "#a6a6a6"   # Grey color for listbox backgrounds
white_color = "#Ffffff"  # White color for listbox text

# Initialize the main application window
root = tk.Tk()
root.title("BudgetBuddy")
root.geometry("1200x800")

# Function to close the application
def close_app():
    """Closes the application window."""
    root.destroy()

# Configure the main window's grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a canvas and a scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas,style="TFrame")

# Setup the canvas for scrolling
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Position the frame inside the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Place the canvas and scrollbar in the window
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Initialize lists to store expense and income data
expenses = []  # List for storing expenses as (label, amount) tuples
incomes = []   # List for storing incomes as (label, amount) tuples

# Function to add an expense to the list
def add_expense():
    """Adds a new expense entry to the expenses list after validation."""
    expense_amount = expense_amount_entry.get()
    expense_label = expense_label_entry.get()

    # Validate input before adding
    if not expense_amount.replace('.', '', 1).isdigit() or not expense_label:
        messagebox.showerror("Invalid Input", "Please enter a valid amount and label for the expense.")
        return

    expenses.append((expense_label, expense_amount))
    expense_label_entry.delete(0, tk.END)
    expense_amount_entry.delete(0, tk.END)
    update_lists()
    update_graph()

# Function to add an income to the list
def add_income():
    """Adds a new income entry to the incomes list after validation."""
    income_amount = income_amount_entry.get()
    income_label = income_label_entry.get()

    # Validate input before adding
    if not income_amount.replace('.', '', 1).isdigit() or not income_label:
        messagebox.showerror("Invalid Input", "Please enter a valid amount and label for the income.")
        return
    
    incomes.append((income_label, income_amount))
    income_label_entry.delete(0, tk.END)
    income_amount_entry.delete(0, tk.END)
    update_lists()
    update_graph()

# Function to remove selected items from expenses and incomes
def remove_selected():
    """Removes selected items from the expense and income lists."""
    for idx in reversed(expenses_listbox.curselection()):
        expenses.pop(idx)
    for idx in reversed(incomes_listbox.curselection()):
        incomes.pop(idx)
    update_lists()
    update_graph()

# Function to update the lists displayed on the GUI
def update_lists():
    """Updates the contents of the expenses and incomes listboxes."""
    expenses_listbox.delete(0, tk.END)
    incomes_listbox.delete(0, tk.END)
    for label, amount in expenses:
        expenses_listbox.insert(tk.END, f"{label}: {amount}")
    for label, amount in incomes:
        incomes_listbox.insert(tk.END, f"{label}: {amount}")

# Functions for calculating total income and expenses
def calculate_total_income():
    """Calculates and returns the total income."""
    return sum(float(amount) for label, amount in incomes)

def calculate_total_expenses():
    """Calculates and returns the total expenses."""
    return sum(float(amount) for label, amount in expenses)

# Initialize global variables for the matplotlib figure and canvas
global fig, ax, canvas_widget
fig, ax = plt.subplots(1, 2, figsize=(10, 5))  # Matplotlib figure for the plots
# Create a canvas for the matplotlib figure
canvas_widget = FigureCanvasTkAgg(fig)

# Function to update and redraw the budget graphs
def update_graph():
    """Updates and redraws the budget graphs based on current expense and income data."""
    global canvas_widget

    # Clear previous figures
    ax[0].clear()
    ax[1].clear()

    # Prepare data for expense and income charts
    expense_labels = [label for label, amount in expenses]
    expense_amounts = [float(amount) for label, amount in expenses]
    total_income = calculate_total_income()
    total_expenses = calculate_total_expenses()
    income_unused = max(total_income - total_expenses, 0)

    # Plotting the expense chart
    if expense_amounts:
        ax[0].pie(expense_amounts, labels=expense_labels, autopct='%1.1f%%', startangle=140)
        ax[0].set_title('Expense Distribution')
    else:
        ax[0].text(0.5, 0.5, 'No Expense Data', horizontalalignment='center', verticalalignment='center')

    # Plotting the income chart
    income_labels = ['Income Used', 'Income Unused']
    income_amounts = [total_expenses, income_unused]
    ax[1].pie(income_amounts, labels=income_labels, autopct='%1.1f%%', startangle=140, colors=['red', 'green'])
    ax[1].set_title('Income Usage')

    # Draw the updated plots
    plot_graphs()
    canvas_widget.draw()

# Function to open a new window displaying the budget graphs
def open_graph_window():
    """Opens a new window displaying the budget graphs."""
    global fig, ax

    # Create and configure the graph window
    graph_window = tk.Toplevel(root)
    graph_window.title("Budget Graphs")
    graph_window.geometry("600x600")

    # Create a canvas widget for the new window and add the print button
    new_canvas_widget = FigureCanvasTkAgg(fig, master=graph_window)
    new_canvas_widget_widget = new_canvas_widget.get_tk_widget()
    new_canvas_widget_widget.pack(fill=tk.BOTH, expand=True)

    print_button = ttk.Button(graph_window, text="Print Graph", command=print_graph)
    print_button.pack(pady=10)

    plot_graphs()
    new_canvas_widget.draw()

# Function to handle the printing of the graph
def print_graph():
    """Handles the printing of the graph."""
    try:
        # Save the figure to a temporary file
        temp_file = "temp_graph.png"
        fig.savefig(temp_file)

        # Implement platform-specific print command
        if os.name == 'nt':  # Windows
            os.startfile(temp_file, "print")
        else:  # macOS, Linux, and others
            print_command = f"lpr {temp_file}"
            os.system(print_command)

        messagebox.showinfo("Print Graph", "Graph sent to the printer.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to draw the plots on the graph
def plot_graphs():
    """Draws the plots on the graph based on the expense and income data."""
    global fig, ax, expenses, incomes

    # Clear the previous figures
    ax[0].clear()
    ax[1].clear()

    # Data for expense chart
    expense_labels = [label for label, amount in expenses]
    expense_amounts = [float(amount) for label, amount in expenses]

    # Data for income chart
    total_income = calculate_total_income()
    total_expenses = calculate_total_expenses()
    income_unused = max(total_income - total_expenses, 0)

    # Plotting the expense chart
    if expense_amounts:
        ax[0].pie(expense_amounts, labels=expense_labels, autopct='%1.1f%%', startangle=140)
        ax[0].set_title('Expense Distribution')
    else:
        ax[0].text(0.5, 0.5, 'No Expense Data', horizontalalignment='center', verticalalignment='center')

    # Plotting the income chart
    income_labels = ['Income Used', 'Income Unused']
    income_amounts = [total_expenses, income_unused]
    ax[1].pie(income_amounts, labels=income_labels, autopct='%1.1f%%', startangle=140, colors=['red', 'green'])
    ax[1].set_title('Income Usage')

# Load and configure the logo image
logo_image = PhotoImage(file='C:\\Users\\david\\OneDrive\\Desktop\\BudgetBuddy\\BudgetApp\\BBLogo.png')

logo_label = ttk.Label(scrollable_frame, image=logo_image)
logo_label.image = logo_image
logo_label.grid(row=0, column=2, padx=50, pady=10)

# Labels for expense label and amount entries

expense_label_label = ttk.Label(scrollable_frame, text="Expense Label:")
expense_label_label.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

expense_amount_label = ttk.Label(scrollable_frame, text="Expense Amount:")
expense_amount_label.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# Entry fields for expense labels and amounts
expense_label_entry = ttk.Entry(scrollable_frame)
expense_label_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

expense_amount_entry = ttk.Entry(scrollable_frame)
expense_amount_entry.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

# Labels for income label and amount entries
income_label_label = ttk.Label(scrollable_frame, text="Income Label:")
income_label_label.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

income_amount_label = ttk.Label(scrollable_frame, text="Income Amount:")
income_amount_label.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# Entry fields for income labels and amounts
income_label_entry = ttk.Entry(scrollable_frame)
income_label_entry.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

income_amount_entry = ttk.Entry(scrollable_frame)
income_amount_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

style = ttk.Style()
style.configure("TButton", background=green_color)
style.configure("TFrame", background=green_color)
# Buttons to add expenses, incomes, and remove selected items
expense_button = ttk.Button(scrollable_frame, text="Add Expense", command=add_expense)
income_button = ttk.Button(scrollable_frame, text="Add Income", command=add_income)
remove_button = ttk.Button(scrollable_frame, text="Remove Selected", command=remove_selected)
expense_button.grid(row=5, column=1, columnspan=2, pady=10, sticky="ew")
expense_button.configure(style="TButton")
income_button.grid(row=6, column=1, columnspan=2, pady=10, sticky="ew")
remove_button.grid(row=7, column=1, columnspan=2, pady=10, sticky="ew")

# Listboxes to display expenses and incomes
expenses_listbox = tk.Listbox(scrollable_frame, height=10, width=40, selectmode=tk.MULTIPLE)
incomes_listbox = tk.Listbox(scrollable_frame, height=10, width=40, selectmode=tk.MULTIPLE)
expenses_listbox.grid(row=8, column=1, columnspan=2, pady=10, sticky="ew")
incomes_listbox.grid(row=9, column=1, columnspan=2, pady=10, sticky="ew")
expenses_listbox.configure(bg=grey_color, fg=white_color)
incomes_listbox.configure(bg=grey_color, fg=white_color)

# Button to open the graph window
graph_button = ttk.Button(scrollable_frame, text="Budget Graph", command=open_graph_window)
graph_button.grid(row=13, column=1, columnspan=2, pady=10, sticky="ew")

# Button to exit program
exit_button = ttk.Button(scrollable_frame, text="Exit", command=close_app)
exit_button.grid(row=14, column=1, columnspan=2, pady=10, sticky="ew")
exit_button.configure(style="TButton")


# Run the application
root.mainloop()
