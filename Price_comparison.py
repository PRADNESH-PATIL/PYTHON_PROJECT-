from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
import random

# Define the attempt_login function and other related login functionality
def attempt_login():
    # Implement your authentication logic here
    if username_entry.get() == "admin" and password_entry.get() == "password":
        login_window.destroy()
        root.deiconify()  # Show the main app window after successful login
    else:
        login_feedback.config(text="Incorrect username or password!", fg="red")

# Initialize the main application window (hidden at first)
root = Tk()
root.withdraw()  # Hide the main window initially

# Set up the login window
login_window = Toplevel(root)
login_window.geometry('400x400')
login_window.configure(background='#0096DC') 


username_label = Label(login_window, text="Username",bg='#0096DC', fg='white')
username_label.grid(row=0,column=0, padx=(30, 10), pady=40)  # Adjust padding as needed

# Text field for username
username_entry = Entry(login_window)
username_entry.grid(row=0, column=1)

# Label for password (added for completeness)
password_label = Label(login_window, text="Password",bg='#0096DC', fg='white')
password_label.grid(row=2,column=0, padx=(30, 10), pady=40)  # Adjust padding as needed

# Text field for password
password_entry = Entry(login_window, show="*")
password_entry.grid(row=2, column=1)

# Feedback label for login attempts
login_feedback = Label(login_window, text="", bg='#0096DC', fg='red')
login_feedback.grid()

# Button to attempt login
login_button = Button(login_window, text="Login",bg='#0096DC', fg='red', command=attempt_login)
login_button.grid(row=3,column=1, padx=(10, 10), pady=10)


# Initialize the main application window
root.title('SPEND SMART - Price Comparison Engine')
root.geometry('400x400')        # Adjust the size as needed for your components
root.configure(background='#0096DC')        # Frame background colour

# Optional: Set an icon for the application window
# root.iconbitmap('path_to_your_icon.ico')   # Uncomment and replace with the path to your icon

# Load and display the application logo
img = Image.open('spendsmart1.png')  # Make sure to adjust the path to where your image is located
resized_img = img.resize((70, 70))   # Resizing the image
img = ImageTk.PhotoImage(resized_img)
img_label = Label(root, image=img, bg='#0096DC')
img_label.pack(pady=(10, 10))

# Display the application title
text_label = Label(root, text='SPEND SMART', fg='white', bg='#0096DC')
text_label.pack()
text_label.config(font=('TimesNewRoman', 24))

class Price_compare:

    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        # Creating a frame for the price comparison functionality
        self.frame = Frame(self.master, bg='#0096DC')
        self.frame.pack(pady=20)

        self.var = StringVar()
        self.var_ebay = StringVar()
        self.var_flipkart = StringVar()
        self.var_amzn = StringVar()

        label = Label(self.frame, text='Enter the product', bg='#0096DC', fg='white')
        label.grid(row=0, column=0, padx=(30, 10), pady=30)

        entry = Entry(self.frame, textvariable=self.var)
        entry.grid(row=0, column=1)

        button_find = Button(self.frame, text='Find', bd=4 ,command=self.find)
        button_find.grid(row=1, column=1, sticky=W, pady=8)
        
        

        # Implement the rest of your methods (find, price_flipkart, price_amzn, etc.) here within the Price_compare class
    def find(self):
        self.product = self.var.get()
        self.product_arr = self.product.split()
        self.n = 1
        self.key = ""
        self.title_flip_var = StringVar()
        self.title_amzn_var = StringVar()
        self.variable_amzn = StringVar()
        self.variable_flip = StringVar()

        for word in self.product_arr:
            if self.n == 1:
                self.key = self.key + str(word)
                self.n += 1

            else:
                self.key = self.key + '+' + str(word)

        self.window = Toplevel(root)
        self.window.title('Price Comparison Engine')
        label_title_flip = Label(self.window, text='Flipkart Title:')
        label_title_flip.grid(row=0, column=0, sticky=W)

        label_flipkart = Label(self.window, text='Flipkart price (Rs):')
        label_flipkart.grid(row=1, column=0, sticky=W)

        entry_flipkart = Entry(self.window, textvariable=self.var_flipkart)
        entry_flipkart.grid(row=1, column=1, sticky=W)

        label_title_amzn = Label(self.window, text='Amazon Title:')
        label_title_amzn.grid(row=3, column=0, sticky=W)

        label_amzn = Label(self.window, text='Amazon price (Rs):')
        label_amzn.grid(row=4, column=0, sticky=W)

        entry_amzn = Entry(self.window, textvariable=self.var_amzn)
        entry_amzn.grid(row=4, column=1, sticky=W)

        self.price_flipkart(self.key)
        self.price_amzn(self.key)

        try:
            self.variable_amzn.set(self.matches_amzn[0])
        except:
            self.variable_amzn.set('Product not available')
        try:
            self.variable_flip.set(self.matches_flip[0])
        except:
            self.variable_flip.set('Product not available')

        option_amzn = OptionMenu(self.window, self.variable_amzn, *self.matches_amzn)
        option_amzn.grid(row=3, column=1, sticky=W)

        lab_amz = Label(self.window, text='Not this? Try out suggestions by clicking on the title')
        lab_amz.grid(row=3, column=2, padx=4)

        option_flip = OptionMenu(self.window, self.variable_flip, *self.matches_flip)
        option_flip.grid(row=0, column=1, sticky=W)

        lab_flip = Label(self.window, text='Not this? Try out suggestions by clicking on the title')
        lab_flip.grid(row=0, column=2, padx=4)

        button_search = Button(self.window, text='Search', command=self.search, bd=4)
        button_search.grid(row=2, column=2, sticky=E, padx=10, pady=4)

        button_amzn_visit = Button(self.window, text='Visit Site', command=self.visit_amzn, bd=4)
        button_amzn_visit.grid(row=4, column=2, sticky=W)

        button_flip_visit = Button(self.window, text='Visit Site', command=self.visit_flip, bd=4)
        button_flip_visit.grid(row=1, column=2, sticky=W)
    
    
    
    
    def price_amzn(self, key):
        url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)

        # Faking the visit from a browser
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        map = defaultdict(list)
        home = 'https://www.amazon.in'
        proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                        "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                        "134.213.29.202:4444"]
        proxies = {'https': random.choice(proxies_list)}
        source_code = requests.get(url_amzn, headers=headers)
        plain_text = source_code.text
        self.opt_title = StringVar()
        self.soup = BeautifulSoup(plain_text, "html.parser")
        # print(self.soup)
        # print(self.soup.find_all('div', {'class': 'sg-col-inner'}))
        for html in self.soup.find_all('div', {'class': 'sg-col-inner'}):
            title, link,price = None, None,None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text
            for l in html.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
                link = home + l.get('href')
            if title and link:
                map[title] = [price, link]
        user_input = self.var.get().title()
        self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
        self.looktable = {}
        for title in self.matches_amzn:
            self.looktable[title] = map[title]
        self.opt_title.set(self.matches_amzn[0])
        self.var_amzn.set(self.looktable[self.matches_amzn[0]][0] + '.00')
        self.product_link = self.looktable[self.matches_amzn[0]][1]
        
        
    def price_flipkart(self, key):
        url_flip = 'https://www.flipkart.com/search?q=' + str(
            key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
        map = defaultdict(list)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        source_code = requests.get(url_flip, headers=self.headers)
        soup = BeautifulSoup(source_code.text, "html.parser")
        self.opt_title_flip = StringVar()
        home = 'https://www.flipkart.com'
        for block in soup.find_all('div', {'class': '_2kHMtA'}):
            title, price, link = None, 'Currently Unavailable', None
            for heading in block.find_all('div', {'class': '_4rR01T'}):
                title = heading.text
            for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                price = p.text[1:]
            for l in block.find_all('a', {'class': '_1fQZEK'}):
                link = home + l.get('href')
            map[title] = [price, link]

        user_input = self.var.get().title()
        self.matches_flip = get_close_matches(user_input, map.keys(), 20, 0.1)
        self.looktable_flip = {}
        for title in self.matches_flip:
            self.looktable_flip[title] = map[title]

        try:
            self.opt_title_flip.set(self.matches_flip[0])
            self.var_flipkart.set(self.looktable_flip[self.matches_flip[0]][0] + '.00')
            self.link_flip = self.looktable_flip[self.matches_flip[0]][1]
        except IndexError:
            self.opt_title_flip.set('Product not found')
            
            

    def search(self):
        amzn_get = self.variable_amzn.get()
        self.opt_title.set(amzn_get)
        product = self.opt_title.get()
        price, self.product_link = self.looktable[product][0], self.looktable[product][1]
        self.var_amzn.set(price + '.00')
        flip_get = self.variable_flip.get()
        flip_price, self.link_flip = self.looktable_flip[flip_get][0], self.looktable_flip[flip_get][1]
        self.var_flipkart.set(flip_price + '.00')

    def visit_amzn(self):
        webbrowser.open(self.product_link)
        
    def visit_flip(self):
        webbrowser.open(self.link_flip)


if __name__ == "__main__":
    pc = Price_compare(root)
    root.mainloop()
