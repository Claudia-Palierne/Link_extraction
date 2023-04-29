#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

GET_IDX = 4
HTTP_IDX: int = -5


def sort_url(url_str):
    """
    This function will sort the urls.
    """
    file_name = url_str.split("/")[-1]
    sort_key = file_name.split("-")[-1]
    return sort_key


def read_urls(filename):
    """
    Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order.
    """
    urls = []
    host = filename.split("_")[-1]
    try:
        with open(filename, "r") as f:
            for line in f:
                path = re.search(r"GET \S+ HTTP", line).group()[GET_IDX:HTTP_IDX]
                if "puzzle" in path:
                    urls.append("https://" + host + path)
        return sorted(list(set(urls)), key=sort_url)
    except FileNotFoundError as error:
        print("You cannot open the file :", error)
        return []


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        #os.makedirs(dest_dir)
        dest_dir = os.getcwd()
    try:
        with open(dest_dir+"/index.html", "w") as index:
            index.write("<html>\n<body>\n")
            for idx, url in enumerate(img_urls):
                img_path = dest_dir+"/img"+str(idx)+".jpg"
                urllib.request.urlretrieve(url, img_path)
                index.write("<img src=\"img"+str(idx)+".jpg\">")
                print(f"Downloading img{idx} at : {url}")
            index.write("\n</body>\n</html>")
    except FileNotFoundError as error:
        print("The file cannot open :", error)


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
