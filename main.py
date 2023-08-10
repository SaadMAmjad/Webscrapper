from bs4 import BeautifulSoup
import requests
import time
import tkinter
import customtkinter
import sv_ttk

# variables to hold the data between page switching, and the current page number respectively
data = []
pages = 0

# function to clear the table
def clear_all():
    # clear the data from previous search
    global data
    data = []
    global pages
    pages = 0
    # disable the nav buttons to stop errors
    page_number.configure(text="")
    previous.configure(state='disabled')
    next.configure(state='disabled')
    # reset status label
    status_label.configure(text='Data cleared, waiting to search', text_color='white')
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
        # pagination, divide the pages by the limit per page, then add one if needed
        global data 
        # .get_children method returns ids only
        temp = table.get_children()
        # loop through the ids and retrieve the value for each, then add it to the global data array
        for i in temp:
            data.append(table.item(i))
        global pages
        pages = len(data) // 20 + (1 if len(data) % 20 else 0)
        update_table(1)

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

# TODO, when searching again without clearing, it repeats the initial search and adds duplicate entries
# fix the lazy way by running the clear every time before searching, or scan and remove dupes

# Pagination methods
def update_table(page):
    # Clear the old content
    table.delete(*table.get_children())
    
    # Slice the data according to the page number
    start = (page - 1) * 20
    end = start + 20
    sliced_data = data[start:end]
    
    # Insert the new content
    for item in sliced_data:
        # need to pass values as the key, otherwise will get ghibberish back
        table.insert("", tkinter.END, values=item['values'])
    
    # Update the page label
    page_number.configure(text=f"Page {page} of {pages}")

    # enable the nav buttons
    previous.configure(state='normal')
    next.configure(state='normal')
    

def prev_page():
    # Get the current page number
    # pull the text from the page label, split it (by spaces) and get the second item, which is the page number in this case
    current_page = int(page_number.cget("text").split()[1])
    
    # Check if it is not the first page
    if current_page > 1:
        # Decrement the page number by one
        new_page = current_page - 1
        
        # Update the table content
        update_table(new_page)

def next_page():
    # Get the current page number
    # pull the text from the page label, split it (by spaces) and get the second item, which is the page number in this case
    current_page = int(page_number.cget("text").split()[1])
    
    # Check if it is not the last page
    if current_page < pages:
        # Increment the page number by one
        new_page = current_page + 1
        
        # Update the table content
        update_table(new_page)
                

# ui system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme('blue')

# initialize
app = customtkinter.CTk()
app.geometry("1280x800")
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

# DISPLAY TABLE, LABEL and PAGINATION
tabLabel = customtkinter.CTkLabel(app, text='Results will be displayed below, if nothing is found check your spelling or try a different book')
tabLabel.pack()

# headers used to set lead rows and loop through when adding more rows
headers=['Title', 'Price', 'Rating', 'Stock', 'Link']
# create the table and set row heights
table=tkinter.ttk.Treeview(app, height=20, columns=headers, show='headings')
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
table.column('Link', width=400)
table.heading('Link', text='Link')
table.pack(padx=10, pady=10)

# pagination controls and info
page_number = customtkinter.CTkLabel(app, text='') #will be filled at runtime
page_number.pack(pady = (0, 10))

# TODO, make this do something
previous = customtkinter.CTkButton(app, text='Previous', command=prev_page, state='disabled')
previous.pack(padx=10, pady=10, side='left')

next = customtkinter.CTkButton(app, text='Next', command=next_page, state='disabled')
next.pack(padx=10, pady=10, side='right')


# nifty library to make the ugly table into dark mode
sv_ttk.set_theme("dark")

# need to create a 'loop' to run the app so it doesn't close instantly
app.mainloop()