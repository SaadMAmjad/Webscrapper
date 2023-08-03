from bs4 import BeautifulSoup
import requests
import time
import tkinter
import customtkinter

# ui system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme('blue')

# initialize
app = customtkinter.CTk()
app.geometry("720x480")
app.title('GUI Webscrapper')

# need to create a 'loop' to run the app so it doesn't close instantly
app.mainloop()