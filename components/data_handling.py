from tkinter import messagebox, ttk
from tkinter import filedialog
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

    def find_config(self):
        selected_configure = self.run_selection.get()
        load_data = {}
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
                data = json.load(conf)
            conf_id = int(selected_configure.split(".")[0])
            for i in range(len(data)):
                if data[i]["id"] == conf_id:
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
    def import_data(self):
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Select json file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if filepath:
            try:
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
                data = json.load(conf)
            start_index = 1
            for item in data:
                item["id"] = start_index
                start_index += 1
            with open("conf.json","w") as conf:
                json.dump(data,conf,indent=4)
            messagebox.showinfo(message="Index reset successfully!")
            self.update_selection()
        except Exception as e:
            messagebox.showerror(message="Something went wrong!",details=str(e))










