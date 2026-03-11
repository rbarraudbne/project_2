import requests
import csv
from bs4 import BeautifulSoup


#extraction des informations de la page d'un livre
product_page_url = "https://books.toscrape.com/catalogue/the-requiem-red_995/index.html"
response = requests.get(product_page_url)
soup = BeautifulSoup(response.content, 'html.parser')

# informations du tableau
upc = soup.find("th", string="UPC").find_next("td").text
price_including_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text
number_available = soup.find("th", string="Availability").find_next("td").text
number_of_reviews = soup.find("th", string="Number of reviews").find_next("td").text

# titre
title = soup.find("h1").text

# description
description_tag = soup.find("div", id="product_description")
if description_tag:
    product_description = description_tag.find_next("p").text
else:
    product_description = ""

# catégorie
category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

# note
review_rating = soup.find("p", class_="star-rating")["class"][1]

# image
image_url = "https://books.toscrape.com/" + soup.find("img")["src"].replace("../", "")

# écriture CSV pour un livre
with open(f"{title}.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow([
        "UPC",
        "Title",
        "Price including tax",
        "Price excluding tax",
        "Number available",
        "Description",
        "Category",
        "Review rating",
        "Image URL"
    ])

    writer.writerow([
        upc,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url
    ])

#création d'une fonction à partir du code précédent qui prend l'url d'un livre et retourne ses informations

def get_book_data(book_url):

    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, "html.parser")

    upc = soup.find("th", string="UPC").find_next("td").text
    title = soup.find("h1").text
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text
    number_available = soup.find("th", string="Availability").find_next("td").text
    description_tag = soup.find("div", id="product_description")
    if description_tag:
        product_description = description_tag.find_next("p").text
    else:
        product_description = ""
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = "https://books.toscrape.com/" + soup.find("img")["src"].replace("../", "")
    return [upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

#on va maintenant extraire les données de tous les livres d'une catégorie
category_url = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"
response_category = requests.get(category_url)
soup_category = BeautifulSoup(response_category.content, 'html.parser')
chosen_category = soup_category.find("li", class_="active").text.strip()

with open(f"{chosen_category}.csv", "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "UPC",
        "Title",
        "Price including tax",
        "Price excluding tax",
        "Number available",
        "Description",
        "Category",
        "Review rating",
        "Image URL"
    ])

    next_page = category_url

    while next_page:

        response = requests.get(next_page)
        soup_category = BeautifulSoup(response.content, "html.parser")

        for book in soup_category.find_all("h3"):
            book_url = "https://books.toscrape.com/catalogue/" + book.a["href"].replace("../../../", "")

            writer.writerow(get_book_data(book_url))

        next_button = soup_category.find("li", class_="next")

        if next_button:
            page = next_button.find("a")["href"]
            next_page = "https://books.toscrape.com/catalogue/category/books/romance_8/" + page
        else:
            next_page = None

#définition d'une fonction qui prend l'url  d'une catégorie en paramètre et retourne le fichier csv avec toutes les infos de tous les livres de cette catégorie

def get_category_data(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    chosen_category = soup.find("li", class_="active").text.strip()

    with open(f"{chosen_category}.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "UPC",
            "Title",
            "Price including tax",
            "Price excluding tax",
            "Number available",
            "Description",
            "Category",
            "Review rating",
            "Image URL"
        ])

        next_page = category_url

        while next_page:

            response = requests.get(next_page)
            soup_category = BeautifulSoup(response.content, "html.parser")

            for book in soup_category.find_all("h3"):
                book_url = "https://books.toscrape.com/catalogue/" + book.a["href"].replace("../../../", "")

                writer.writerow(get_book_data(book_url))

            next_button = soup_category.find("li", class_="next")

            if next_button:
                page = next_button.find("a")["href"]
                next_page = category_url.replace("index.html", "") + page
            else :
                next_page = None


# on va maintenant extraire les données de toutes les catégories
accueil_url = "https://books.toscrape.com/"
response_accueil = requests.get(accueil_url)
soup_accueil = BeautifulSoup(response_accueil.content, 'html.parser')

for category in soup_accueil.select(".nav-list ul li a"):
    category_url = "https://books.toscrape.com/" + category["href"]
    get_category_data(category_url)

