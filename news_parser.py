from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiohttp
from bs4 import BeautifulSoup
from dateparser import parse


BASE_URL: str = "https://wotexpress.info"


@dataclass
class News:
    title: str
    url: str
    date: datetime

    def __eq__(self, other) -> bool:
        if not isinstance(other, News):
            return False

        return all(
            [self.date == other.date,
             self.url == other.url,
             self.title == other.title]
        )


async def get_news() -> List[News]:
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + "/news/world-of-tanks/") as request:
            page_text = await request.text()

    soup = BeautifulSoup(page_text, features="lxml")
    news_list = soup.select("div.flex-start a.news-block-row")
    news_objects = []

    for news in news_list:

        try:
            title: str = news.find('h4').text
            date: str = news.find('div', class_='news_date').text
            link: str = news['href']

            news_objects.append(
                News(title, link, parse(date))
            )
        except AttributeError:
            continue

    return news_objects
