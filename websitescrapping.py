
from langchain.document_loaders import SeleniumURLLoader,WebBaseLoader
from langchain.document_loaders import ImageCaptionLoader

from selenium import webdriver
from time import sleep
import os

def extract_text(url):
    name=url.split('.')[1]
    if name=='verizon':
        urls_VER=[url]
        #urls_VER = ['https://www.verizon.com/smartphones/apple-iphone-15-pro-max/']
        loader_VER = SeleniumURLLoader(urls=urls_VER)
        data_VER = loader_VER.load()

        #print(data_VER[0].page_content)
        # Create a new file if it does not exist
        with open(f"{name}.txt", "w") as f:
            f.write(data_VER[0].page_content)
    elif name=='att':
        loader = WebBaseLoader(url)
        data = loader.load()

       # print(data[0].page_content)
        
        with open(f"{name}.txt", "w") as f:
            f.write(data[0].page_content)
        
url="https://www.verizon.com/smartphones/apple-iphone-15-pro-max/"
url2="https://www.att.com/buy/phones/apple-iphone-15-pro-max.html"

extract_text(url2)
