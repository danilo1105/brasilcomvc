from cities_light import InvalidItems


def filter_city_import(sender, items, **kwargs):
    if items[8] not in ('BR',):
        raise InvalidItems()
