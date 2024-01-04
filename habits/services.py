import logging
from time import sleep

import requests
from django.conf import settings
from requests import RequestException

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self, bot_token: str):
        self.token = bot_token
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.max_request_retries = 5
        self.request_delay = 1
        self.last_update = 0

        bot_data = self.getme()

        self.id = bot_data["id"]
        self.username = bot_data["username"]

    def make_request(self, url: str, params: dict = None) -> requests.Response:
        for attempt in range(self.max_request_retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                return response
            except RequestException as e:
                if attempt < self.max_request_retries - 1:
                    sleep(self.request_delay)
                    logger.info(f"Attempt {attempt + 1} to make request to {url}")
                else:
                    logger.error(f"Cant make request to {url}. Error: {e}")

    def send_message(self, chat_id: int, text: str) -> requests.Response:
        url = f"{self.api_url}/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        response = self.make_request(url, params=params)
        return response

    def get_updates(self) -> list[dict]:
        url = f"{self.api_url}/getUpdates"
        params = {"offset": self.last_update + 1}
        response = self.make_request(url, params)

        updates: list = response.json().get("result")

        if updates:
            self.last_update = updates[-1].get("update_id")
            print(self.last_update)

        return updates

    def getme(self) -> dict:
        url = f"{self.api_url}/getme"
        response = self.make_request(url)
        return response.json().get("result")

    def generate_invite_link(self, secret):
        link = f"https://t.me/{self.username}?start={secret}"
        return link


telegram_service = TelegramService(settings.TELEGRAM_TOKEN)
