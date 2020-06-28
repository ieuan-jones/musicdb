import datetime
import requests
import csv

def reformat_date(date):
    '''Reformat from dd/mm/yyyy, to yyyy-mm-dd'''
    return datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')

server = 'http://localhost:5000/catalogue'
artists = {}
albums = []
full_genre = {
    'Elec.': 'Electronic',
    'Exp.': 'Experimental',
    'Folk': 'Folk/Country',
    'Hip.': 'Hip-Hop',
    'Amb.': 'Ambient',
    'Cont.': 'Contemporary',
    'W.': 'Worship',
    'Rock': 'Rock',
    'Pop': 'Pop'
}

with open('moosic.csv','r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header
    next(reader) # Skip the header
    next(reader) # Skip the header
    for row in reader:
        if row:
            album = {
                'name': row[1],
                'format': row[6],
                'genre': row[4],
                'songs': []
            }
            if row[0]:
                album['release_date'] = reformat_date(row[0])
            if row[8]:
                album['rating'] = int(float(row[8])*10)
            if row[5]:
                album['subgenres'] = [full_genre[row[5]]]
            if row[55]:
                album['first_listen'] = reformat_date(row[55])
            if row[49]:
                album['pitchfork'] = row[49]
            if row[50]:
                album['metacritic'] = row[50]
            if row[51]:
                album['fantano'] = row[51]

            for song in row[11:49]:
                if song:
                    album['songs'].append(song.upper())
            
            if row[3] not in artists:
                res = requests.post(f'{server}/artist', json={'name': row[3]})
                if res.status_code == 200:
                    artists[row[3]] = res.json()['artist_id']
                else:
                    print(res.status_code)
            
            album['artist_id'] = artists[row[3]]

            res = requests.post(f'{server}/album', json=album)
            if res.status_code == 200:
                #print(album['name'], res.json()['album_id'])
                pass
            else:
                print(res.status_code)
                print(album)
                break

