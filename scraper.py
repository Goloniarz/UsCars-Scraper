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
    
def parse_page(html, collection):
    # Szukanie elementów HTML reprezentujących pojazdy 
    for car_element in html.css("div.vehicle-card__content"):
        car = {
            "name": extract_text(car_element, ".vehicle-card__title"),
            "price": extract_text(car_element, ".vehicle-card__bid-digits"),
            "condition": extract_text(car_element, ".vehicle-card__specs"),
            "link": car_element.css_first("a").attributes["href"]
        }
        # Wypisujemy informacje o pojazdach
        print(f"name: {car['name']}\nprice: {car['price']}\ncondition: {car['condition']}\nlink: {car['link']}\n---------")
        
        # Zapisujemy pojazd do MongoDB
        collection.insert_one(car)

def main():
    # Nawiązanie połączenia z MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['mydb']
    collection = db['cars']


    baseurl = "https://ucars.pro/pl/sales-history"
    num_pages = 10  # Liczba stron do przetworzenia
    
    for page in range(1, num_pages + 1):
        print(f"Pobieranie strony {page}")
        html = get_html(baseurl, params={'page': page})
        if html:
            parse_page(html, collection)

if __name__ == "__main__":
    main()


    ###Importing Data to MySql in progress