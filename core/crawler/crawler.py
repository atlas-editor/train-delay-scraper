import logging

import requests
from fake_useragent import UserAgent


def get_headers():
    """
    tries to load a random header from the fake_useragent library, returns None if loading failed else a valid header
    :return: a header or None if loading failed
    """
    try:
        ua = UserAgent()
        return {'User-Agent': ua.random}
    except Exception as e:
        logging.warning(e)
        logging.warning("couldn't load headers")
        return None


def get_html(url, headers=None):
    """
    returns the html located on: url
    :param url: from which to load webpage
    :param headers: if specified used while getting the request
    :return: html of the specified webpage
    """
    proxies = None # {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
    response = requests.get(url, headers=headers, proxies=proxies)
    if not response:
        raise ConnectionError("couldn't connect to: " + str(url))

    return response.text
