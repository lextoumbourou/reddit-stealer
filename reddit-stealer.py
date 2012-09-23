""" 
Reddit Video Stealer

Download every Youtube video in a subreddit then rip the audio
"""
import os
from sys import exit, argv
import subprocess

import httplib2
import json

from lib.youtube.youtube import YouTube
import config

def get_page(url):
    """Return html content (a simple wrapper for httplib2)"""
    output = []
    headers = {'User-Agent':'audio collector bot by /u/WalkThePlank'}
    h = httplib2.Http('.cache')
    resp, content = h.request(url, 'GET', headers=headers)

    if resp['status'] == '200':
        return content
    else:
        return None

def get_youtube_links(data):
    """Return a list of Youtube links

    Arguments:
    data -- Json data for a Subreddit

    """
    output = []
    json_data = json.loads(data)
    for j in json_data['data']['children']:
        link = j['data']['url']
        if 'youtube.com' in link:
            output.append(link)

    return output

def convert_to_audio(infile):
    """Call avconv to perform the video conversion

    Arguments:
    infile -- an absolute path to a video file

    """
    outfile = config.FINISH_PATH+'/'+yt.filename+'.wav'
    cmd = ['avconv', '-i', infile, outfile]
    subprocess.call(cmd)

if __name__ == '__main__':
    # Check if the directories exist as per the config
    if not os.path.exists(config.FINISH_PATH):
        os.makedirs(config.FINISH_PATH)
    if not os.path.exists(config.TMP_PATH):
        os.makedirs(config.TMP_PATH)
        
    for subreddit in config.SUBREDDITS:
        url = 'http://www.reddit.com/r/{0}/.json?limit={1}'.format(subreddit,
                                                                   config.LIMIT)
        data = get_page(url)
        if not data:
            print "Can't find Subreddit "+subreddit
            continue
        links = get_youtube_links(data)
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
                        # Convert the video file to audio
                        convert_to_audio(download_path)
                        # Remove the video file
                        os.remove(download_path)
                else:
                    print "Already got ", yt.filename
