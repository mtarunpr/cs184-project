from bs4 import BeautifulSoup
from typing import NamedTuple
import requests


class Tactic(NamedTuple):
    id: int
    keyword: str
    num_args: int


def scrape_tactics() -> list[Tactic]:
    url = "https://coq.inria.fr/doc/V8.18.0/refman/coq-tacindex.html"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    rows = soup.find_all("tr")
    for row in rows:
        links = row.find_all("a", href=True)
        for link in links:
            code = link.find("code", class_=True)
            keyword = code.contents[0]
            deets_url = f"https://coq.inria.fr/doc/V8.18.0/refman/{link['href']}"
            deets_html = requests.get(deets_url)
            print(deets_html.text)

    return []


if __name__ == "__main__":
    scrape_tactics()
