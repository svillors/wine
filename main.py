from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
from collections import defaultdict
from dotenv import load_dotenv
import os


def declension(years):
    if years % 10 == 1 and years % 100 != 11:
        return 'год'
    elif years % 10 in [2, 3, 4] and not 15 > years % 100 > 10:
        return 'года'
    else:
        return 'лет'


def main():
    load_dotenv()
    wines = pandas.read_excel(os.getenv('WINES_FILE'), keep_default_na=False)
    wines = wines.to_dict(orient='records')
    grouped_wines = defaultdict(list)
    for wine in wines:
        grouped_wines[wine['Категория']].append(wine)
    grouped_wines = dict(grouped_wines)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    winery_age = datetime.datetime.now().year - 1920

    rendered_page = template.render(
        time="Уже {} {} с вами".format(winery_age, declension(winery_age)),
        grouped_wines=grouped_wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
