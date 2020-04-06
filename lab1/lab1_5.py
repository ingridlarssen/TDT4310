'''Ex 5, '''
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.ntnu.edu/vacancies"
html = urlopen(url).read()

def get_nr_of_vacancies():
    soup = BeautifulSoup(html, features="html.parser")
    list_with_vacancies = [vacancy.get('href') for vacancy in soup.findAll('a') if "ledige-stillinger/stilling/" in vacancy.get('href')]
    return len(list_with_vacancies)


def get_vacancy_titles():
    soup = BeautifulSoup(html, features="html.parser")
    vacancy_titles = [vacancy.get('title') for vacancy in soup.findAll('a') if "ledige-stillinger/stilling/" in vacancy.get('href')]
    return vacancy_titles


def get_deadlines_for_vacancies():
    vacancies = get_vacancy_titles()
    deadlines = [vacancy_deadline.split("Søknadsfrist:",1)[1] for vacancy_deadline in vacancies]
    return deadlines


if __name__ == '__main__':
    print(get_nr_of_vacancies())
    print(get_vacancy_titles())
    print(get_deadlines_for_vacancies())


