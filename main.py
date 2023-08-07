from bs4 import BeautifulSoup
import requests
import time
import tkinter
import customtkinter
# extra tkinter import to make the link work in table
# from tkinter import *
# library to open websites
# import webbrowser
# library to make tkinter table less ugly
import sv_ttk

# function to open the url
# def callback(url):
#     webbrowser.open_new(url)

# function to clear the table
def clear_all():
   for item in table.get_children():
      table.delete(item)

# webscrape method
def find_books():
    html_text = requests.get('http://books.toscrape.com/').text
    soup = BeautifulSoup(html_text, 'lxml')

    # new var to hold books pulled from html taken from site before, looking for list elements with the class specified
    books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    # check whether any input was given and tell the user what happens in each case
    if search.get() or search.get() != '':
        status_label.configure(text=f'Looking for "{search.get()}"', text_color='white')
    else:
        status_label.configure(text='Displaying all books', text_color='white')

    for current_book in books:

        rating = current_book.find('p', class_='star-rating')
        title = current_book.find('h3').a
        price = current_book.find('p', class_='price_color').text
        # line to get rid of the weird unicode char
        price = price.replace('Â', '')
        stock = current_book.find('p', class_='instock availability').text
        stock = stock.strip()

        # check if the search has something
        if search.get() or search.get() != '':
            # check if it contains the searched word(s)
            if search.get().casefold() in title['title'].casefold():

                # f'http://books.toscrape.com/{title["href"]}
                # make the link clickable from the table
                # create the widget and add it to frame
                # text_widget = Text(app, height=1, width=30)
                # text_widget.pack()
                # # link info and text to represent hyperlink
                # text_widget.insert(END, 'Click for more info')
                # text_widget.tag_add("hyperlink", "1.0", "1.end")
                # # make it look like a link
                # text_widget.tag_config("hyperlink", foreground="blue", underline=True)
                # text_widget.tag_bind("hyperlink", "<Button-1>", open_link(f'http://books.toscrape.com/{title["href"]}'))

                # link1 = Label(app, text="Google Hyperlink", fg="blue", cursor="hand2")
                # link1.pack()
                # link1.bind("<Button-1>", lambda e: callback(f'http://books.toscrape.com/{title["href"]}'))



                book_info = [title.get("title", "no title found"), price, rating.get("class", "class not found")[1] + ' out of five', stock, f'http://books.toscrape.com/{title["href"]}']

                # insert the data into a new table row
                table.insert('', 'end', values=book_info)
                # use enumerate and item to loop, something about tracking index with i? idk
                for i, item in enumerate(book_info):
                    table.column(headers[i],anchor=tkinter.CENTER)

        # if search is not present, then show all books
        else:
            book_info = [title.get("title", "no title found"), price, rating.get("class", "class not found")[1] + ' out of five', stock, f'http://books.toscrape.com/{title["href"]}']

            # insert the data into a new table row
            table.insert('', 'end', values=book_info)
            # use enumerate and item to loop, something about tracking index with i? idk
            for i, item in enumerate(book_info):
                table.column(headers[i],anchor=tkinter.CENTER)

# ui system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme('blue')

# initialize
app = customtkinter.CTk()
app.geometry("1080x720")
app.title('GUI Webscrapper')

# TITLE
title = customtkinter.CTkLabel(app, text='Enter a title or keywords to look for books, or leave blank to see all')
# adds it to the app frame I think? pady and x specify padding
title.pack(padx=10, pady=10)

# SEARCH INPUT
search_input = tkinter.StringVar()
search = customtkinter.CTkEntry(app, width=350, height=40, textvariable=search_input)
search.pack(padx=10, pady=10)

# STATUS LABEL
status_label = customtkinter.CTkLabel(app, text='')
status_label.pack()

# SEARCH BUTTON
download = customtkinter.CTkButton(app, text='Search', command=find_books)
download.pack(padx=10, pady=10)

# CLEAR BUTTON
clear = customtkinter.CTkButton(app, text='Reset Results', command=clear_all)
clear.pack(pady=(0, 10))

# DISPLAY TABLE AND LABEL
tabLabel = customtkinter.CTkLabel(app, text='Results will be displayed below, if nothing is found check your spelling or try a different book')
tabLabel.pack()

# headers used to set lead rows and loop through when adding more rows
headers=['Title', 'Price', 'Rating', 'Stock', 'Link']
# create the table and set row heights
table=tkinter.ttk.Treeview(app, height=25, columns=headers, show='headings')
# column set to give each one a more fitting width
table.column('Title', width=400)
# heading to create the header for each column
table.heading('Title', text='Title')
table.column('Price', width=100)
table.heading('Price', text='Price')
table.column('Rating', width=200)
table.heading('Rating', text='Rating')
table.column('Stock', width=150)
table.heading('Stock', text='Stock')
table.column('Link', width=200)
table.heading('Link', text='Link')
table.pack(padx=10, pady=10)
# TODO, table might be too much of a pain, bing exmaple just made a psuedo table with text widget, look into that

# nifty library to make the ugly table into dark mode
sv_ttk.set_theme("dark")

# need to create a 'loop' to run the app so it doesn't close instantly
app.mainloop()