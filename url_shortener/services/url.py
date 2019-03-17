import random
import string
from typing import List


class UrlService:
    def generate_slug(self, length: int, chars: List[str] = string.ascii_letters + string.digits) -> str:
        return ''.join(random.choice(chars) for _ in range(length))
