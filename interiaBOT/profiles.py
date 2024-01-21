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


class ProfilesMenu:
    def validate_profile_format(self, profile):
        pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+\|[^|]*\|[^|]*\|[^|]*\|[^|]*$')
        return bool(pattern.match(profile))

    def save_profiles(self):
        profiles = self.profile_textbox.get("1.0", END).strip().split("\n")

        valid_profiles = []
        invalid_profiles = []

        for profile in profiles:
            if self.validate_profile_format(profile):
                valid_profiles.append(profile)
            else:
                invalid_profiles.append(profile)
        try:
            with open('..\infoFiles\profiles.txt', 'w') as file:
                file.write('\n'.join(profiles) + '\n')
        except FileNotFoundError:
            pass

    def clear_profiles(self):
        self.profile_textbox.delete(1.0, END)

    def load_profiles(self):
        try:
            with open('..\infoFiles\profiles.txt', 'r') as file:
                profiles_content = file.read()
                self.profile_textbox.delete(1.0, END)
                self.profile_textbox.insert(INSERT, profiles_content)
        except FileNotFoundError:
            pass
    def __init__(self, tab):
        self.tab = tab

        # Textbox profiles
        self.textbox_label = customtkinter.CTkLabel(master=self.tab, text="Enter profiles below:")
        self.textbox_label.grid(row=0, column=0)
        self.profile_textbox = customtkinter.CTkTextbox(master=self.tab, width=500, height=500,
                                                        corner_radius=20)
        self.profile_textbox.grid(row=1, column=0, padx=20)

        # Save profiles button
        self.save_button = customtkinter.CTkButton(master=self.tab, text="Save profiles",
                                                   command=self.save_profiles)
        self.save_button.grid(row=1, column=1, padx=20)

        # Clear profiles button
        self.clear_button = customtkinter.CTkButton(master=self.tab, text="Clear profiles",
                                                    command=self.clear_profiles)
        self.clear_button.grid(row=1, column=2, padx=30)

        self.load_profiles()