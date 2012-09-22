import httplib2
import os
from lib.youtube.youtube import YouTube
from sys import exit, argv
import json
import config
import subprocess
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
    # Check if the directories exist as per the config
    if not os.path.exists(config.FINISH_PATH):
        os.makedirs(config.FINISH_PATH)

    if not os.path.exists(config.TMP_PATH):
        os.makedirs(config.TMP_PATH)
        
    for subreddit in config.SUBREDDITS:
        url = 'http://www.reddit.com/r/{0}/.json?limit={1}'.format(subreddit,
                                                                   config.LIMIT)
        links = get_youtube_links(get_page(url))
        for link in links:
            yt = YouTube()
            yt.url = link
            video = yt.get_highest_quality()
            if video:
                download_path = "{0}/{1}.{2}".format(config.TMP_PATH,
                                                      yt.filename,
                                                      video.extension)
                if not os.path.isfile(download_path):
                    video.download(path=config.TMP_PATH)
                    if os.path.isfile(download_path):
                        cmd = ['avconv', 
                               '-i',
                               download_path,
                               config.FINISH_PATH+yt.filename+'.wav']
                        subprocess.call(cmd)
                else:
                    print "Already got ", yt.filename
