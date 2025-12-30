from tkinter import messagebox, ttk
from tkinter import filedialog
<<<<<<< HEAD
import tkinter as tk
import components.main_window as r
import json
import os
KEYS = [
    # Alphanumeric
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    
    # Function Keys
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24',

    # Modifiers
    'alt', 'alt gr', 'ctrl', 'left alt', 'left ctrl', 'left shift', 'left win',
    'right alt', 'right ctrl', 'right shift', 'right win', 'shift', 'windows',
    'command', 'option', # Sometimes mapped on Mac keyboards

    # Navigation & Editing
    'backspace', 'delete', 'down', 'end', 'enter', 'esc', 'home', 'insert',
    'left', 'page down', 'page up', 'right', 'space', 'tab', 'up',

    # Keypad
    'num lock', 'numpad 0', 'numpad 1', 'numpad 2', 'numpad 3', 'numpad 4',
    'numpad 5', 'numpad 6', 'numpad 7', 'numpad 8', 'numpad 9',
    'numpad add', 'numpad decimal', 'numpad divide', 'numpad enter',
    'numpad multiply', 'numpad subtract',

    # Symbols & Punctuation
    '`', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/',
    'caps lock', 'pause', 'print screen', 'scroll lock',
    
    # Media & Special
    'volume down', 'volume up', 'volume mute', 'play/pause', 'stop', 
    'next track', 'previous track', 'browser back', 'browser forward', 
    'browser home', 'browser refresh', 'browser search', 'browser stop',
    'launch app 1', 'launch app 2', 'launch mail', 'launch media',
    'sleep'
]
DB = "conf.json"
DB_SETTING = "setting.json"
DEFAULT_CONFIG = []
DEFAULT_CONFIG_SETTING = [{"copy": "F1", "stop": "q"}]

class DataHandling():
    def __init__(self):
        # Initialize Config DB
        if not os.path.exists(DB):
            with open(DB, "w") as f:
                json.dump(DEFAULT_CONFIG, f)

        # Initialize Setting DB
        if not os.path.exists(DB_SETTING):
            with open(DB_SETTING, "w") as f:
                json.dump(DEFAULT_CONFIG_SETTING, f)

        # --- UI Setup ---
        self.configure_frame = ttk.Frame(r.root, padding=5)
        self.configure_frame.pack(fill="both", expand=True)

        # Dropdowns
        self.del_selection = ttk.Combobox(self.configure_frame, state="readonly", width=30)
        self.del_selection.set("Delete a config")
        self.del_selection.pack(pady=10)
        
        self.run_selection = ttk.Combobox(self.configure_frame, state="readonly", width=30)
        self.run_selection.set("Open a config")
        self.run_selection.pack(pady=(1, 1))
        
        self.update_selection()
        self.del_selection.bind("<<ComboboxSelected>>", self.del_config)

        # Extra Functions Frame
        self.extra_function_frame = ttk.Frame(self.configure_frame)
        self.extra_function_frame.pack(anchor="center", pady=5)
        
        self.import_button = ttk.Button(self.extra_function_frame, text="Import", width=10, command=self.import_data)
        self.import_button.pack(side="left", padx=2)
        
        self.reset_index_button = ttk.Button(self.extra_function_frame, text="Reset Index", width=10, command=self.reset_config)
        self.reset_index_button.pack(side="left", padx=2)

        # Setting Button Frame
        self.setting_frame = ttk.Frame(self.configure_frame)
        self.setting_frame.pack(pady=5)
        # Fixed the incomplete command here
        self.setting_button = ttk.Button(self.setting_frame, text="SETTING", width=20, command=self.hotkey_setting)
        self.setting_button.pack()
=======
import components.main_window as r
import json
import os
DB = "conf.json"
DEFAULT_CONFIG = []
class DataHandling():
    def __init__(self):
        if not os.path.exists(DB):
            with open(DB, "w") as f:
                json.dump(DEFAULT_CONFIG, f)
        try:
            with open("conf.json", "r") as config:
                data = json.load(config)
            options = []
            for items in data:
                options.append((items["id"], items["name"]))
        except KeyError:
            print()
        self.configure_frame = ttk.Frame(r.root,padding=5)
        self.configure_frame.pack(fill = "both",expand=True)
        self.del_selection = ttk.Combobox(self.configure_frame,state="readonly",width=30,values = [str(item[0])+"."+item[1] for item in options])
        self.del_selection.set("Delete a config")
        self.del_selection.pack(pady=10)
        self.run_selection = ttk.Combobox(self.configure_frame,state="readonly",width=30,values = [str(item[0]) + "." + item[1] for item in options])
        self.run_selection.set("Open a config")
        self.run_selection.pack(pady=(1,1))
        self.del_selection.bind("<<ComboboxSelected>>",self.del_config)
        self.extra_function_frame = ttk.Frame(self.configure_frame,padding=1)
        self.extra_function_frame.pack(anchor="center")
        self.import_button = ttk.Button(self.extra_function_frame,text="Import",width=10,command=self.import_data)
        self.import_button.pack(side="left")
        self.reset_index_button = ttk.Button(self.extra_function_frame,text="Reset Index",width=10,command=self.reset_config)
        self.reset_index_button.pack(side="left")
>>>>>>> 358525b105fd275ed0745680f6162683843288f4

    def find_config(self):
        selected_configure = self.run_selection.get()
        load_data = {}
<<<<<<< HEAD
        try:
            with open("conf.json", "r") as conf:
=======
        with open("conf.json","r") as conf:
            data = json.load(conf)
        conf_id = int(selected_configure.split(".")[0])
        for i in range(len(data)):
            if data[i]["id"] == conf_id:
                load_data = data[i]
                print("found the configure!")
                break
        self.run_selection.set("Open a config")
        return load_data
    def del_config(self,event):
        confirm = messagebox.askyesno(message="Do you really want to delete this?")
        if confirm:
            selected_configure = self.del_selection.get()
            with open("conf.json","r") as conf:
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
                data = json.load(conf)
            conf_id = int(selected_configure.split(".")[0])
            for i in range(len(data)):
                if data[i]["id"] == conf_id:
<<<<<<< HEAD
                    load_data = data[i]
                    break
        except Exception:
            pass
        self.run_selection.set("Open a config")
        return load_data

    def del_config(self, event):
        confirm = messagebox.askyesno(message="Do you really want to delete this?")
        if confirm:
            selected_configure = self.del_selection.get()
            try:
                with open("conf.json", "r") as conf:
                    data = json.load(conf)
                conf_id = int(selected_configure.split(".")[0])
                for i in range(len(data)):
                    if data[i]["id"] == conf_id:
                        data.remove(data[i])
                        break
                with open("conf.json", "w") as conf:
                    json.dump(data, conf, indent=4)
                self.update_selection()
            except Exception:
                pass
        self.del_selection.set("Delete a config")

    def update_selection(self):
        try:
            with open("conf.json", "r") as conf:
                data = json.load(conf)
            options = []
            for item in data:
                options.append((item["id"], item["name"]))
            values = [str(item[0]) + "." + item[1] for item in options]
            self.del_selection.configure(state="readonly", values=values)
            self.run_selection.configure(state="readonly", values=values)
        except Exception:
            self.del_selection.configure(values=[])
            self.run_selection.configure(values=[])

=======
                    data.remove(data[i])
                    break
            with open("conf.json","w") as conf:
                json.dump(data,conf,indent=4)
        self.del_selection.set("Delete a config")
        self.update_selection()

    def update_selection(self):
        with open("conf.json","r") as conf:
            data = json.load(conf)
        options = []
        for item in data:
            options.append((item["id"],item["name"]))
        self.del_selection.configure(state="readonly",values = [str(item[0])+"."+item[1] for item in options])
        self.run_selection.configure(state="readonly",values = [str(item[0]) + "." + item[1] for item in options])
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
    def import_data(self):
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Select json file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if filepath:
            try:
<<<<<<< HEAD
                with open(filepath, "r") as imp_conf:
                    import_data = json.load(imp_conf)
                with open("conf.json", "r") as conf:
                    conf_data = json.load(conf)
                
                start_id = int(conf_data[-1]["id"]) + 1 if conf_data else 1
                
                for item in import_data:
                    item["id"] = start_id
                    start_id += 1
                    conf_data.append(item)
                    
                with open("conf.json", "w") as conf:
                    json.dump(conf_data, conf, indent=4)
                messagebox.showinfo(message="Data imported!")
                self.update_selection()
            except Exception:
                messagebox.showerror(message="Something went wrong!")

    def reset_config(self):
        try:
            with open("conf.json", "r") as conf:
=======
                with open(filepath,"r") as imp_conf:
                    import_data = json.load(imp_conf)
                with open("conf.json","r")  as conf:
                    conf_data = json.load(conf)
                for item in import_data:
                    item["id"] = int(conf_data[len(conf_data)-1]["id"]) + 1
                    conf_data.append(item)
                with open("conf.json","w") as conf:
                    json.dump(conf_data,conf,indent=4)
                messagebox.showinfo(message="Data imported!")
            except Exception as e:
                messagebox.showerror(message="Something went wrong!",details=str(e))

    def reset_config(self):
        try:
            with open("conf.json","r") as conf:
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
                data = json.load(conf)
            start_index = 1
            for item in data:
                item["id"] = start_index
                start_index += 1
<<<<<<< HEAD
            with open("conf.json", "w") as conf:
                json.dump(data, conf, indent=4)
            messagebox.showinfo(message="Index reset successfully!")
            self.update_selection()
        except Exception as e:
            messagebox.showerror(message="Something went wrong!", details=str(e))

    def hotkey_setting(self):
        """Opens a window to configure hotkeys."""
        self.setting_window = tk.Toplevel(r.root)
        self.setting_window.geometry("250x200")
        self.setting_window.title("Settings")

        # Load current settings
        try:
            with open(DB_SETTING, "r") as f:
                settings = json.load(f)[0]
        except Exception:
            settings = DEFAULT_CONFIG_SETTING[0]
        print(settings)

        # --- Copy Coordinate Hotkey ---
        frame_copy = ttk.Frame(self.setting_window, padding=10)
        frame_copy.pack(fill="x")
        
        ttk.Label(frame_copy, text="Copy Coordinate Key:").pack(side="left")
        
        copy_entry = ttk.Entry(frame_copy)
        copy_entry.insert(0, settings["copy"])
        copy_entry.pack(side="left", padx=2,fill="y")

        # --- Stop Execution Hotkey ---
        frame_stop = ttk.Frame(self.setting_window, padding=10)
        frame_stop.pack(fill="x")
        
        ttk.Label(frame_stop, text="Stop Execution Key:").pack(anchor="w",side="left")
        
        stop_entry = ttk.Entry(frame_stop)
        stop_entry.insert(0, settings["stop"])
        stop_entry.pack(side="left",padx=2,fill="y")

        # --- Save Function ---
        def save_settings():
            new_copy = copy_entry.get().strip().lower()
            new_stop = stop_entry.get().strip().lower()

            if not new_copy or not new_stop or (not new_copy in KEYS or not new_stop in KEYS):
                messagebox.showerror("Error", "Keys values must be valid!")
                return

            new_settings = [{"copy": new_copy, "stop": new_stop}]
            
            try:
                with open(DB_SETTING, "w") as f:
                    json.dump(new_settings, f, indent=4)
                messagebox.showinfo("Success", "Settings saved! Restart app to apply.")
                self.setting_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save settings: {e}")

        # Save Button
        save_btn = ttk.Button(self.setting_window, text="SAVE SETTINGS", command=save_settings)
        save_btn.pack(pady=20)
=======
            with open("conf.json","w") as conf:
                json.dump(data,conf,indent=4)
            messagebox.showinfo(message="Index reset successfully!")
            self.update_selection()
        except Exception as e:
            messagebox.showerror(message="Something went wrong!",details=str(e))










>>>>>>> 358525b105fd275ed0745680f6162683843288f4
