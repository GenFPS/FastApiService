import re


class DataExtraction:
    def __init__(self, text: str):
        self._text = text
        self.inn_kpp: str = ''

    @property
    def text(self) -> str:
        return self._text

    def inn_and_kpp_extract(self) -> str | Exception:
        pattern_inn_kpp = r'\d{12}|(\d{10}(?:\/\d{9})?)'
        result = re.search(pattern_inn_kpp, self._text.replace(' ', '').lower())
        try:
            self.inn_kpp = result.group(0)
        except AttributeError as e:
            return e
        return self.inn_kpp
