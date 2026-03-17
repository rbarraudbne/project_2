import requests
import csv
from bs4 import BeautifulSoup
import os
os.makedirs("images", exist_ok=True)


#création d'une fonction qui prend l'url d'un livre et retourne ses informations

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
    image_response = requests.get(image_url)
    image_name = title.replace("/", "").replace(":", "") + ".jpg"
    with open("images/" + image_name, "wb") as f:
        f.write(image_response.content)

    return [upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]


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
