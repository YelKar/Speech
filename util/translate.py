import requests
from dataclasses import dataclass
from typing import Generator


@dataclass
class Translation:
    text: str
    detected_language: str


def translate(
        text: list or str,
        to_: str = "en",
        from_: str = None,
        TOKEN="t1.9euelZqPlsqYls7MzcyXkI7LypuOye3rnpWalIyYjJ7LmJmUmIrHncfIl8rl8_dAQndq-e9GehUm_d3z9wBxdGr570Z6FSb9"
              ".Rz290b3xrjdbp1XVj4Z0tnYkeWeTO8a-YIz5SZluti8-My_qH0BcmRcLKML0AzsZDififkRdkP6laIii9GJBCA",
        folder_id="b1g0q5gvhonjk3t3e0st"
) -> Generator or Translation:
    body = {
        "targetLanguageCode": to_,
        "sourceLanguageCode": from_,
        "texts": text if isinstance(text, list) else [text],
        "folderId": folder_id,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(TOKEN)
    }
    response = requests.post(
        'https://translate.api.cloud.yandex.net/translate/v2/translate',
        json=body,
        headers=headers
    )

    def replacing(translations):
        for translation in translations:
            tr = Translation(translation["text"], translation["detectedLanguageCode"])
            yield tr
    translations = replacing(response.json()["translations"])

    if isinstance(text, list):
        return translations
    return next(translations)


if __name__ == '__main__':
    translate("Привет")
