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
import profiles
import tasks
import proxies
class MyTabView(customtkinter.CTkTabview):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Tasks")
        self.add("Proxies")
        self.add("Profiles")
        # add widgets on tabs
        self.profiles_menu = profiles.ProfilesMenu(self.tab("Profiles"))
        self.tasks_menu = tasks.Tasks(self.tab("Tasks"))
        self.proxies_menu = proxies.Proxies(self.tab("Proxies"))


