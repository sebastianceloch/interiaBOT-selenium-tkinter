import customtkinter
from tkinter import *
import re
import tabs
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("InterBOT")
        #self.wm_iconbitmap('media\interbot.ico')
        customtkinter.set_appearance_mode("dark")

        self.tab_view = tabs.MyTabView(master=self, width=800, height=600, corner_radius=20)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)

app = App()
app.mainloop()