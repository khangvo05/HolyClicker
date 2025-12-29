import threading
import time
import random
import re
import pyautogui as pg
import components.main_window as r
import keyboard
from tkinter import messagebox
import keyboard
import os
from datetime import datetime

class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    def is_empty(self):
        return len(self.items) == 0

class Parser:
    def __init__(self, entries_list, interval):
        self.raw_entries = entries_list
        self.interval = interval
        self.stop_flag = threading.Event()
        self.command_lines = []
        self.bracket_index = {}
        self.marked_indices = {}
        self.construction = []
        
        # 1. Extract valid lines
        for entry in self.raw_entries:
            text = entry.get("1.0", "end-1c").strip()
            # Only add non-empty lines that aren't comments
            if text and not text.startswith("//"):
                self.command_lines.append(text)
        # 2. Build Bracket Map (Begin/End pairing)
        self._map_blocks()

    def _map_blocks(self):
        #Finds matching begin/end pairs using a Stack (Leetcode 101)
        test_stack = Stack()
        for i in range(len(self.command_lines)):
            cmd = self.command_lines[i].lower()
            if cmd == 'begin':
                test_stack.push(i)
            elif cmd == 'end':
                open_pos = test_stack.pop()
                if open_pos is not None:
                    self.bracket_index[open_pos] = i
                else:
                    print(f"Syntax Error: Unmatched 'end'")

    def start(self):
        """Starts execution in a separate thread to keep UI responsive."""
        self.thread = threading.Thread(target=self._run_parser, daemon=True)
        self.thread.start()

    def _run_parser(self):
        try:
            # Build the Abstract Syntax Tree (AST)
            self.parse_program()
            print(self.construction)
            # Execute the built AST
            self.execute_construction()
            
            if not self.stop_flag.is_set():
                messagebox.showinfo("Done", "Script execution finished!")
        except Exception as e:
            print(f"Runtime Error: {e}")
            messagebox.showerror("Runtime Error", str(e))

    def checktype(self, command):
        """Helper to distinguish nested commands from simple statements."""
        c = command.lower().strip()
        # Check if the command starts with any keyword that requires a block (nested)
        if c.startswith('repeat') or c.startswith('if') or c.startswith('random') or c.startswith('until'):
            return 'nested'
        return 'statement'

    def parse_program(self):
        """Main parsing loop using jump logic for top-level commands."""
        current_index = 0
        while current_index < len(self.command_lines):
            cmd = self.command_lines[current_index]
            type_ = self.checktype(cmd)
            
            if type_ == 'statement':
                # Skip standalone 'begin' or 'end' keywords in the top loop
                if cmd.lower() != 'begin' and cmd.lower() != 'end':
                    self.construction.append(cmd)
                current_index += 1
                
            elif type_ == 'nested':
                # Ensure the next line is 'begin'
                if current_index + 1 < len(self.command_lines) and self.command_lines[current_index+1].lower() == 'begin':
                    # Recursively parse the block between begin and end
                    end_idx = self.bracket_index[current_index + 1]
                    parsed_block = self.parse_code(current_index + 2, end_idx)
                    
                    # Store as a dictionary { "command_string": [children] }
                    self.construction.append({cmd: parsed_block})
                    
                    # Jump execution index to after the closing 'end'
                    current_index = end_idx + 1
                else:
                    print(f"Syntax Error: Nested command '{cmd}' at line {current_index} must be followed by 'begin'")
                    current_index += 1

    def parse_code(self, start, end):
        """Recursive parsing using marked_indices to skip processed nested blocks."""
        parse = []
        for i in range(start, end):
            # If this index hasn't been processed yet
            if self.marked_indices.get(i) is None:
                self.marked_indices[i] = True
                
                cmd = self.command_lines[i]
                type_ = self.checktype(cmd)
                
                if type_ == 'statement':
                    if cmd.lower() != 'begin' and cmd.lower() != 'end':
                        parse.append(cmd)
                
                elif type_ == 'nested':
                    # Check for 'begin'
                    if i + 1 < len(self.command_lines) and self.command_lines[i+1].lower() == 'begin':
                        block_end = self.bracket_index[i + 1]
                        
                        # Recurse
                        nested_content = self.parse_code(i + 2, block_end)
                        parse.append({cmd: nested_content})
                        
                        # Mark the 'begin' and 'end' lines as processed so they aren't added as statements
                        self.marked_indices[i+1] = True
                        self.marked_indices[block_end] = True
                    else:
                        print(f"Syntax Error: Nested '{cmd}' missing 'begin' inside block")
        return parse

    def execute_construction(self):
        """Entry point for execution traversal."""
        self.execute_index = 0
        while self.execute_index < len(self.construction):
            item = self.construction[self.execute_index]
            
            if isinstance(item, str):
                self.basic_parsing(item)
                time.sleep(self.interval)
            else:
                self.nested_execute(item)

            self.execute_index += 1

    def nested_execute(self, dict_or_list):
        """Recursive execution"""
        if self.stop_flag.is_set(): return

        # Case 1: It's a Dictionary (Nested Command Wrapper)
        if isinstance(dict_or_list, dict):
            for key in dict_or_list:
                c = key.lower().strip()
                content = dict_or_list[key] # The list of children
                
                if c.startswith('repeat'):
                    # Syntax: repeatN: (repeat N times)
                    try:
                        times = int(c.split(":")[0].replace("repeat", ""))
                        for _ in range(times):
                            if self.stop_flag.is_set(): break
                            self.nested_execute(content)
                    except:
                        messagebox.showerror(f"Error parsing repeat syntax")
                        return
                
                elif c.startswith("until"):
                    #Syntax: untilIMG.png (repeat until IMG.png appears on the screen)
                    #Syntax: untilHH:MM:SS (repeat until HH:MM:SS)
                    try:
                        para = c[5:].strip()
                        if para.find(".png") != -1:
                            found = False
                            while not found:
                                if self.stop_flag.is_set(): break
                                self.nested_execute(content)
                                time.sleep(0.5)
                                try:
                                    pos = pg.locateOnScreen(para,confidence=0.8)
                                    if pos: found = True
                                except:
                                    pass
                        else:
                            passed = False
                            while not passed:
                                if self.stop_flag.is_set(): break
                                current_time = datetime.now().strftime("%H:%M:%S")
                                if current_time >= para:
                                    passed = True
                                    continue
                                self.nested_execute(content)
                                time.sleep(0.1)
                    except:
                        pass

                                
                                    
                elif c.startswith('if'):
                    # Syntax: ifX,Y (Checks if mouse is near X,Y)
                    try:
                        coords = c[2:].split(",")
                        tx, ty = int(coords[0]), int(coords[1])
                        mx, my = pg.position()
                        # Radius of 10 pixels
                        if abs(mx - tx) < 10 and abs(my - ty) < 10:
                            self.nested_execute(content)
                    except:
                        messagebox.showerror(f"Error parsing if syntax")
                
                elif c.startswith('random'):
                    # Syntax: random0.3,0.3,0.4
                    # Syntax: randomUNIFORM
                    # Logic: Pick ONE valid instruction from the children list based on the the distribution type: uniform or customized
                    if isinstance(content, list) and len(content) > 0:
                        choice = None
                        try:
                            if c[6:].lower() == 'uniform':
                                choice = random.choice(content)
                            else:
                                probability_distribution = [float(item) for item in c[6:].split(",")]
                                if all(isinstance(item,float) for item in probability_distribution) and len(probability_distribution) == len(content) and sum(probability_distribution) == 1:
                                    choice = random.choices(content,weights=probability_distribution,k=1)[0]                               
                        except:
                            messagebox.showerror(message="There is something wrong with syntax of 'random' command!")
                            return

                        if isinstance(choice, str):
                            self.basic_parsing(choice)
                            time.sleep(self.interval)
                        else:
                            self.nested_execute(choice)

                # elif c.startswith('listen'):
                #     threading.Thread(target=self.execute_listen,args=(key,content),daemon=True).start()
                #     #self.execute_listen(key, content)

        # Case 2: It's a List (Block of Commands)
        elif isinstance(dict_or_list, list):
            for item in dict_or_list:
                if self.stop_flag.is_set(): break
                
                if isinstance(item, str):
                    self.basic_parsing(item)
                    time.sleep(self.interval)
                else:
                    self.nested_execute(item)

    #SCRAPPED COMMAND: LISTEN (UNTIL IS A MORE STREAMLINED EXPERIENCE)
    # def execute_listen(self, cmd_str, content):
    #     # Syntax: listenIMG.PNG,DURATION,MAX,REGION(OPTIONAL)
    #     try:
    #         parts = cmd_str.split(",")
    #         img = parts[0].strip().replace("listen", "")
    #         duration = float(parts[1].striP())
    #         maximum = int(parts[2].strip())
            
    #         # Region parsing if exists
    #         region = None
    #         if "(" in cmd_str:
    #             reg_str = re.search(r'\((.*?)\)', cmd_str).group(1)
    #             region = tuple(map(int, reg_str.split(',')))

    #         start_time = time.time()
    #         exe_count = 0
    #         listen_stop_flag = threading.Event()

    #         def stop_condition():
    #             while time.time() - start_time < duration:
    #                 if self.stop_flag.is_set(): break
    #                 continue
    #                 time.sleep(0.2)
    #             listen_stop_flag.set()
                
            
    #         threading.Thread(target=stop_condition,args=(duration),daemon=True).start()

    #         while exe_count < maximum and not listen_stop_flag:    
    #             found = False           
    #             try:
    #                 if pg.locateOnScreen(img, region=region, confidence=0.8):
    #                     found = True
    #                     break
    #             except Exception:
    #                 pass # Image not found
    #             if found:
    #                 self.nested_execute(content)
    #                 exe_count += 1
    #             time.sleep(0.5)
    

                
    #     except Exception as e:
    #         print(f"Listen Error: {e}")

    def basic_parsing(self, command):
        """Executes leaf nodes (actual PyAutoGUI commands)."""
        if self.stop_flag.is_set(): return
        cmd = command.lower()
        try:
            if cmd.startswith("c"):
                print("FOUND!!!!")
                # Syntax: cX,Y,T(OPTIONAL) or clickIMG.png...
                parts = command[1:].split(",")
                
                # Coordinate Click
                if parts[0].strip().isdigit():
                    x, y = int(parts[0]), int(parts[1])
                    times = int(parts[2]) if len(parts) > 2 else 1
                    pg.click(x, y, clicks=times)
                # Image Click
                else:
                    target = parts[0]
                    region = None
                    if "(" in command:
                         reg_str = re.search(r'\((.*?)\)', command).group(1)
                         region = tuple(map(int, reg_str.split(',')))
                    try:
                        pos = pg.locateCenterOnScreen(target, region=region, confidence=0.8)
                        if pos: pg.click(pos)
                    except:
                        pass

            elif cmd.startswith("wait") and not cmd.startswith("waituntil"):
                # Syntax: waitTIME (TIME is divisible by 0.1)
                for _ in range(int(float(command[4:]) / 0.1)):
                    if self.stop_flag.is_set(): break
                    time.sleep(0.1)
                    
            elif cmd.startswith("waituntil"):
                # Syntax: waituntilHH:MM:SS
                target_str = command[9:].strip()
                while not self.stop_flag.is_set():
                    now_str = datetime.now().strftime("%H:%M:%S")
                    if now_str >= target_str:
                        break
                    time.sleep(0.5)

            elif cmd.startswith("type") and not cmd.startswith("typerandom"):
                # Syntax: typeTEXT 
                pg.write(command[4:])

            elif cmd.startswith("press"):
                # Syntax: pressKEY or pressdownKEY
                if "down" in cmd:
                    key = command[9:].lower() # pressdown...
                    pg.keyDown(key)
                else:
                    key = command[5:].lower() # press...
                    pg.press(key)

            elif cmd.startswith("release"):
                key = command[7:].lower() # release key
                pg.keyUp(key)

            elif cmd.startswith("dragto"):
                # Syntax: dragToX,Y,BUTTON,DURATION (drag the mouse button to coordinate)
                p = command[6:].split(",")
                pg.dragTo(int(p[0]), int(p[1]), button=p[2], duration=float(p[3]))
                
            elif cmd.startswith("mousedown"):
                # Syntax: mousedownX,Y,BUTTON
                p = command[9:].split(",")
                pg.mouseDown(int(p[0]), int(p[1]), button=p[2])
                
            elif cmd.startswith("mouseup"):
                # Syntax: mouseupX,Y,BUTTON
                p = command[7:].split(",")
                pg.mouseUp(int(p[0]), int(p[1]), button=p[2])

            elif cmd.startswith("typerandom"):
                # Syntax: randomtypeFILE,DELETE (randomly type a line in a text file. DELETE parameter ensure that line get deleted after it is typed)
                args = command[10:].split(",")
                fname = args[0]
                should_delete = args[1].lower() == 'true' if len(args) > 1 else False
                
                if os.path.exists(fname):
                    with open(fname, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    if lines:
                        idx = random.randint(0, len(lines)-1)
                        line_to_type = lines[idx].strip()
                        pg.write(line_to_type)
                        
                        if should_delete:
                            del lines[idx]
                            with open(fname, "w", encoding="utf-8") as f:
                                f.writelines(lines)
        except Exception as e:
            print(f"Command Error ({command}): {e}")

    def stop(self):
        self.stop_flag.set()