import customtkinter
from tkinter import *
import re

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x100")
        self.title("InterBOT")
        self.label = customtkinter.CTkLabel(self, text="FIX ERRORS IN FORMAT OF PROXIES")
        self.label.pack(padx=20, pady=20)