import tkinter as tk
from app_settings import Settings , App_font
from datetime import datetime 
from EditorWidget import Editorwidget
class Menubar(tk.Frame):
    def __init__(self,master=None, **kw):
        super().__init__(master, **kw)

        self.editor_widget = None

        self.configure(bg=Settings['Background_color'])
        self.configure(height=50)

        self.Datelabel = tk.Label(self) 
        #self.setup_label()
        
        self.edit_icon= tk.PhotoImage(file="icons/edit_todays.png")
        self.edit_todays = tk.Button(self ,image=self.edit_icon ,bg=Settings['Background_color'] , bd=0 , highlightbackground=Settings['Background_color'] , activebackground=Settings['Background_color'],command=self.open_todays)
        self.edit_todays.pack(side='left',padx=0,pady=10)

        self.save_icon= tk.PhotoImage(file="icons/save_todays.png")
        self.save_todays= tk.Button(self ,image=self.save_icon ,bg=Settings['Background_color'] , bd=0 , highlightbackground=Settings['Background_color'] , activebackground=Settings['Background_color'],command=self.save_todays)
        self.save_todays.pack(side='left',padx=2,pady=10)



    def setup_label(self):
        self.Datelabel.config(bg=Settings['Background_color'])
        self.Datelabel.config(fg=Settings['Theme_color'])
        self.Datelabel.pack(side="left",padx=10,pady=10)
        self.Datelabel.config(font=App_font)
        #set todays day by default
        todays_date = datetime.now().strftime("%d %B , %Y")
        self.update_Datelabel(todays_date)

    def update_Datelabel(self,text):
        self.Datelabel.config(text=text)

    def set_editor_widget(self,editor_widget):
        self.editor_widget = editor_widget

    def save_todays(self):
        if self.editor_widget:
            self.editor_widget.save_todays()

    def open_todays(self):
        if self.editor_widget:
            self.editor_widget.open_todays()
