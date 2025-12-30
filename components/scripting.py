import json
import threading
<<<<<<< HEAD
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
=======
from datetime import datetime
import tkinter as tk
from random import random
from tkinter import ttk
from tkinter import messagebox
import keyboard
import random
from components.data_handling import DataHandling
import components.main_window as r
import pyautogui as pg
import time
DB = "conf.json"
class Scripting(DataHandling):
    def __init__(self):
        DataHandling.__init__(self)
        #Scripting
        self.selected_interval = 0.1
        self.tutorial_window = None
        self.editor_window = None
        self.script_frame = ttk.Frame(r.root)
        self.script_frame.pack(fill="both", expand=True)
        self.editor_button = tk.Button(self.script_frame,text="Open Editor",font=("Arial",12),command =self.editor)
        self.editor_button.pack()
        self.new_configure_button = tk.Button(text="New Configure",font=("Arial",12),)
        self.run_selection.bind("<<ComboboxSelected>>",self.open_config)

    def editor(self):
        #Create new windows
        self.editor_window = tk.Toplevel(r.root)
        self.editor_window.geometry("550x600")
        self.editor_window.bind("<F1>", self.copy)
        self.entries_list = []

        # Create main frame
        main_frame = ttk.Frame(self.editor_window, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Editor",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=(0, 10))

        # Add entry button
        add_button = ttk.Button(
            control_frame,
            text="ADD",
            command=self.add_entry
        )
        add_button.pack(side="left", padx=(0, 10))

        # Save button
        save_button = ttk.Button(
            control_frame,
            text="SAVE",
            command=self.save_content
        )
        save_button.pack(side="left",padx=(0,10))

        #Execute button
        execute_button = ttk.Button(
            control_frame,
            text="EXECUTE",
            command=self.parser
        )
        execute_button.pack(side="left",padx=(0,10))

        #Setting button
        interval_num = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        INTERVAL = [str(interval) for interval in interval_num]
        self.interval = ttk.Combobox(control_frame,state="readonly",values=INTERVAL,font=("Arial",12))
        self.interval.pack(side="left")
        self.interval.bind("<<ComboboxSelected>>",self.select_interval)
        self.interval.set("Interval")


        # Create a frame for the scrollable entries area
        entries_container = ttk.Frame(main_frame)
        entries_container.pack(fill="both", expand=True)

        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(entries_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(entries_container, orient="vertical", command=self.canvas.yview)

        # Create frame inside canvas to hold entries
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure canvas scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas for our frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to scroll
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.add_entry()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_entry(self):
        # Create a frame for this entry with controls
        entry_frame = ttk.Frame(self.scrollable_frame)
        entry_frame.pack(fill="x", pady=(0, 5),)


        # Create the entry widget
        entry = tk.Text(
            entry_frame,
            font=("Arial", 11),
            width=35,
            height = 1
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))


        # Create delete button
        delete_button = ttk.Button(
            entry_frame,
            text = "Delete",
            width=6,
            command=lambda: self.delete_entry(entry,entry_frame)
        )
        delete_button.pack(side="left", padx=(0, 5))

        add_button = ttk.Button(
            entry_frame,
            text="Add",
            width=6,
            command=lambda: self.insert_entry(entry_frame,entry)
        )
        add_button.pack(side="left", padx=(0, 5))
        # Store the entry and its components
        self.entries_list.append(entry)




    def delete_entry(self, entry,entry_frame):
        self.entries_list.remove(entry)
        entry_frame.destroy()

    def insert_entry(self,insert_frame,insert_entry):
        entry_frame = ttk.Frame(self.scrollable_frame)
        entry_frame.pack(fill="x", pady=(0, 5),after=insert_frame)
        # Create the entry widget

        entry = tk.Text(
            entry_frame,
            font=("Arial", 11),
            width=35,
            height = 1
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))


        # Create delete button
        delete_button = ttk.Button(
            entry_frame,
            text = "Delete",
            width=6,
            command=lambda: self.delete_entry(entry,entry_frame)
        )
        delete_button.pack(side="left", padx=(0, 5))

        add_button = ttk.Button(
            entry_frame,
            text="Add",
            width=6,
            command=lambda: self.insert_entry(entry_frame,entry)
        )
        add_button.pack(side="left", padx=(0, 5))
        # Store the entry and its components
        self.entries_list.insert(self.entries_list.index(insert_entry)+1,entry)

    def select_interval(self,event):
        self.selected_interval = float(self.interval.get())
        self.interval.set(self.selected_interval)

    def save_content(self):
        command_list = []
        with open("conf.json","r") as conf:
            r_data = json.load(conf)
        def add_conf():
            w_data = {}
            for command in self.entries_list:
                if command.get("1.0","end-1c").strip():
                    command_list.append(command.get("1.0","end-1c").strip())
            if len(r_data) > 0:
                w_data["id"] = r_data[len(r_data)-1]["id"] + 1
            else:
                w_data["id"] = 1
            w_data["name"] = self.name_entry.get().strip()
            w_data["command"] = command_list
            r_data.append(w_data)
            try:
                with open("conf.json","w") as conf:
                    json.dump(r_data, conf, indent=4)
                self.update_selection()
                self.conf_name_window.destroy()
                messagebox.showinfo(message="Save successfully!")
            except Exception:
                messagebox.showerror(message="Cannot save")

        self.conf_name_window = tk.Toplevel(self.editor_window)
        self.conf_name_window.title("Saving")
        self.conf_name_window.geometry("200x100")
        self.save_label = ttk.Label(self.conf_name_window,text="Enter name:")
        self.save_label.pack(side="top",fill="x")
        self.name_entry = ttk.Entry(self.conf_name_window)
        self.name_entry.pack(side="top",fill="x")
        self.save_button = ttk.Button(self.conf_name_window,text= "Save",command=add_conf)
        self.save_button.pack(side="top",fill="x")


    def copy(self,event):
        text = '{},{}'.format(pg.position().x, pg.position().y)
        self.editor_window.clipboard_clear()
        self.editor_window.clipboard_append(text)
    def parser(self):
        for entry in self.entries_list:
            print(entry.get("1.0","end-1c"))
        try:
            self.finished_parser = threading.Event()
            stop_thread = threading.Thread(target=self.stop_parser,daemon=True)
            stop_thread.start()
            i = 0
            total_size = len(self.entries_list)
            while i < total_size:
                jump = 1
                if self.finished_parser.is_set():
                    break
                if self.entries_list[i].get("1.0","end-1c"):
                    command = self.entries_list[i].get("1.0","end-1c").strip()
                    if command[0:2] == '//':
                        i += jump
                        continue
                    if command[0:6].lower() == "repeat":
                        end_index = None
                        for j in range(i+1,len(self.entries_list)):
                            if self.entries_list[j].get("1.0","end-1c").strip() == "end":
                                end_index = j
                                break
                        repeat_time = int(command[6:len(command)-1])
                        jump = repeat_time+1
                        print(repeat_time)
                        for _ in range(repeat_time):
                            if self.finished_parser.is_set():
                                break
                            repeat_count = i+1
                            while repeat_count < end_index:
                                if self.finished_parser.is_set():
                                    break
                                repeat_jump = 1
                                if self.entries_list[repeat_count].get("1.0","end-1c").strip():
                                    repeat_command = self.entries_list[repeat_count].get("1.0","end-1c").strip()
                                    if repeat_command[0:2] == "//":
                                        repeat_count += 1
                                        continue
                                    if repeat_command[0:6].lower() == "listen" or repeat_command[0:13].lower() == "randomcommand":
                                        repeat_jump = self.advance_parsing(repeat_command,repeat_count)
                                    else:
                                        self.basic_parsing(repeat_command)
                                time.sleep(self.selected_interval)
                                repeat_count += repeat_jump

                    elif command[0:6].lower() == "listen" or command[0:13].lower() == "randomcommand":
                        jump = self.advance_parsing(command,i)
                    else:
                        self.basic_parsing(command)
                i += jump
                time.sleep(self.selected_interval)
            self.finished_parser.set()
        except Exception :
                messagebox.showerror("Error","Something went wrong")

    def advance_parsing(self,command,index):
        jump = 1
        if command[0:6].lower() == "listen":
            image_thread = threading.Thread(target=self.listen, daemon=True, args=[index, command])
            image_thread.start()
            components = command.split(",")
            jump = components[3] + 1
        if command[0:13].lower() == "randomcommand":
            components = command[13:].split(",")
            if components[1].lower() == "uniform":
                random_entry_index = random.randint(index+1, index+int(components[0]))
                if self.entries_list[random_entry_index].get("1.0","end-1c").strip():
                    self.basic_parsing(self.entries_list[random_entry_index].get("1.0","end-1c").strip())
            else:
                entry_index_list = [index for index in range(index+1, index+int(components[0])+1)]
                probability_list = [float(components[index]) for index in range(1,int(components[0]) +1)]
                chosen_entry = random.choices(entry_index_list,weights=probability_list,k=1)[0]
                chosen_command = self.entries_list[chosen_entry].get("1.0","end-1c").strip()
                if chosen_command:
                    self.basic_parsing(chosen_command)
            jump = int(components[0]) + 1
        return jump
    def basic_parsing(self,command):
            #Handle click command cX,Y,T
            if command[0:5].lower() == "click":
                cor = (command[5:]).split(",")
                if cor[0].isdigit() and cor[1].isdigit():
                    pg.moveTo(int(cor[0]),int(cor[1]))
                    if len(cor) == 2:
                        pg.click()
                    if len(cor) == 3:
                        pg.click(clicks=int(cor[2]),interval=0.01)
                else:
                    try:
                        check = cor[1][0].upper() + cor[1][1:].lower()
                        if len(cor) == 3:
                            img = pg.center(pg.locateOnScreen(cor[0],grayscale=check,region=cor[2],confidence=0.9))
                        else:
                            img = pg.center(pg.locateOnScreen(cor[0],grayscale=check,confidence=0.9))
                        pg.click(img[0],img[1])
                    except pg.ImageNotFoundException:
                        print()
                    except Exception as e:
                        print()

                #Handle wait command wX
            if command[0:4].lower() == 'wait':
                w_time = float(command[4:])
                for i in range(int(w_time / 0.1)):
                    if self.finished_parser.is_set():
                        break
                    time.sleep(0.1)
            if command[0:9].lower() == "waituntil":
                req_time = command[9:]
                flag = False
                while True:
                    cur_time = str(datetime.now().time())
                    if req_time < cur_time:
                        break
                    if self.finished_parser.is_set():
                        break
                    time.sleep(1)
                #Handle type command t[TEXT]
            if command[0:4].lower() == 'type':
                pg.write(command[4:])
                #Handle press command pButton
            if command[0:5].lower() == 'press':
                pg.press(command[5:].lower())
            #HANDLE press down and release BUTTON:
            if command[0:9].lower() == 'pressdown':
                pg.keyDown(command[9:].lower())
            if command[0:7].lower() == "release":
                pg.keyUp(command[7:].lower())
            #Handle Drag:
            if command[0:6].lower() == 'dragto':
                components = command[6:].split(",")
                x = int(components[0])
                y = int(components[1])
                button = components[2].lower()
                t = float(components[3])
                pg.dragTo(x,y,t,button=button)
            if command[0:6].lower() == "scroll":
                pg.scroll(int(command[6:]))
            if command[0:9].lower() == "mousedown":
                components = command[9:].split(",")
                x = int(components[0])
                y = int(components[1])
                option = components[2].lower()
                pg.mouseDown(x,y,option)
            if command[0:7].lower() == "mouseup":
                components = command[7:].split(",")
                x = int(components[0])
                y = int(components[1])
                option = components[2].lower()
                pg.mouseUp(x,y,option)
            if command[0:10].lower() == "randomtype":
                components = command[10:].split(",")
                file = ""
                random_index = 10
                if len(components) == 1:
                    file = command[10:]
                else:
                    file = components[0]
                    with open(file, "r",encoding="utf-8") as random_text:
                        data = random_text.readlines()
                    random_index = random.randint(0, len(data) - 1)
                    pg.write(data[random_index].strip())
                if len(components) == 2:
                    del data[random_index]
                    with open(file, "w",encoding="utf-8") as write_file:
                        write_file.writelines("".join(data))

    def listen(self,index,command):
        #Listenimg.png,50,0.1,1,100,false
        try:
            command_parts = command.split(",")
            additional_para = None
            img = command_parts[0][6:]
            run_time = int(command_parts[1])
            rest = float(command_parts[2])
            command_num = int(command_parts[3])
            execute_num = int(command_parts[4])
            checkcolor = command_parts[5][0].upper() + command_parts[5][1:].lower()
            if len(command_parts) == 7:
                additional_para = command_parts[5]
            seq = []
            sec = 0
            self.count_execute = 0
            for i in range(index+1,index+command_num+1):
                seq.append(self.entries_list[i].get("1.0","end-1c"))
            check_image_thread = threading.Thread(target=self.image_catching,args=[seq,img,rest,checkcolor,additional_para],daemon=True)
            self.stop_event = threading.Event()
            check_image_thread.start()
            check_stop = threading.Thread(target=self.stop_image, daemon=True)
            check_stop.start()
            while sec < run_time and not self.stop_event.is_set() and self.count_execute < execute_num:
                print(sec)
                time.sleep(1)
                sec+=1
            if sec >= run_time or self.count_execute >= execute_num:
                messagebox.showinfo(message="Finished!")
            self.stop_event.set()
        except Exception :
            messagebox.showerror("Error","Something went wrong")

    def image_catching(self,seq,img,rest,checkcolor,additional_para):
        while not self.stop_event.is_set():
            try:
                if additional_para:
                    flag = pg.locateOnScreen(img,grayscale=checkcolor,region=additional_para,confidence=0.9)
                else:
                    flag = pg.locateOnScreen(img,grayscale=checkcolor,confidence=0.9)
                print("found the image")
                for command in seq:
                    self.basic_parsing(command)
                self.count_execute+=1
            except pg.ImageNotFoundException as e:
                print()
            except Exception:
                messagebox.showerror("Error",message="something went wrong")
            time.sleep(rest)
    def stop_image(self):
        while not self.stop_event.is_set():
            if keyboard.is_pressed("q"):
                self.stop_event.set()
                messagebox.showinfo(message="Cancelled!")
                break
            time.sleep(0.1)
    def stop_parser(self):
        while not self.finished_parser.is_set():
            if keyboard.is_pressed("q"):
                self.finished_parser.set()
                messagebox.showinfo(message="Cancelled!")
                break

            time.sleep(0.1)
    def open_config(self,event):
        load_data = self.find_config()
        self.Editor()
        try:
            if load_data:
                for i in range(len(load_data["command"])):
                    self.add_entry()
                    self.entries_list[i].insert("1.0",load_data["command"][i])
        except Exception as e:
            messagebox.showerror("Error",message="something went wrong")
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
