import requests
import os
import shutil
import urllib

import json
import deezloader
import eyed3
eyed3.log.setLevel('ERROR')


def name_files(directory_album):

    song_num = 1
    directory = ''

    # Renaming All Songs and Creating a New Folder

    song = ''
    for song in directory_album:
        tag = eyed3.load(song)

        if song_num == 1:
            dalbum = tag.tag.album + '/'
            dartist = tag.tag.artist
            directory = dartist + ' - ' + dalbum
            os.mkdir('./download/' + directory)

        os.rename(song, './download/' + directory + str(song_num) + ' - ' + tag.tag.title + '.mp3')

        song_num += 1

    # Removing Older Folder

    older_folder = song.split('/')[:2]  # Taking the Main Folder
    shutil.rmtree(older_folder[0] + '/' + older_folder[1])

    # Opening Folder With Album
    real_path = os.path.realpath('./download/' + directory)
    os.startfile(real_path)

    return real_path


def cover(path, info_album):
    urllib.request.urlretrieve(info_album['cover_xl'], path + '/cover.png')


d = deezloader.Login('ARL TOKER HERE')

while True:
    query = input("Search for Album : ")

    link = 'https://api.deezer.com/search/album?q=' + query
    response = requests.get(link)

    # Writing Response in File JSON
    with open('received.json', 'w+') as f:
        f.write(response.text)

    # Creating a Dict from Response
    parsed = json.loads(response.text)

    info = """
    
        Found : {} Album
        Visualizing : {}
        
    """.format(parsed['total'],
               len(parsed['data']))

    print(info)

    if len(parsed['data']) is 0:
        continue

    for album in range(0, len(parsed['data'])):

        album_info = """
        
        Refecence For Download : {}    
        Album Name : {}
        Number of Tracks : {}
        Artist Name : {}
        Type (Check) : {}
        
        """.format(album+1,
                   parsed['data'][album]['title'],
                   parsed['data'][album]['nb_tracks'],
                   parsed['data'][album]['artist']['name'],
                   parsed['data'][album]['type'])

        print(album_info)

    try:
        download = int(input('Which One You Want Download? : '))
        download -= 1
    except ValueError:
        raise ValueError('Inserted Isn\'t a Number')

    cover(
        name_files(
            d.download_albumdee(
                parsed['data'][download]['link'],
                output='download',
                quality='MP3_320',
                recursive_quality=True,
                recursive_download=True,
                not_interface=False,
                zips=False
            )
        ),
        parsed['data'][download]
    )

