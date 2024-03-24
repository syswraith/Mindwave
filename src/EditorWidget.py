import tkinter as tk 
from tkinter import *
from app_settings import Settings , App_font 
from datetime import datetime
from tkinter import *
import re
import os
class Editorwidget(tk.Text):
    def __init__(self, master=None,**kw):
        super().__init__(master ,**kw) 

        #general configs
        self.config(bg=Settings['Editor_color'])
        self.config(fg=Settings['Text_color'])
        self.config(width=40)
        self.config(height=10)
        self.config(highlightthickness=1)
        self.config(insertwidth=2)
        self.config(font=App_font)
        self.config(padx=10)
        self.config(pady=10)
        self.config(wrap=WORD)
        self.config(highlightbackground="black")
        self.config(insertbackground=Settings['Text_color'])

        self.tag_configure("bold", font=(App_font + ("bold",)))
        self.tag_configure("italic", font=(App_font + ("italic",)))
        self.tag_configure("underline", underline=True)

        #keyboard bindings 
        self.bind('<Control-a>', self.select_all_text)
        self.bind("<Control-b>", self.toggle_bold)
        self.bind("<Control-i>", self.toggle_italic)
        self.bind("<Control-u>", self.toggle_underline)

        self.bind("<Control-s>", self.save_todays)
        self.bind("<Control-o>", self.open_todays)


        #set focus 
        self.focus_set()

    def select_all_text(self, event=None):
        self.tag_remove("sel", "1.0", "end")
        for line in self.get("1.0", "end").split("\n"):
            start_index = "1.0"
            while True:
                start_index = self.search(r'\S', start_index, stopindex="end", regexp=True)
                if not start_index:
                    break
                end_index = self.search(r'\s', start_index, stopindex="end", regexp=True)
                if not end_index:
                    end_index = "end"
                self.tag_add("sel", start_index, end_index)
                start_index = f"{end_index}+1c"
        return "break"

    def toggle_bold(self,event=None):
        if self.cget('state') == "disabled":
            return 

        cursor_position = self.index(tk.INSERT)
        if self.is_selected_text_bold():
            self.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.tag_add("bold", "sel.first", "sel.last")
            self.tag_configure("bold", font=("Arial", 15, "bold"))

        self.tag_remove("sel", "1.0", "end")
        return "break"

    def toggle_italic(self,event=None):
        if self.cget('state') == "disabled":
            return 

        cursor_position = self.index(tk.INSERT)
        
        if self.tag_ranges("italic"):
            self.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.tag_add("italic", "sel.first", "sel.last")
            self.tag_configure("italic", font=("Arial", 15, "italic"))

        self.tag_remove("sel", "1.0", "end")
        self.mark_set(tk.INSERT, cursor_position)
        return "break"

    def toggle_underline(self,event=None):
        if self.cget('state') == "disabled":
            return 

        cursor_position = self.index(tk.INSERT)
        if self.tag_ranges("underline"):
            self.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.tag_add("underline", "sel.first", "sel.last")
            self.tag_configure("underline", underline=True)
        self.tag_remove("sel", "1.0", "end")
        self.mark_set(tk.INSERT, cursor_position)
        return "break"

    def is_selected_text_bold(self):

        # Get the ranges of the "bold" tag
        bold_ranges = self.tag_ranges("bold")
        # Get the selection range
        sel_start = self.index("sel.first")
        sel_end = self.index("sel.last")
        # Check if any of the bold ranges intersect with the selection
        for i in range(0, len(bold_ranges), 2):
            if self.compare(bold_ranges[i], "<=", sel_end) and self.compare(bold_ranges[i+1], ">=", sel_start):
                return True
        return False


    def is_selected_text_underline(self):
        underline_ranges = self.tag_ranges("underline")
        sel_start = self.index("sel.first")
        sel_end = self.index("sel.last")
        for i in range(0, len(underline_ranges), 2):
            if self.compare(underline_ranges[i], "<=", sel_end) and self.compare(underline_ranges[i+1], ">=", sel_start):
                return True
        return False

    def open_todays(self,event=None):
        #set date today's date
        #cal.selection_set(datetime.today().date())
        today_date_file = Settings['Diary_folder'] + '/' +datetime.now().strftime("%d-%m-%y") + ".md"
        self.configure(state='normal')
        self.delete('1.0', 'end')
        self.focus_set()
        try:
            with open(today_date_file, 'r') as Today_file:
                self.apply_formatting(Today_file.read())
        except FileNotFoundError:
            with open(today_date_file, 'w'):
                pass  # Creating the file

    def apply_formatting(self,md_content):
        bold = italic = underline = False
        formatted_text = ""
        i = 0

        while i < len(md_content):
            if md_content[i:i+2] == "**" and not italic and not underline:
                bold = not bold
                i += 2
                continue

            if md_content[i:i+1] == "*" and not bold and not underline:
                italic = not italic
                i += 1
                continue

            if md_content[i:i+2] == "__" and not bold and not italic:
                underline = not underline
                i += 2
                continue

            if bold:
                formatted_text += md_content[i]
                self.insert(tk.END, md_content[i], "bold")
            elif italic:
                formatted_text += md_content[i]
                self.insert(tk.END, md_content[i], "italic")
            elif underline:
                formatted_text += md_content[i]
                self.insert(tk.END, md_content[i], "underline")
            else:
                formatted_text += md_content[i]
                self.insert(tk.END, md_content[i])

            i += 1
    def save_todays(self,Event=None):
        if self.cget('state')=="disabled":
            return 

        markdown_content = ""
        start_index = "1.0"
        while True:
            bold_start = self.search(r'\S', start_index, stopindex="end", regexp=True, count=1, nocase=True)
            italic_start = self.search(r'\S', start_index, stopindex="end", regexp=True, count=1, nocase=True)
            underline_start = self.search(r'\S', start_index, stopindex="end", regexp=True, count=1, nocase=True)
            
            # Find the earliest starting index among all formatting types
            next_start = min((bold_start, italic_start, underline_start), key=lambda x: float("inf") if not x else float(x.split(".")[1]))
            
            if not next_start:
                break
            
            # Add the section of text before the next formatting
            end_index = self.search(r'\s', next_start, stopindex="end", regexp=True, count=1, nocase=True)
            if not end_index:
                end_index = "end"
            
            markdown_content += self.get(start_index, next_start)
            
            # Add Markdown syntax for formatting
            if "bold" in self.tag_names(next_start):
                markdown_content += "**"
            if "italic" in self.tag_names(next_start):
                markdown_content += "*"
            if "underline" in self.tag_names(next_start):
                markdown_content += "__"
            
            # Add the section of text with formatting
            markdown_content += self.get(next_start, end_index)
            
            # Close Markdown syntax for formatting
            if "underline" in self.tag_names(next_start):
                markdown_content += "__"
            if "italic" in self.tag_names(next_start):
                markdown_content += "*"
            if "bold" in self.tag_names(next_start):
                markdown_content += "**"
            
            start_index = end_index
        
        today_date_file = Settings['Diary_folder'] + '/' +datetime.now().strftime("%d-%m-%y") + ".md"
        with open(today_date_file, "w") as file:
            file.write(markdown_content) 
        self.config(state='disabled')

    def open_date(self,date):

        file_name = Settings['Diary_folder']+'/' + date.replace('/','-') + '.md'

        self.configure(state='normal')
        self.delete('1.0', 'end')
        if os.path.exists(file_name):
            with open(file_name) as Diary_File:
                self.apply_formatting(Diary_File.read())
                if date == datetime.now().strftime("%d/%m/%y"):
                    self.configure(state="normal")
                    self.focus_set()
                else:
                    self.configure(state="disabled")

        else:
            if date == datetime.now().strftime("%d/%m/%y"):
                self.configure(state='normal')
                self.set_tempate()
                self.focus_set()
            else:
                self.configure(state='normal')
                self.insert('4.6',"No Entry found..")
                self.config(state='disabled')

    def set_template(self):
        with open(Settings['Template']) as Diary_File:
            self.apply_formatting(Diary_File.read())
