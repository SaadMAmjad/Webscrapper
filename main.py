from bs4 import BeautifulSoup
import requests
import time
import tkinter
import customtkinter

# webscrape method
# turning the main code into a function
def find_books():
    html_text = requests.get('http://books.toscrape.com/').text
    soup = BeautifulSoup(html_text, 'lxml')

    # new var to hold books pulled from html taken from site before, looking for list elements with the class specified
    books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    # check whether any input was given and tell them what happens in each case
    if search.get() or search.get() != '':
        status_label.configure(text=f'Looking for "{search.get()}"', text_color='white')
    else:
        status_label.configure(text='Displaying all books', text_color='white')

    # TODO, no longer using file IO, change this to write to a dictionary/tuple/array
    # create a file to save the results to, w mode will create a new file if one doesn't exist, also overwrite previous data
    # f = open('list/readingList.txt', 'w')
    # f.close()

    for current_book in books:

        rating = current_book.find('p', class_='star-rating')
        title = current_book.find('h3').a
        price = current_book.find('p', class_='price_color').text
        stock = current_book.find('p', class_='instock availability').text
        stock = stock.strip()

        # check if the search has something
        if search.get() or search.get() != '':
            # check if it contains the searched word(s)
            if search.get().casefold() in title['title'].casefold():
                print('test')

                # TODO not using file IO so change this
                # # open the file stream and set mode to a or append
                # f = open('list/readingList.txt', 'a')
                # f.write('------------------------------------------ \n')
                # # access the a tag's title attribute since it's not truncated, return fallback if attribute isn't found
                # f.write(f'Title: {title.get("title", "no title found")} \n')
                # f.write(f'Price: {price} \n')
                # # using .get turns it into a list for some reason, use index to get number from it
                # f.write(
                #     f'Rating: {rating.get("class", "class not found")[1]} out of Five \n')
                # f.write(f'Its status is: {stock} \n')
                # f.write(  # can also get sub elements such as href, title, etc like this var['href']
                #     f'More Information: http://books.toscrape.com/{title["href"]} \n')
                # f.write('------------------------------------------ \n')
                # print(f'Book "{title.get("title", "no title found")}" saved')
                # # close the file stream
                # f.close()

        # if search is not present, then show all books
        else:
            print('test')
            # # open the file stream and set mode to a or append
            # f = open('list/readingList.txt', 'a')
            # # f.write will write to the file specified
            # f.write(f'------------------------------------------ \n')
            # # access the a tag's title attribute since it's not truncated, return fallback if attribute isn't found
            # f.write(f'Title: {title.get("title", "no title found")} \n')
            # f.write(f'Price: {price} \n')
            # # using .get turns it into a list for some reason, use index to get number from it
            # f.write(
            #     f'Rating: {rating.get("class", "class not found")[1]} out of Five \n')
            # f.write(f'Its status is: {stock} \n')
            # f.write(  # can also get sub elements such as href, title, etc like this var['href']
            #     f'More Information: http://books.toscrape.com/{title["href"]} \n')
            # f.write('------------------------------------------ \n')
            # print(f'Book "{title.get("title", "no title found")}" saved')
            # f.close()

# ui system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme('blue')

# initialize
app = customtkinter.CTk()
app.geometry("720x480")
app.title('GUI Webscrapper')

# TITLE
title = customtkinter.CTkLabel(app, text='Enter a title or keywords to look for or leave blank to see all books')
# adds it to the app frame I think? pady and x specify padding
title.pack(padx=10, pady=10)

# SEARCH INPUT
search_input = tkinter.StringVar()
search = customtkinter.CTkEntry(app, width=350, height=40, textvariable=search_input)
search.pack(padx=10, pady=10)

# STATUS LABEL
status_label = customtkinter.CTkLabel(app, text='')
status_label.pack()

# DOWNLOAD BUTTON
# command lets you call a function
download = customtkinter.CTkButton(app, text='Download', command=find_books)
download.pack(padx=10, pady=10)

# TODO, add a text area to display scrapped books

# need to create a 'loop' to run the app so it doesn't close instantly
app.mainloop()