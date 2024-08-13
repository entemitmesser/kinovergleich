from bs4 import BeautifulSoup
import requests

class astorScraper():
    def __init__(self) -> None:
        self.html_text = requests.get("https://muenchen.premiumkino.de/programm").text
        if self.html_text:
            print("website pulled\n\n")
            #print(self.html_text)
        soup = BeautifulSoup(self.html_text, "lxml")
        self.film_cards = soup.find_all("vertical-list", class_="ng-tns-c184-10 ng-star-inserted")

    def getAllMovieNames(self):
        movie_titles = []
        for card in self.film_cards:
            movie_title = card.find("h2", class_ = "title-with-link__headline").text
            movie_titles.append(movie_title)
        return(movie_titles)

#print(astorScraper().getAllMovieNames())