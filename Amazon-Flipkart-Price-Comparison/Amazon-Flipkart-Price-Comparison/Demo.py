from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
import random

# Initialize the main application window
root = Tk()
root.title('SPEND SMART - Price Comparison Engine')
root.geometry('400x400')
root.configure(background='#0096DC')

# Display the application title
text_label = Label(root, text='SPEND SMART', fg='white', bg='#0096DC')
text_label.pack()
text_label.config(font=('TimesNewRoman', 24))

class Price_compare:
    def __init__(self, master):
        self.master = master
        self.link_flip = ""
        self.setup_ui()

    def setup_ui(self):
        self.frame = Frame(self.master, bg='#0096DC')
        self.frame.pack(pady=20)

        self.var = StringVar()
        self.var_flipkart = StringVar()
        self.var_amzn = StringVar()

        Label(self.frame, text='Enter the product', bg='#0096DC', fg='white').grid(row=0, column=0, padx=(30, 10), pady=30)
        Entry(self.frame, textvariable=self.var).grid(row=0, column=1)
        Button(self.frame, text='Find', bd=4 ,command=self.find).grid(row=1, column=1, sticky=W, pady=8)

    def find(self):
        # Product key creation
        key = '+'.join(self.var.get().split())
        self.window = Toplevel(root)
        self.window.title('Price Comparison Engine')

        # Setup additional UI elements for price display
        Label(self.window, text='Flipkart Title:').grid(row=0, column=0, sticky=W)
        Entry(self.window, textvariable=self.var_flipkart).grid(row=1, column=1, sticky=W)

        # Scrape prices from Flipkart and Amazon
        self.price_flipkart(key)
        self.price_amzn(key)

        # More UI elements
        Button(self.window, text='Search', command=self.search, bd=4).grid(row=2, column=2, sticky=E, padx=10, pady=4)
        Button(self.window, text='Visit Site', command=self.visit_amzn, bd=4).grid(row=4, column=2, sticky=W)

    def price_flipkart(self, key):
        url_flip = f'https://www.flipkart.com/search?q={key}&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        try:
            response = requests.get(url_flip, headers=headers)
            response.raise_for_status()  # Ensure the request was successful
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return

        # Continue processing only if request is successful
        product_map = defaultdict(list)
        home = 'https://www.flipkart.com'
        for block in soup.find_all('div', {'class': '_2kHMtA'}):
            title = block.find('div', {'class': '_4rR01T'}).text if block.find('div', {'class': '_4rR01T'}) else None
            price = block.find('div', {'class': '_30jeq3 _1_WHN1'}).text[1:] if block.find('div', {'class': '_30jeq3 _1_WHN1'}) else 'Currently Unavailable'
            link = home + block.find('a', {'class': '_1fQZEK'}).get('href') if block.find('a', {'class': '_1fQZEK'}) else None
            product_map[title] = [price, link]

        # Determine best matches for the entered product
        matches = get_close_matches(self.var.get().title(), product_map.keys(), 20, 0.1)
        if matches:
            self.var_flipkart.set(product_map[matches[0]][0] + '.00')
            self.link_flip = product_map[matches[0]][1]
        else:
            self.var_flipkart.set('Product not found')

    def price_amzn(self, key):
        url_amz = f'https://www.amazon.in/?&ext_vrnc=hi&tag=googinhydr1-21&ref=pd_sl_8b9xsvs1gj_b&adgrpid=136127568877&hvpone=&hvptwo=&hvadid=617721249835&hvpos=&hvnetw=g&hvrand=10110820156681291013&hvqmt=b&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062237&hvtargid=kwd-29089840&hydadcr=5716_2362046&gclid=CjwKCAjw5v2wBhBrEiwAXDDoJYK5PbVrAUi0KuOewdK8wMr8knBedvbBPsEQd4hiRnvbXUqu49RYyhoCIjQQAvD_BwE'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        try:
            response = requests.get(url_amz, headers=headers)
            response.raise_for_status()  # Ensure the request was successful
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return

        # Continue processing only if request is successful
        product_map = defaultdict(list)
        home = 'https://www.amazon.in'
        for block in soup.find_all('div', {'class': '_2kHMtA'}):
            title = block.find('div', {'class': '_4rR01T'}).text if block.find('div', {'class': '_4rR01T'}) else None
            price = block.find('div', {'class': '_30jeq3 _1_WHN1'}).text[1:] if block.find('div', {'class': '_30jeq3 _1_WHN1'}) else 'Currently Unavailable'
            link = home + block.find('a', {'class': '_1fQZEK'}).get('href') if block.find('a', {'class': '_1fQZEK'}) else None
            product_map[title] = [price, link]

        # Determine best matches for the entered product
        matches = get_close_matches(self.var.get().title(), product_map.keys(), 20, 0.1)
        if matches:
            self.var_amazon.set(product_map[matches[0]][0] + '.00')
            self.link_amz = product_map[matches[0]][1]
        else:
            self.var_amazon.set('Product not found')
        # Similar to price_flipkart but for Amazon
        pass

    def search(self):
        # Implement functionality to search and display results based on user input
        pass

    def visit_amzn(self):
        webbrowser.open(self.product_link)

    def visit_flip(self):
        webbrowser.open(self.link_flip)

if __name__ == "__main__":
    pc = Price_compare(root)
    root.mainloop()
