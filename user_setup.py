"""
User Profile Setup Dialog
Shows on first run to collect user information
"""

import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

class UserSetupDialog:
    def __init__(self, root, data_file="data.json"):
        self.data_file = Path(data_file)
        self.root = root
        self.user_data = None
        
    def is_first_run(self):
        """Check if this is the first run (no user profile exists)"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return "user_profile" not in data
        return True
    
    def show_setup(self):
        """Show the setup dialog if first run"""
        if not self.is_first_run():
            return False
        
        # Create a new window
        setup_window = tk.Tk()
        setup_window.title("Welcome to MochiPet!")
        setup_window.geometry("400x350")
        setup_window.resizable(False, False)
        
        # Center the window
        setup_window.update_idletasks()
        width = setup_window.winfo_width()
        height = setup_window.winfo_height()
        x = (setup_window.winfo_screenwidth() // 2) - (width // 2)
        y = (setup_window.winfo_screenheight() // 2) - (height // 2)
        setup_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Title
        title_label = tk.Label(
            setup_window,
            text="Welcome to MochiPet! 🐾",
            font=("Arial", 16, "bold"),
            fg="#5D4037"
        )
        title_label.pack(pady=15)
        
        # Name
        tk.Label(setup_window, text="What's your name?", font=("Arial", 10)).pack(anchor="w", padx=30)
        name_entry = tk.Entry(setup_window, font=("Arial", 10), width=30)
        name_entry.pack(padx=30, pady=5)
        
        # Gender
        tk.Label(setup_window, text="What's your gender?", font=("Arial", 10)).pack(anchor="w", padx=30, pady=(15, 0))
        gender_var = tk.StringVar(value="female")
        tk.Radiobutton(setup_window, text="Female", variable=gender_var, value="female", font=("Arial", 9)).pack(anchor="w", padx=50)
        tk.Radiobutton(setup_window, text="Male", variable=gender_var, value="male", font=("Arial", 9)).pack(anchor="w", padx=50)
        
        # Daily water intake target
        tk.Label(setup_window, text="Daily water intake target (ml):", font=("Arial", 10)).pack(anchor="w", padx=30, pady=(15, 0))
        water_entry = tk.Entry(setup_window, font=("Arial", 10), width=30)
        water_entry.insert(0, "2000")
        water_entry.pack(padx=30, pady=5)
        
        # Submit button
        def save_profile():
            name = name_entry.get().strip()
            gender = gender_var.get()
            
            if not name:
                messagebox.showwarning("Input Error", "Please enter your name!")
                return
            
            try:
                daily_target = int(water_entry.get())
                if daily_target <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid water intake target!")
                return
            
            # Save to data.json
            data = {}
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
            
            data["user_profile"] = {
                "name": name,
                "gender": gender,
                "daily_target_ml": daily_target
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.user_data = data["user_profile"]
            setup_window.destroy()
        
        submit_button = tk.Button(
            setup_window,
            text="Let's Go! 🎉",
            font=("Arial", 11, "bold"),
            bg="#81C784",
            fg="white",
            command=save_profile,
            padx=20,
            pady=8
        )
        submit_button.pack(pady=20)
        
        setup_window.mainloop()
        return True
    
    def get_user_profile(self):
        """Get the user profile from data.json"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                if "user_profile" in data:
                    return data["user_profile"]
        return None
