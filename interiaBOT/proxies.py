import customtkinter
from tkinter import *
import re
import time
import random
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import topLevel
import undetected_chromedriver as uc


class Proxies:

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = topLevel.ToplevelWindow(self)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def validate_proxy_format(self, proxy):
        pattern = re.compile(r'^(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?$')
        return bool(pattern.match(proxy))

    def save_proxies_to_file(self):
        proxies = self.proxy_textbox.get("1.0", END).strip().split("\n")
        valid_proxies = []
        invalid_proxies = []

        for proxy in proxies:
            if self.validate_proxy_format(proxy):
                valid_proxies.append(proxy)
            else:
                invalid_proxies.append(proxy)

        if invalid_proxies:
            self.open_toplevel()
        try:
            with open("..\infoFiles\proxy.txt", 'w') as file:
                file.write('\n'.join(proxies) + '\n')
        except FileNotFoundError:
            pass

    def clear_proxy(self):
        self.proxy_textbox.delete(1.0, END)

    def load_proxies(self):
        try:
            with open('..\infoFiles\proxy.txt', 'r') as file:
                proxies_content = file.read()
                self.proxy_textbox.delete(1.0, END)
                self.proxy_textbox.insert(INSERT, proxies_content)
        except FileNotFoundError:
            pass

    def __init__(self, tab):

        self.tab = tab
        self.toplevel_window = None

        self.textbox_label = customtkinter.CTkLabel(master=self.tab, text="ENTER PROXIES:")
        self.textbox_label.grid(row=0, column=0)
        self.format_label = customtkinter.CTkLabel(master=self.tab,
                                                   text="FORMAT | PROXY:PORT:USERNAME:PASSWORD OR PROXY:PORT")
        self.format_label.grid(row=1, column=0)
        self.proxy_textbox = customtkinter.CTkTextbox(master=self.tab, width=400, height=500,
                                                      corner_radius=20)
        self.proxy_textbox.grid(row=2, column=0, padx=20)

        # Save proxies button
        self.save_proxy_button = customtkinter.CTkButton(master=self.tab, text="Save proxies",
                                                         command=self.save_proxies_to_file)
        self.save_proxy_button.grid(row=2, column=1, padx=20)

        # Clear proxies button
        self.clear_proxy_button = customtkinter.CTkButton(master=self.tab, text="Clear proxies",
                                                          command=self.clear_proxy)
        self.clear_proxy_button.grid(row=2, column=2, padx=30)

        self.load_proxies()
