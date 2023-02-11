import re
import os
import requests
from bs4 import BeautifulSoup


def create_folder(name):
    try:
        os.makedirs(name)
    except FileExistsError:
        print("Folder already exists")


def validate_url_wikipedia(url):

    if re.match(r'^https://[a-z]{2,3}\.wikipedia\.org/wiki/.+$', url):
        return True
    else:
        return False


url = input("Enter a Wikipedia link: ")

while True:
    if validate_url_wikipedia(url):
        break
    else:
        print("Link not valid")

    url = input("Enter a Wikipedia link: ")

request = requests.get(url)
soup = BeautifulSoup(request.content, "html.parser")
images = soup.find_all("a", class_="image")
print("Total images " + str(len(images)))
print("You would like to download all of them? (y/n)")

answer = input("> ")

if answer.lower() == "y":

    folder_name = input("Enter a folder name: ")
    create_folder(folder_name)

    for image in images:
        url = "https://es.wikipedia.org/" + image["href"]

        headers = {
            'User-Agent': 'My User Agent 1.0'
        }
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html.parser")
        imageSoup = soup.find("div", class_="fullImageLink")
        imageSoup = imageSoup.find("a")["href"].replace("//", "https://")
        request = requests.get(imageSoup, headers=headers, stream=True)

        title = soup.find("head").find("title").text

        match = re.search(r":(.*?) -", title)

        if match:
            extracted_string = match.group(1)

            print("Downloading image: " + extracted_string)

            with open(folder_name + "/" + extracted_string, "wb") as file:
                file.write(request.content)

    print("Done!")
else:
    print("Bye!")
