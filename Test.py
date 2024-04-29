#!/usr/bin/env python3

import re
import os
import requests
import argparse
import concurrent.futures
from tkinter import *
from tkinter import messagebox

parser = argparse.ArgumentParser()
parser.add_argument('-s', help='hash', dest='hash')
parser.add_argument('-f', help='file containing hashes', dest='file')
parser.add_argument('-d', help='directory containing hashes', dest='dir')
parser.add_argument('-t', help='number of threads', dest='threads', type=int)
args = parser.parse_args()

result = {}

def alpha(hashvalue, hashtype):
    return False

def beta(hashvalue, hashtype):
    response = requests.get('https://hashtoolkit.com/reverse-hash/?hash=' + hashvalue).text
    match = re.search(r'/generate-hash/\?text=(.*?)"', response)
    if match:
        return match.group(1)
    else:
        return False

def gamma(hashvalue, hashtype):
    response = requests.get('https://www.nitrxgen.net/md5db/' + hashvalue, verify=True).text
    if response:
        return response
    else:
        return False

def theta(hashvalue, hashtype):
    response = requests.get('https://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728' % (hashvalue, hashtype)).text
    if len(response) != 0:
        return response
    else:
        return False

md5 = [gamma, alpha, beta, theta]
sha1 = [alpha, beta, theta]
sha256 = [alpha, beta, theta]
sha384 = [alpha, beta, theta]
sha512 = [alpha, beta, theta]

def crack(hashvalue):
    result = False
    if len(hashvalue) == 32:
        for api in md5:
            r = api(hashvalue, 'md5')
            if r:
                return r
    elif len(hashvalue) == 40:
        for api in sha1:
            r = api(hashvalue, 'sha1')
            if r:
                return r
    elif len(hashvalue) == 64:
        for api in sha256:
            r = api(hashvalue, 'sha256')
            if r:
                return r
    elif len(hashvalue) == 96:
        for api in sha384:
            r = api(hashvalue, 'sha384')
            if r:
                return r
    elif len(hashvalue) == 128:
        for api in sha512:
            r = api(hashvalue, 'sha512')
            if r:
                return r
    else:
        return False

def show_result():
    def click():
        hash_value = entry.get()
        result = crack(hash_value)
        if result:
            result_text.config(state=NORMAL)
            result_text.delete('1.0', END)
            result_text.insert(END, result)
            result_text.config(state=DISABLED)

    root = Tk()
    root.title("Hash Cracker Dashboard")
    root.geometry('800x600+0+0')  # Set window size to 800x600 pixels
    root.wm_iconbitmap("logo.ico")
    root.configure(bg='navy')  # Set background color to navy blue

    # Create and customize the title label
    title = Label(root, text="HASH CRACKING DASHBOARD", font=('Arial', 24, 'bold'), fg='white', bg='navy')
    title.pack(pady=20)

    # Create the entry for hash value input
    entry = Entry(root, width=50, font=('Arial', 12))
    entry.pack(padx=20, pady=10)

    # Create the button to trigger hash cracking
    crack_button = Button(root, text="Crack Hash", font=('Arial', 16), fg='white', bg='green', command=click)
    crack_button.pack(pady=10)

    # Create the text box to display hash cracking results
    result_text = Text(root, height=20, width=80, font=('Arial', 14), wrap=WORD, state=DISABLED)
    result_text.pack(fill=BOTH, expand=True, padx=20, pady=10)

    root.mainloop()


if __name__ == "__main__":
    show_result()
