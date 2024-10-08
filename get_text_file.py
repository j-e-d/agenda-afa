import cloudscraper
import re
import sys

import requests
from bs4 import BeautifulSoup, Comment, NavigableString


def tag_visible(element):
    if isinstance(element, NavigableString):
        if element.parent.name in [
            "style",
            "script",
            "head",
            "title",
            "meta",
            "[document]",
        ]:
            return False
        if isinstance(element, Comment):
            return False
        return True
    return False


def get_visible_text(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    date_span = soup.select_one(".btArticleDate")
    date_text = date_span.text.strip() if date_span is not None else ""

    div = soup.select_one(".btArticleContentInnerInner")
    div_text = ""
    if div is not None:
        texts = div.findAll(string=True)
        visible_texts = filter(tag_visible, texts)
        div_text = "\n".join(re.sub(r"\s+", " ", t) for t in visible_texts if t.strip())

    return date_text + "\n" + div_text


def get_clean_html(url, file_path):
    clean_text = get_visible_text(url)
    if len(clean_text.splitlines()) >= 3:
        with open(file_path, "w") as f:
            f.write(clean_text)
    else:
        print("No se pudo obtener el texto de la página")
        return 1
    return 0


def main():
    get_clean_html("https://www.afa.com.ar/es/posts/la-agenda-de-la-afa", "agenda.txt")


if __name__ == "__main__":
    sys.exit(main())
