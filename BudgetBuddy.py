import tkinter as tk
from tkinter import ttk, messagebox


class NavigationBar(tk.Frame):
    def __init__(self, master, frame_classes):
        super().__init__(master)
        self.frame_classes = frame_classes
        self.create_widgets()

    def create_widgets(self):
        for frame_class in self.frame_classes:
            frame_name = frame_class.__name__
            button = ttk.Button(self, text=frame_name, command=lambda f=frame_class: self.master.switch_frame(f))
            button.pack(side='left')

class BudgetApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('BudgetBuddy')
        self.geometry('600x400')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#a4b0be')
        self.style.configure('TButton', background='#2f3542', foreground='#ffffff')
        self.style.configure('TLabel', background='#a4b0be', foreground='#2ed573')
        self.switch_frame(InputFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill='both', expand=True)

class InputFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.inputs = {'income': [], 'expenses': []}
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text='Income').grid(row=0, column=0, sticky='w')
        self.add_income_button = ttk.Button(self, text='+ Add Income', command=self.add_income_field)
        self.add_income_button.grid(row=0, column=1)

        ttk.Label(self, text='Expenses').grid(row=1, column=0, sticky='w')
        self.add_expense_button = ttk.Button(self, text='+ Add Expense', command=self.add_expense_field)
        self.add_expense_button.grid(row=1, column=1)

        self.submit_button = ttk.Button(self, text='Submit', command=self.submit_data)
        self.submit_button.grid(row=2, column=1, pady=10)

    def add_income_field(self):
        row = len(self.inputs['income']) + 2
        entry = ttk.Entry(self)
        entry.grid(row=row, column=0, sticky='ew')
        self.inputs['income'].append(entry)

    def add_expense_field(self):
        row = len(self.inputs['expenses']) + 3 + len(self.inputs['income'])
        entry = ttk.Entry(self)
        entry.grid(row=row, column=0, sticky='ew')
        self.inputs['expenses'].append(entry)

    def submit_data(self):
        income_data = [entry.get() for entry in self.inputs['income']]
        expenses_data = [entry.get() for entry in self.inputs['expenses']]
        messagebox.showinfo('Submitted', 'Your data has been submitted.')
        print('Income:', income_data)
        print('Expenses:', expenses_data)

class BudgetFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg='#80cbc4')
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Budget Summary", font=('Helvetica', 14, "bold"), background='#80cbc4', foreground='#004d40').pack(pady=10)

        self.total_income_label = ttk.Label(self, text="Total Income: $0.00", background='#80cbc4', foreground='#004d40')
        self.total_income_label.pack(pady=5)
        
        self.total_expenses_label = ttk.Label(self, text="Total Expenses: $0.00", background='#80cbc4', foreground='#004d40')
        self.total_expenses_label.pack(pady=5)
        
        self.budget_label = ttk.Label(self, text="Budget: $0.00", background='#80cbc4', foreground='#004d40')
        self.budget_label.pack(pady=5)

    def update_budget_summary(self, total_income, total_expenses, budget):
        self.total_income_label.config(text=f"Total Income: ${total_income:.2f}")
        self.total_expenses_label.config(text=f"Total Expenses: ${total_expenses:.2f}")
        self.budget_label.config(text=f"Budget: ${budget:.2f}")

class GraphFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg='white')
        self.create_widgets()

    def create_widgets(self):
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title("Budget Graph")
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

    def update_budget_graph(self, x_values, y_values):
        self.ax.clear()
        self.ax.plot(x_values, y_values, marker='o')
        self.ax.set_xlabel('Month')
        self.ax.set_ylabel('Budget ($)')
        self.ax.set_title("Budget Graph")
        self.canvas.draw()

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
