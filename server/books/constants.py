from typing import List, Tuple


SUBSCRIPTION_TYPES: List[Tuple[int, str]] = [
        (1, 'Стандарт'),
        (2, 'Плюс'),
        (3, 'Премиум'),
]

SUBSCRIPTION_DURATIONS: List[Tuple[int, str]] = [
        (3, '3 Месяца'),
        (6, '6 Месяцев'),
        (12, 'Год'),
]

ALREADY_LIKED: str = 'Вы уже лайкнули эту книгу'

NOT_LIKED: str = 'Вы еще не лайкнули эту книгу'

NO_SUBSCRIPTION: dict = {
    'type': None,
    'duration': None,
    'start_date': None,
    'days_to_end': None
}
