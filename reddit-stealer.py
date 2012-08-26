import httplib2
from os import path
from lib.youtube.youtube import YouTube
from sys import exit
import json
""" 
Reddit Video Stealer

Download every Youtube video in a subreddit then rip the audio
"""
def get_page(url):
    output = []
    headers = {'User-Agent':'audio collector bot by /u/WalkThePlank'}
    h = httplib2.Http('.cache')
    resp, content = h.request(url, 'GET', headers=headers)

    return content

def get_youtube_links(data):
    output = []
    json_data = json.loads(data)
    for j in json_data['data']['children']:
        link = j['data']['url']
        if 'youtube.com' in link:
            output.append(link)

    return output

if __name__ == '__main__':
    url = ('http://www.reddit.com/r/ObscureMedia/.json?limit=100')
    links = get_youtube_links(get_page(url))
    for link in links:
        yt = YouTube()
        yt.url = link
        video = yt.get_highest_quality()
        if video:
            if not path.isfile(yt.filename+'.'+video.extension):
                video.download()
            else:
                print "Already got ", yt.filename
