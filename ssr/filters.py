import re
from datetime import datetime


def return_date(date_as_str):
    if date_as_str == '' or date_as_str is None:
        return ''
    else:
        return datetime.strptime(date_as_str, '%Y-%m-%d')


def get_filtered_data(data, filters):
    if filters['author'] is not None and filters['author'] != 'None':
        data = list(filter(lambda x: x['author'] == filters['author'], data))

    if filters['name'] is not None and filters['name'] != 'None':
        data = list(filter(lambda x: re.match(f'.*{filters["name"]}.*', x['title']), data))

    if filters['from'] is not None and filters['from'] != 'None' and filters['from'] != '':
        data = list(
            filter(lambda x: datetime.strptime(x['date'], '%Y-%m-%d') > datetime.strptime(filters['from'], '%Y-%m-%d'),
                   data))

    if filters['to'] is not None and filters['to'] != 'None' and filters['to'] != '':
        data = list(
            filter(lambda x: datetime.strptime(x['date'], '%Y-%m-%d') < datetime.strptime(filters['to'], '%Y-%m-%d'),
                   data))

    return sorted(data, key=lambda d: d[filters['sortBy']]) if filters['sortBy'] is not None and filters[
        'sortBy'] != 'None' else data


def get_authors(data):
    authors = [None]
    for book in data:
        if book['author'] not in authors:
            authors.append(book['author'])
    return authors
