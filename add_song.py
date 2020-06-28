import requests
import time

server = 'http://localhost:5000/catalogue'
'''song = {
    'name': 'Marching on',
    'length': 137,
    'position': 2,
    'grade': 'A',
    'comments': 'All in all a very good song'
}'''
artist = {
    'name': 'The Alarm'
}
album = {
    'artist_id': 'aaaa-bbbb',
    'name': 'Declaration',
    'format': 'LP',
    'release_date': '11/12/2019',
    'first_listen': '05/02/2020',
    'rating': 93,
    'songs': [
        'a',
        'b',
        'a',
        '*'
    ],
    'genre': 'Rock',
    'subgenres': [
        'Alternative Rock'
    ]
}

res = requests.post(f'{server}/artist', json=artist)
if res.status_code == 200:
    artist_id = res.json()['artist_id']
    print(artist_id)
else:
    print(res.status_code)

album['artist_id'] = artist_id
res = requests.post(f'{server}/album', json=album)

if res.status_code == 200:
    print(res.json())
else:
    print(res.status_code)
