import tkinter as tk
from tkinter import ttk

def select_cell_by_value(tree, column_index, target_value):
    for child_id in tree.get_children():
        item_values = tree.item(child_id, 'values')
        print(item_values)
        if item_values and len(item_values) > column_index and item_values[column_index] == target_value:
            tree.selection_set(child_id)
            return

# Example data
data = [
    ('Item 1', 'Value 1', 'Description 1'),
    ('Item 2', 'Value 2', 'Description 2'),
    ('Item 3', 'Value 3', 'Description 3'),
]

# Create the main window
root = tk.Tk()
root.title("Treeview with Cell Selection")

# Create a Treeview widget
columns = ('Column 1', 'Column 2', 'Column 3')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Set up column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Populate the Treeview
for item in data:
    tree.insert('', tk.END, values=item)

# Select the cell with the value 'Value 2' in the second column (index 1)
select_cell_by_value(tree, 1, 'Value 2')

# Pack the Treeview
tree.pack(expand=tk.YES, fill=tk.BOTH)

# Run the Tkinter event loop
root.mainloop()
