import requests
import yfinance as yf

# завдання 1
def check_page_availability(url):
    print("1. Перевірка доступності сторінки:")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Сторінка {url} доступна\n")
        else:
            print(f"Сторінка {url} недоступна, код: {response.status_code}\n")
    except requests.RequestException as e:
        print(f"Помилка при доступі до {url}: {e}\n")

# завдання 2
def get_robots_txt(url):
    print("2. Вміст robots.txt:")
    if not url.endswith('/'):
        url += '/'
    robots_url = url + "robots.txt"
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            print(response.text + "\n")
        else:
            print(f"Не вдалося завантажити robots.txt, код: {response.status_code}\n")
    except requests.RequestException as e:
        print(f"Помилка: {e}\n")

# завдання 3
def get_dataset_count():
    print("3. Кількість наборів даних на data.gov:")
    url = "https://catalog.data.gov/api/3/action/package_search"
    try:
        response = requests.get(url)
        data = response.json()
        if data['success']:
            count = data['result']['count']
            print(f"Кількість наборів: {count}\n")
        else:
            print("Не вдалося отримати дані\n")
    except requests.RequestException as e:
        print(f"Помилка: {e}\n")

# завдання 4
def get_latest_dataset_name():
    print("4. Останній доданий набір даних:")
    url = "https://catalog.data.gov/api/3/action/package_search?rows=1&sort=metadata_created desc"
    try:
        response = requests.get(url)
        data = response.json()
        if data['success']:
            latest = data['result']['results'][0]
            print(f"Назва: {latest['title']}\n")
        else:
            print("Не вдалося отримати дані\n")
    except requests.RequestException as e:
        print(f"Помилка: {e}\n")

# завдання 5
def get_covid_stats(country=None):
    print("5. COVID-19 статистика:")
    url = "https://api.covid19api.com/summary"
    try:
        response = requests.get(url)
        data = response.json()
        if country:
            for c in data['Countries']:
                if c['Slug'] == country.lower():
                    print(f"{c['Country']}: Випадки: {c['TotalConfirmed']}, Смерті: {c['TotalDeaths']}, Одужало: {c['TotalRecovered']}\n")
                    return
            print("Країна не знайдена\n")
        else:
            global_data = data['Global']
            print(f"Світ: Випадки: {global_data['TotalConfirmed']}, Смерті: {global_data['TotalDeaths']}, Одужало: {global_data['TotalRecovered']}\n")
    except requests.RequestException as e:
        print(f"Помилка: {e}\n")

# завдання 6
def get_stock_info(ticker):
    print("6. Дані з Yahoo Finance:")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        print(f"Назва: {info.get('shortName')}")
        print(f"Ринок: {info.get('exchange')}")
        print(f"Ціна: {info.get('regularMarketPrice')}")
        print(f"Обсяг: {info.get('volume')}\n")
    except Exception as e:
        print(f"Помилка при отриманні даних: {e}\n")



check_page_availability("https://en.wikipedia.org")
get_robots_txt("https://en.wikipedia.org")
get_dataset_count()
get_latest_dataset_name()
get_covid_stats()
get_stock_info("AAPL")

# завдання 7
import openrouteservice

def get_coordinates(client, city_name):
    try:
        geocode = client.pelias_search(text=city_name)
        coords = geocode['features'][0]['geometry']['coordinates']
        return coords
    except Exception as e:
        print(f"Помилка при пошуку координат міста {city_name}: {e}")
        return None

def get_route_between_cities(api_key, from_city, to_city):
    print("7. Маршрут між містами з OpenRouteService:\n")

    client = openrouteservice.Client(key=api_key)

    from_coords = get_coordinates(client, from_city)
    to_coords = get_coordinates(client, to_city)

    if not from_coords or not to_coords:
        print("Не вдалося отримати координати одного з міст.")
        return

    try:
        route = client.directions(
            coordinates=[from_coords, to_coords],
            profile='driving-car',
            format='json'
        )
        summary = route['routes'][0]['summary']
        distance_km = summary['distance'] / 1000
        duration_min = summary['duration'] / 60

        print(f"Маршрут: {from_city} → {to_city}")
        print(f"Відстань: {distance_km:.2f} км")
        print(f"Час у дорозі: {duration_min:.1f} хвилин\n")
    except Exception as e:
        print(f"Помилка при отриманні маршруту: {e}\n")

API_KEY = "5b3ce3597851110001cf624880eb6b9c6325432796fb14b4af51d588"
get_route_between_cities(API_KEY, "Kyiv", "Lviv")

#завдання 8

import requests

def get_city_info(city_name: object, username: object) -> None:
    print(f"Інформація про місто: {city_name}\n")
    base_url = "http://api.geonames.org/searchJSON"
    params = {
        "q": city_name,
        "maxRows": 1,
        "username": username
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if not data['geonames']:
            print("Місто не знайдено.")
            return None

        city = data['geonames'][0]
        name = city.get('name')
        country = city.get('countryName')
        population = city.get('population')
        lat = city.get('lat')
        lng = city.get('lng')

        print(f"Назва: {name}")
        print(f"Країна: {country}")
        print(f"Населення: {population}")
        print(f"Координати: широта {lat}, довгота {lng}")

        timezone_url = "http://api.geonames.org/timezoneJSON"
        tz_params = {
            "lat": lat,
            "lng": lng,
            "username": username
        }
        tz_response = requests.get(timezone_url, params=tz_params)
        tz_data = tz_response.json()

        timezone = tz_data.get("timezoneId", "Немає інформації")
        gmt_offset = tz_data.get("gmtOffset", "Немає інформації")

        print(f"Часовий пояс: {timezone}")
        print(f"Зміщення GMT: {gmt_offset}")

    except Exception as e:
        print(f"Помилка: {e}")

USERNAME = "kozhokar_dr"
get_city_info("Kherson", USERNAME)
