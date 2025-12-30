import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
from components.data_handling import DataHandling
from components.editor import Editor
from components.parser import Parser  # Import the new Parser class
import components.main_window as r
import json
DB_SETTING = "setting.json"
class Scripting(DataHandling):
    def __init__(self):
        # Initialize DataHandling to manage config files
        DataHandling.__init__(self)

        self.run_selection.bind("<<ComboboxSelected>>",lambda event: self.new_editor(self.find_config()))
        
        self.current_parser = None
        
        # UI Setup
        self.script_frame = ttk.Frame(r.root)
        self.script_frame.pack(fill="both", expand=True, pady=10)
        
        self.editor_button = tk.Button(
            self.script_frame,
            text="Open Editor",
            font=("Arial", 12),
            bg="#e1e1e1",
            command=self.new_editor
        )
        self.editor_button.pack()
        
        # Bind button to stop execution globally
        stop_button = "q"
        with open(DB_SETTING,"r") as f:
            stop_button = json.load(f)[0]["stop"]
        keyboard.add_hotkey('{}'.format(stop_button.upper()), self.stop_execution)
    def new_editor(self, load_entry=None):
        #New Editor Window
        editor_window = Editor()
        
        # RE-BIND BUTTONS: Override Editor's default buttons with Scripting logic
        editor_window.execute_button.configure(
            command=lambda: self.run_parser(editor_window)
        )
        editor_window.save_button.configure(
            command=lambda: self.save_script(editor_window)
        )

        # LOAD EXISTING SCRIPT if provided
        if load_entry:
            try:
                # Clear default entry if any (Editor starts with 1 empty entry)
                # But easiest way is just to append data.
                # If we want to replace, we could iterate and delete, 
                # but appending to the fresh window is safer.
                
                # Note: Editor __init__ adds one empty entry. We might want to use it or ignore it.
                # Here we simply fill the entries.
                first = True
                for cmd in load_entry.get("command", []):
                    if first:
                        # Use the initial empty entry for the first command
                        editor_window.entries_list[0].insert("1.0", cmd)
                        first = False
                    else:
                        editor_window.add_entry()
                        editor_window.entries_list[-1].insert("1.0", cmd)
            except Exception as e:
                print(f"Load Error: {e}")
                messagebox.showerror("Error", "Failed to load configuration.")

    def run_parser(self, editor_window):
        """Instantiates and runs the Parser on the current editor content."""
        # 1. Get Interval
        try:
            val = editor_window.interval.get()
            # Handle default text "Interval" or empty string
            interval = float(val) if val.replace('.','',1).isdigit() else 0.1
        except ValueError:
            interval = 0.1

        # 2. Initialize Parser with the Text widgets list
        self.current_parser = Parser(editor_window.entries_list, interval)
        
        # 3. Start Execution
        self.current_parser.start()

    def stop_execution(self):
        """Stops the running parser if one exists."""
        if self.current_parser:
            self.current_parser.stop()
            # We don't set self.current_parser to None immediately 
            # because the thread might take a moment to finish.

    def save_script(self, editor_window):
        """Saves the current script to conf.json via DataHandling."""
        command_list = []
        
        # Extract text from widgets
        for entry in editor_window.entries_list:
            text = entry.get("1.0", "end-1c").strip()
            if text:
                command_list.append(text)
        
        if not command_list:
            messagebox.showwarning("Empty", "Script is empty!")
            return

        # Popup for Naming
        conf_name_window = tk.Toplevel(r.root)
        conf_name_window.title("Save Configuration")
        conf_name_window.geometry("250x120")
        
        ttk.Label(conf_name_window, text="Enter Configuration Name:", padding=5).pack(fill="x")
        name_entry = ttk.Entry(conf_name_window)
        name_entry.pack(fill="x", padx=10, pady=5)
        name_entry.focus_set()

        def confirm_save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            # Use DataHandling logic (or manual json handling)
            try:
                with open("conf.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Generate new ID
            new_id = (data[-1]["id"] + 1) if data else 1
            
            new_config = {
                "id": new_id,
                "name": name,
                "command": command_list
            }
            
            data.append(new_config)
            
            try:
                with open("conf.json", "w") as f:
                    json.dump(data, f, indent=4)
                
                # Refresh the dropdown in DataHandling UI
                self.update_selection()
                conf_name_window.destroy()
                messagebox.showinfo("Success", "Script saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

        ttk.Button(conf_name_window, text="Save", command=confirm_save).pack(pady=10)
