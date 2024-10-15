#print("Hello, 123!")


import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect('text_storage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save text to the database
def save_text():
    text_to_save = text_field.get("1.0", tk.END).strip()  # Get text from the text field
    if text_to_save:
        conn = sqlite3.connect('text_storage.db')
        cursor = conn.cursor()
        
        # Delete the old text and save the new one (only one row will be in the table)
        cursor.execute("DELETE FROM texts")
        cursor.execute("INSERT INTO texts (content) VALUES (?)", (text_to_save,))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Text saved successfully!")
    else:
        messagebox.showwarning("Warning", "Text field is empty!")

# Load text from the database
def load_text():
    conn = sqlite3.connect('text_storage.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT content FROM texts LIMIT 1")
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        text_field.delete("1.0", tk.END)  # Clear the text field
        text_field.insert(tk.END, result[0])  # Insert the loaded text
        messagebox.showinfo("Success", "Text loaded successfully!")
    else:
        messagebox.showwarning("Warning", "No text found in the database!")

# GUI setup
root = tk.Tk()
root.title("Text Saver and Loader")

# Text field
text_field = tk.Text(root, height=10, width=40)
text_field.pack(pady=10)

# Save button
save_button = tk.Button(root, text="Save", command=save_text)
save_button.pack(pady=5)

# Load button
load_button = tk.Button(root, text="Load", command=load_text)
load_button.pack(pady=5)

# Initialize the database
setup_database()

# Run the application
root.mainloop()
