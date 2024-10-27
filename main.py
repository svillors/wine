from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
from collections import defaultdict


def declension(years):
    if years % 10 == 1 and years % 100 != 11:
        return 'год'
    elif years % 10 in [2, 3, 4] and not 15 > years % 100 > 10:
        return 'года'
    else:
        return 'лет'


def main():
    wines = pandas.read_excel('wine3.xlsx', keep_default_na=False)
    wines_dict = wines.to_dict(orient='records')
    new_wines = defaultdict(list)
    for wine in wines_dict:
        new_wines[wine['Категория']].append(wine)
    new_wines_dict = dict(new_wines)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    winery_age = (datetime.datetime.now()
                  - datetime.datetime(year=1920, month=1, day=1)).days//365

    rendered_page = template.render(
        time="Уже {} {} с вами".format(winery_age, declension(winery_age)),
        new_wines_dict=new_wines_dict,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
