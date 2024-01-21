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
import seleniumwire.undetected_chromedriver as uc
class Tasks:
    def proxies_for_task(self):
        proxy_list = []
        if self.proxy_option == "Proxy List":
            try:
                with open("..\infoFiles\proxy.txt", 'r') as file:
                    proxy_list = file.read().splitlines()
            except FileNotFoundError:
                print("File not found")
        else:
            return ""
        return proxy_list

    def profiles_for_task(self):
        profile_list = []
        # do rozwiniecia wybranie tylko niektorych profili np albo pojedynczego i zwrocenie listy? chuj wi moze
        if self.profile_option == "All profiles":
            try:
                with open("..\infoFiles\profiles.txt", 'r') as file:
                    profile_list = file.read().splitlines()
            except FileNotFoundError:
                print("File not found")
        else:
            return False
        return profile_list

    def create_options(self, proxy_list, index):
        options = {'disable_capture': True, 'proxy': {}}

        proxy_str = proxy_list[index]
        parts = proxy_str.split(':')
        login, password, ip, port = parts[0], parts[1], parts[2], parts[3]

        http_proxy = f'http://{login}:{password}@{ip}:{port}'
        https_proxy = f'https://{login}:{password}@{ip}:{port}'

        options['proxy']['http'] = http_proxy
        options['proxy']['https'] = https_proxy

        return options
    def create_interia_emails(self, index):
        proxy_list = self.proxies_for_task()
        profile_list = self.profiles_for_task()
        profile_result = []
        for entry in profile_list:
            entry_data = entry.split('|')
            profile_result.append({
                'email': entry_data[0],
                'name': entry_data[1],
                'surname': entry_data[2],
                'password': entry_data[3]
            })
        profile_name = profile_result[index]['name']
        print(profile_list)
        if proxy_list != "":
            proxy_result = []
            for proxy in proxy_list:
                proxy_data = proxy.split(':')
                proxy_result.append({
                    'login': proxy_data[0],
                    'password': proxy_data[1],
                    'ip': proxy_data[2],
                    'port': proxy_data[3]
                })
            proxy_login = proxy_result[index]['login']
            proxy_password = proxy_result[index]['password']
            proxy_ip = proxy_result[index]['ip']
            proxy_port = proxy_result[index]['port']
            options = {
                'proxy': {
                    'http': f'http://{proxy_login}:{proxy_password}@{proxy_ip}:{proxy_port}',
                    'https': f'https://{proxy_login}:{proxy_password}@{proxy_ip}:{proxy_port}',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
        else:
            options = {}
        months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień',
                  'Październik', 'Listopad', 'Grudzień']
        print(proxy_list)
        driver = uc.Chrome(seleniumwire_options=options)
        self.task_textbox.configure(state="normal")
        self.task_textbox.delete(1.0, 2.0)
        self.task_textbox.insert(INSERT, f'Starting task:...{index+1}/{len(self.profiles_for_task())}\n')
        self.task_textbox.configure(state="disable")
        driver.get("https://konto-pocztowe.interia.pl/#/nowe-konto/darmowe")
        driver.find_element(By.XPATH, "//button[@class='rodo-popup-agree rodo-popup-main-agree']").click()
        # name surname
        names = driver.find_elements(By.CLASS_NAME, "_2E5no53p0eu72a")
        names[0].send_keys(profile_result[index]['name'])
        names[1].send_keys(profile_result[index]['surname'])
        # birthdayday birthdaymonth
        driver.find_element(By.XPATH, "// input[ @ id = 'birthdayDay']").send_keys(random.randint(1, 28), Keys.TAB)
        month_xpath = "//span[@class='account-select__options__label'][normalize-space()='{}']".format(
            random.choice(months))
        driver.find_element(By.XPATH, month_xpath).click()
        # birthdayyear
        driver.find_element(By.XPATH, "//input[@id='birthdayYear']").send_keys(random.randint(1990, 2002), Keys.TAB)
        driver.find_element(By.XPATH,
                            "//span[@class='account-select__options__label'][contains(text(),'Mężczyzna')]").click()
        # accountname
        names[2].send_keys(profile_result[index]['email'])
        # password
        driver.find_element(By.XPATH, "//input[@id='password']").send_keys(profile_result[index]['password'])
        driver.find_element(By.XPATH, "//input[@id='rePassword']").send_keys(profile_result[index]['password'])
        driver.find_element(By.XPATH,
                            "//label[@class='checkbox-container checkbox-container--remove-margin']//div[@class='checkbox-label']").click()

    def subprocess_create_emails(self):
        # dodac target w wywolaniu moze?
        loop_range = len(self.profiles_for_task())
        thread_list = list()
        # petla ile threadow
        for x in range(loop_range):
            # tworzenie threadu
            t = threading.Thread(name='Test {}'.format(x), target=self.create_interia_emails(x))
            # start
            t.start()
            # delay taska o 2 sekundy
            time.sleep(0.2)
            print(t.name + ' started!')
            thread_list.append(t)
        for thread in thread_list:
            thread.join()
        print('Test completed!')

    def check_interia_emails(self):
        proxy_list = self.proxies_for_task()
        profile_list = self.profiles_for_task()

    # FUNKCJA Z SELENIUM DO JEDNEGO TASKA
    # FUNKCJA Z SELENIUM DO DRUGIEGO TASKA
    # W STARCIE TYLKO IFY I WYWOLANIE ODPOWIEDNICH FUNKCJI
    def start_button(self):

        if self.task_option == "Create interia emails":
            self.subprocess_create_emails()
        if self.task_option == "Check interia emails":
            # tu tez zrobic subprocess
            self.check_interia_emails()

    def stop_button(self):
        self.task_textbox.configure(state="normal")
        self.task_textbox.insert(INSERT, "Task stopped")
        self.task_textbox.configure(state="disable")

    def modemenu_callback(self,choice):  # wybor z menu i wtedy co sie dzieje jak to klikniesz
        print("optionmenu dropdown clicked:", choice)
        self.task_option = str(choice)

    def profilesmenu_callback(self, profile_choice):  # wybor z menu i wtedy co sie dzieje jak to klikniesz
        print("optionmenu dropdown clicked:", profile_choice)
        self.profile_option = str(profile_choice)

    def proxiesmenu_callback(self, proxy_choice):  # wybor z menu i wtedy co sie dzieje jak to klikniesz
        print("optionmenu dropdown clicked:", proxy_choice)
        self.proxy_option = str(proxy_choice)

    def __init__(self, tab):
        self.tab = tab

        self.proxy_option = "Proxy List"
        self.task_option = None
        self.profile_option = "All profiles"

        # modeslidermenuchoice
        self.mode_label = customtkinter.CTkLabel(master=self.tab, text="Select mode")
        self.mode_label.grid(row=0, column=0, padx=10)



        task_optionmenu = customtkinter.CTkOptionMenu(master=self.tab,
                                                      values=["Create interia emails", "Check interia emails"],
                                                      command=self.modemenu_callback)
        task_optionmenu.set("No mode selected")
        task_optionmenu.grid(row=1, column=0, padx=10, pady=5)

        # profilesslidermenuchoice
        self.profile_label = customtkinter.CTkLabel(master=self.tab, text="Select profiles")
        self.profile_label.grid(row=3, column=0)



        profile_optionmenu = customtkinter.CTkOptionMenu(master=self.tab, values=["All profiles", "option 2"],
                                                         command=self.profilesmenu_callback)
        profile_optionmenu.set("All profiles")
        profile_optionmenu.grid(row=4, column=0)

        # proxiesslidermenuchoice
        self.proxies_label = customtkinter.CTkLabel(master=self.tab, text="Select proxies")
        self.proxies_label.grid(row=0, column=1, padx=20)

        proxy_optionmenu = customtkinter.CTkOptionMenu(master=self.tab, values=["Local IP", "Proxy List"],
                                                       command=self.proxiesmenu_callback)
        proxy_optionmenu.set("Proxy List")
        proxy_optionmenu.grid(row=1, column=1, padx=20)

        # Status info textbox
        self.task_textbox = customtkinter.CTkTextbox(master=self.tab, width=400, height=250, corner_radius=20,
                                                     state="disabled")
        self.task_textbox.grid(row=2, column=2, padx=50)
        # Start task button
        self.start_button = customtkinter.CTkButton(master=self.tab, text="Start Task",
                                                    command=threading.Thread(target=self.start_button).start)
        self.start_button.grid(row=3, column=2, pady=20)

        # Stop task button
        self.stop_button = customtkinter.CTkButton(master=self.tab, text="Stop Task", command=self.stop_button)
        self.stop_button.grid(row=4, column=2, pady=5)