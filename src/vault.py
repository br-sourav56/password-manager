import re
from tkinter import Toplevel, Label, Entry, Button, StringVar
from Database.database import init_database


class VaultMethods:

    def __init__(self):
        self.db, self.cursor = init_database()

    def validate_password(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$"
        return bool(re.match(pattern, password))

    def add_password(self, vault_screen):
        # Create a new form window
        form = Toplevel()
        form.title("Add New Password")
        form.geometry("420x250")

        # Labels and Entry fields
        Label(form, text="Website:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        website_entry = Entry(form, width=30)
        website_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(form, text="Username/Email:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        userid_entry = Entry(form, width=30)
        userid_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(form, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        password_entry = Entry(form, width=30, show="*") 
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Error message label
        error_msg = StringVar()
        error_label = Label(form, textvariable=error_msg, fg="red", font=("Arial", 8))
        error_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Function to handle saving the password
        def save_password():
            website = website_entry.get().strip()
            userid = userid_entry.get().strip()
            password = password_entry.get().strip()

            if website and userid and password: 
                if not self.validate_password(password):
                    # Show error message under the password field
                    error_msg.set(
                        "Password must be at least 8 characters long\ncontain an uppercase letter, a lowercase letter\nand a special character.")
                    return
                else:
                    error_msg.set("")  # Clear error message if password is valid

                try:
                    # Insert the data into the database
                    insert_cmd = """INSERT INTO vault(website, userid, password) VALUES (?, ?, ?)"""
                    self.cursor.execute(insert_cmd, (website, userid, password))
                    self.db.commit()

                    # Notify user and refresh UI
                    error_msg.set("")  
                    vault_screen()  
                    form.destroy()  
                except Exception as e:
                    error_msg.set(f"An error occurred: {e}")
            else:
                error_msg.set("All fields are required.")

        # Buttons for Save and Cancel
        Button(form, text="Save", command=save_password).grid(row=4, column=1, columnspan=2, pady=10)
        Button(form, text="Cancel", command=form.destroy).grid(row=5, column=1, columnspan=2, pady=5)

    def update_password(self, id, vault_screen):
        # Create a form window to update the password
        form = Toplevel()
        form.title("Update Password")
        form.geometry("350x200")

        Label(form, text="New Password:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        password_entry = Entry(form, width=30, show="*")
        password_entry.grid(row=0, column=1, padx=10, pady=5)

        # Error message label
        error_msg = StringVar()
        error_label = Label(form, textvariable=error_msg, fg="red", font=("Arial", 8))
        error_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Function to handle updating the password
        def save_updated_password():
            password = password_entry.get().strip()

            if password:
                if not self.validate_password(password):
                    # Show error message under the password field
                    error_msg.set(
                        "Password must be at least 8 characters long\ncontain an uppercase letter, a lowercase letter\nand a special character."
                    )
                    return
                else:
                    error_msg.set("")  # Clear error message if password is valid

                try:
                    # Update the password in the database
                    self.cursor.execute("UPDATE vault SET password = ? WHERE id = ?", (password, id))
                    self.db.commit()

                    # Notify user and refresh UI
                    error_msg.set("") 
                    vault_screen()  
                    form.destroy()  
                except Exception as e:
                    error_msg.set(f"An error occurred: {e}")
            else:
                error_msg.set("Password field cannot be empty.")

        # Buttons for Save and Cancel
        Button(form, text="Save", command=save_updated_password).grid(row=2, column=1, columnspan=2, pady=10)
        Button(form, text="Cancel", command=form.destroy).grid(row=3, column=1, columnspan=2, pady=5)

    def remove_password(self, id, vault_screen):
        # Delete the password entry from the database
        try:
            self.cursor.execute("DELETE FROM vault WHERE id = ?", (id,))
            self.db.commit()

            # Notify user and refresh UI
            vault_screen()  
        except Exception as e:
            print(f"Error: {e}")
