import logging
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement
from requests import RequestException
from rich.logging import RichHandler

from .exceptions import GUException
from .models import Item

logging.basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Base:
    __base_url = 'https://gu.ac.ir/'
    _default_image_url = 'file/c604dcdc-8f39-ed11-9eda-005056998f1e/سردر2.jpg'

    def __init__(self, name: str, section_url: str) -> None:
        self._name = name
        self._section_url = section_url

    def get_latest_item(self) -> Item:
        all_items = self.get_all_items(latest=True)
        return all_items[0]

    def get_all_items(self, page: int = 1, latest: bool = False) -> List[Item]:
        bs4 = self._get_bs4_object(page)
        elements = bs4.find_all(
            'tr',
            {'class': 'context-list-row'}
        )

        items: List[Item] = []

        for element in elements:
            items.append(
                self._build_item(element)
            )

            if latest:
                break

        return items

    def log(self, level: int, message: str, *args, **kwargs) -> None:
        message = f'{self._name} | {message}'
        logger.log(level, message, *args, **kwargs)

    def _get_bs4_object(self, page: int = 1) -> BeautifulSoup:
        try:

            req = requests.post(
                f'{self.__base_url}/{self._section_url}',
                {
                    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ctl10$GridView1',
                    '__EVENTARGUMENT': f'Page${page}',
                    '__VIEWSTATE': "/wEPDwUJNDU3ODEwMDEyZBgBBSljdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGN0bDEwJEdyaWRWaWV3MQ88KwAMAgICAQgCKmQdwoMwea9xZgIDRLG/FlEGKkd+1hP9H1U1FkX0YORIrQ==",
                    '__VIEWSTATEGENERATOR': "C0666E88",
                    '__EVENTVALIDATION': "/wEdAAuZyzL8+PA32VOevKFuoPtwTvR7yj4Xi6i3NUI68KPqudUyw2h61WD05OmNkOy6S8jUHRdvYn1KZfEWxtAVDaVD5/N0XPSnvc7LTVa7cqeEw2NxMNhQ6YgOi6njYQt+alFgqGq9WXbBlXr3yojBkyGaPbG0TEeeW47ta8Hp12xCh5sOY4ETmV8wO19lr5rjN1lFiZ/9QXRfX9MGjLqje+Kfo36HWfAMXTgtd61LUOWyMfAD6Dgw7UMUaGZRfuS75eaHK9oMVY2ElGHFYoF21n4l"
                },  # Default data from the website. It's working without the new data.
                timeout=10
            )
            if req.status_code != 200:
                raise RequestException
        except RequestException:
            raise GUException("Couldn't fetch the data")
        else:
            bs4 = BeautifulSoup(req.text, 'html.parser')
            return bs4

    def _build_item(self, element: PageElement) -> Item:
        title = element.find_next('h3').text
        url = self._build_url(
            element.find_next('a')['href']
        )
        date = element.find_next('div', {'class': 'news-date'}).text
        img_url = self._build_url(
            element.find_next('img', {'class': 'img-responsive'})['src'] or self._default_image_url
        ).replace('/thumb/sm', '')

        return Item(title, url, date, img_url)

    def _build_url(self, url: str) -> str:
        return f'{self.__base_url}/{url}'
