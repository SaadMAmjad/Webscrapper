from bs4 import BeautifulSoup
import requests
import time
import tkinter
import customtkinter
import sv_ttk

# function to clear the table
def clear_all():
   for item in table.get_children():
      table.delete(item)

# method to scrape multiple pages
def search_pages(url):
    # this doesn't display first, something to do with threading? Kinda beyond the scope of this project to fix
    status_label.configure(text='Searching...', text_color='white')
    # create new request and get url for first page
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    # send the soup to the webscrapping method
    find_books(soup)
    # find the list item with the link to the next page
    try:
        next_page_link = soup.find("li", class_="next").a
        if next_page_link is not None:
            href = next_page_link['href']
            # trim the catalogue part because some of the pages have different links to the next one, for some reason
            href = href.replace('catalogue/', '')
            # call this method again on the new url
            search_pages('http://books.toscrape.com/catalogue/' + href)
    except:
        print('No more pages')

# webscrape method
def find_books(soup):
    # new var to hold books pulled from html taken from site before, looking for list elements with the class specified
    books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    # check whether any input was given and tell the user what happens in each case
    if search.get() or search.get() != '':
        status_label.configure(text=f'Showing results for "{search.get()}"', text_color='white')
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
title = customtkinter.CTkLabel(app, text='Enter a title or keywords to look for books, or leave blank to see all (It will take a moment)')
title.pack(padx=10, pady=10)

# SEARCH INPUT
search_input = tkinter.StringVar()
search = customtkinter.CTkEntry(app, width=350, height=40, textvariable=search_input)
search.pack(padx=10, pady=10)

# STATUS LABEL
status_label = customtkinter.CTkLabel(app, text='Waiting to search')
status_label.pack()

# SEARCH BUTTON
# need to wrap inline button function calls in a lambda or it runs right away everytime
download = customtkinter.CTkButton(app, text='Search', command= lambda: search_pages('http://books.toscrape.com/'))
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