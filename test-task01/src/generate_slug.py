import string
from secrets import choice

ALPHA: str = string.ascii_letters + string.digits

def generate_slug():
    slug = ""
    for _ in range(6):
        slug += choice(ALPHA)
    return slug