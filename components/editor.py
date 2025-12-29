import tkinter as tk
from tkinter import ttk
import pyautogui as pg
import components.main_window as r
import json
DB_SETTING = "setting.json"
class Editor:
    def __init__(self):
        self.entries_list = []
        
        # Create Toplevel Window
        self.editor_window = tk.Toplevel(r.root)
        self.editor_window.geometry("550x650")
        self.editor_window.title("Script Editor")
        copy_button = "f1"
        try:
            with open("setting.json","r") as f:
                copy_button = json.load(f)[0]["copy"]
        except:
            pass
        self.editor_window.bind("<{}>".format(copy_button.upper()), self.copy_coords)

        # Main Container
        self.main_frame = ttk.Frame(self.editor_window, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        # Header
        ttk.Label(
            self.main_frame, text="Script Editor", font=("Arial", 16, "bold")
        ).pack(pady=(0, 10))

        # --- Control Bar ---
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill="x", pady=(0, 10))

        # Buttons (Logic to be injected by Controller)
        self.add_button = ttk.Button(self.control_frame, text="ADD ENTRY", command=self.add_entry)
        self.add_button.pack(side="left", padx=5)

        self.save_button = ttk.Button(self.control_frame, text="SAVE")
        self.save_button.pack(side="left", padx=5)

        self.execute_button = ttk.Button(self.control_frame, text="EXECUTE")
        self.execute_button.pack(side="left", padx=5)

        # Interval Selector
        self.interval_values = [str(round(x * 0.1, 1)) for x in range(1, 11)]
        self.interval = ttk.Combobox(
            self.control_frame, 
            values=self.interval_values, 
            width=5, 
            font=("Arial", 10),
            state="readonly"
        )
        self.interval.set("0.1")
        self.interval.pack(side="left", padx=5)
        ttk.Label(self.control_frame, text="Interval(s)").pack(side="left")

        # --- Scrollable Area ---
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Scroll Wheel Bindings
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Add initial empty entry
        self.add_entry()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def copy_coords(self, event=None):
        """Helper to copy current mouse coords to clipboard."""
        x, y = pg.position()
        text = f"{x},{y}"
        self.editor_window.clipboard_clear()
        self.editor_window.clipboard_append(text)
        self.editor_window.update()

    def add_entry(self):
        """Adds a new text entry row."""
        self.insert_entry(None, None)

    def insert_entry(self, parent_frame=None, current_widget=None):
        """Inserts a new entry after the current one."""
        
        # Container for this row
        row_frame = ttk.Frame(self.scrollable_frame)
        
        # Positioning logic
        if parent_frame:
            row_frame.pack(fill="x", pady=2, after=parent_frame)
        else:
            row_frame.pack(fill="x", pady=2)

        # Text Area
        text_widget = tk.Text(
            row_frame, font=("Consolas", 11), width=40, height=1, wrap="none"
        )
        text_widget.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # --- Internal Key Bindings ---
        def on_enter(e):
            self.insert_entry(row_frame, text_widget)
            return "break" # Prevent newline

        def on_up(e):
            try:
                idx = self.entries_list.index(text_widget)
                if idx == 0:
                    pass
                else:
                    prev_widget = self.entries_list[idx-1]
                    prev_widget.focus_set()
                self.canvas.yview_scroll(-1, "units")
            except e:
                pass
            return "break"


        def on_backspace(e):
            try:
                current_text = text_widget.get("1.0","end-1c")
                if not current_text:
                    idx = self.entries_list.index(text_widget)
                    if idx != 0:
                        prev_widget = self.entries_list[idx-1]
                        prev_widget.focus_set()
                        prev_widget.mark_set("insert","end")
                    self.delete_entry(row_frame,text_widget)
            except e:
                pass

        def on_down(e):

            try:
                idx = self.entries_list.index(text_widget)
                if idx == len(self.entries_list)-1:
                    pass
                else:
                    next_widget = self.entries_list[idx+1]
                    next_widget.focus_set
                self.canvas.yview_scroll(1, "units")
            except e:
                pass
            return "break"

        text_widget.bind("<Return>", on_enter)
        text_widget.bind("<Up>", on_up)
        text_widget.bind("<Down>", on_down)
        text_widget.bind("<BackSpace>",on_backspace)
        
        # Row Buttons
        del_btn = ttk.Button(
            row_frame, text="X", width=3,
            command=lambda: self.delete_entry(row_frame, text_widget)
        )
        del_btn.pack(side="right")
        
        add_btn = ttk.Button(
            row_frame, text="+", width=3,
            command=lambda: self.insert_entry(row_frame, text_widget)
        )
        add_btn.pack(side="right")

        # Add to list
        if current_widget in self.entries_list:
            idx = self.entries_list.index(current_widget)
            self.entries_list.insert(idx + 1, text_widget)
        else:
            self.entries_list.append(text_widget)

        text_widget.focus_set()

    def delete_entry(self, frame, widget):
        if widget in self.entries_list:
            self.entries_list.remove(widget)
        frame.destroy()