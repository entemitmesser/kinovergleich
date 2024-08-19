from bs4 import BeautifulSoup
import requests

class mScraper():
    def __init__(self) -> None:
        self.html_text = requests.get("https://www.mathaeser.de/mm/programm").text
        if self.html_text:
            print("website pulled\n\n")
            # print(html_text)
        soup = BeautifulSoup(self.html_text, "html.parser")
        self.film_cards = soup.find_all("section", class_="bg-2 movie mb-2")
        self.film_dates = soup.find_all("div", class_ = "prog-nav__day")

    def findDatesForMovies(self):
        movie_date_dict = {}
        for film in self.film_cards:
            date_list = []
            date_list_for_movie = film.find_all("div", class_ = "prog-nav__day")
            movie_title = film.h2.a.text
            #print(movie_title)

            for date in date_list_for_movie:
                #print(date.text)
                date_list.append(date.text)

            movie_date_dict[movie_title] = date_list

        return(movie_date_dict)

    def getAllMovies(self):
        title_list= []
        for card in self.film_cards:
            movie_title = card.h2.a.text
            #print(movie_title)
            title_list.append(movie_title)
        return(title_list)

    def findPriceForMovies(self):
        movie_date_price_dict = {}

        for film in self.film_cards:
            movie_title = film.h2.a.text
            info_field_list = film.find_all("div", class_ = "prog-nav__spacer prog-nav__link")
            price = []

            #print(movie_title)

            for field in info_field_list:
                try:
                    price.append(field.find("div", class_ = "prog-nav__price").text.replace(",", "."))
                except:
                    price.append("Nicht mehr Buchbar")

            movie_date_price_dict[movie_title] = price

        return(movie_date_price_dict)
    
    def findPosterForMovies(self):
        movie_poster_dict = {}

        for film in self.film_cards:
            movie_title = film.h2.a.text
            info_field_list = film.find_all("img", class_ = "img-fluid")
            img = []

            #print(movie_title)

            for field in info_field_list:
                try:
                    img_link: str = field.get("src")
                    if img_link.startswith("https://"):
                        img.append(img_link)
                except:
                    img.append("No Poster Found")

            img_link_out = img[1]
            movie_poster_dict[movie_title] = img_link_out

        return(movie_poster_dict)
