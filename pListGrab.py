import youtube_dl

#example url links for some videos and playlists
video_links = ["https://www.youtube.com/watch?v=X5dFz1ZZWk8", "https://www.youtube.com/watch?v=iIaJLdW0bLg", "https://www.youtube.com/watch?v=B4Cx4XiNntQ", "https://www.youtube.com/watch?v=nR-Zen2s2Qw"]
playlist_links = ["https://youtube.com/playlist?list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3", "https://youtube.com/playlist?list=PLMBYlcH3smRzz8VqMEUO2i9Vu3ynWAkQ0"]

#template and list used for creating real url links from video ids
url_template = "https://www.youtube.com/watch?v="
playlist_urls_listed = []

#youtubeDL object
ydl = youtube_dl.YoutubeDL({'quiet': True, 'extract_flat': 'in_playlist'})

ydl.download(video_links[0])

'''
#grabbing results from one of the example links
with ydl:
    result = ydl.extract_info(url=video_links[1], download=False)
    #result = ydl.extract_info(url=video_links[0], download=False)

    #Some print statements that show all the keys in the dictionary to show what info we can extract from ydl
    print(result.keys())
    #print(result['extractor'])
    #print(result['webpage_url'])
    #print(type(result['webpage_url']))
    #print(result['entries']) #NOTE entries are only in playlist links

    #To see if the link is a YT playlist link
    if 'entries' in result:
        video = result['entries']
        for i, item in enumerate(video): # this goes through each result with an entires key
            video = result['entries'][i]
            #print(video['title'])
            #print(video['url'])
            playlist_urls_listed.append(url_template + video['url'])

#prints each playlist with converted url as a string
for e in playlist_urls_listed:
    print(e)
    #print(type(e))
    '''