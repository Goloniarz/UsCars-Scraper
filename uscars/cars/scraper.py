import httpx
from selectolax.parser import HTMLParser
from pymongo import  MongoClient
def get_html(baseurl, params=None):
    #nagłówek "User-Agent" dla żądania HTTP
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0"
    }
    resp = httpx.get(baseurl, headers=headers, params=params)
    print(resp.status_code)  
    return HTMLParser(resp.text)  

def extract_text(element, sel):
    #Wydobywanie tekstu z elementu HTML
    try:
        return element.css_first(sel).text().strip("'")
    except AttributeError:
        return None

def parse_page(html):
    cars = []
    for car_element in html.css("div.vehicle-card__content"):
        car = {
            "name": extract_text(car_element, ".vehicle-card__title"),
            "price": extract_text(car_element, ".vehicle-card__bid-digits"),
            "condition": extract_text(car_element, ".vehicle-card__specs"),
            "link": car_element.css_first("a").attributes["href"]
        }
        cars.append(car)
    return cars


def find_max_pages(html):
    """Znajdź maksymalną liczbę stron na podstawie paginacji."""
    
    page_numbers = html.css('div.pagination a.page-number')
    if not page_numbers:
        return 1 
    return max(int(page.text()) for page in page_numbers if page.text().isdigit())

def main():
    client = MongoClient('mongodb://localhost:27017')
    db = client['mydb']
    collection = db['cars']

    baseurl = "https://ucars.pro/pl/sales-history"
    
    # Pobieranie pierwszej strony, aby sprawdzić, ile stron jest dostępnych
    first_page_html = get_html(baseurl)
    max_pages = find_max_pages(first_page_html)
    
    for page in range(1, max_pages + 1):
        print(f"Pobieranie strony {page}")
        html = get_html(baseurl, params={'page': page})
        if html:
            parse_page(html, collection)

if __name__ == "__main__":
    main()
