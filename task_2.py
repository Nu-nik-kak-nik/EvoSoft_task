import requests
from bs4 import BeautifulSoup
import random
import time

proxies = {
    'http': 'http://165.22.77.86:80',
    'https': 'https://165.22.77.86:80'
}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

def get_html(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return None

def parse_tweets(html):
    soup = BeautifulSoup(html, 'html.parser')
    tweets = []
    tweet_elements = soup.find_all('div', class_='css-901oao r-18u37j')
    for element in tweet_elements:
        text = element.text.strip()
        if text:
            tweets.append(text)
    return tweets, soup

def main():
    base_url = "https://twitter.com/elonmusk"
    url = base_url
    tweets = []

    while len(tweets) < 10:
        html = get_html(url)
        if html:
            new_tweets, soup = parse_tweets(html)
            tweets.extend(new_tweets)
            time.sleep(random.randint(2, 5))
            url = soup.find('a', rel='next')['href']
        else:
            print("Ошибка при получении HTML-кода.")

    with open("elon_musk_tweets.log", "w") as log_file:
        for tweet in tweets[:10]:
            log_file.write(tweet + "\n\n")

if __name__ == "__main__":
    main()