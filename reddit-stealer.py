#!/usr/bin/env/ python
import os
import subprocess
import json
import sys
import argparse
import urllib2

import httplib2
from pytube import YouTube
import sh
"""
Reddit Video Stealer

Download every YouTube video in a subreddit at the highest
possible quality, and, optionally rip the audio.

"""
USER_AGENT = 'reddit-stealer.py by /u/WalkThePlank'


def get_args():
    parser = argparse.ArgumentParser(
        description="Download every video in a subreddit")
    parser.add_argument(
        'subreddits', type=str, nargs='+',
        help='Subreddits to steal from')
    parser.add_argument(
        '-l', '--limit', type=int, default=50,
        help='Limit amount of videos downloadable per Subreddit')
    parser.add_argument(
        '-o', '--output_dir', type=str, default='./',
        help='Specify output directory (defaults to current directory)')
    parser.add_argument(
        '-a', '--audio', action='store_true',
        help='Additionally, rip a .wav file when done?')
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='Force download even if file already exists in collection')

    args = parser.parse_args()
    return args


def get_page(url):
    """
    Return html content (a simple wrapper for httplib2)
    """
    output = []
    headers = {'User-Agent': USER_AGENT}
    h = httplib2.Http('.cache')
    resp, content = h.request(url, 'GET', headers=headers)

    if resp['status'] == '200':
        return content
    else:
        return None


def get_youtube_links(data):
    """
    Return a list of YouTube links

    Arguments:
    data -- Json data for a Subreddit
    """
    output = []
    json_data = json.loads(data)
    for j in json_data['data']['children']:
        link = j['data']['url']
        if 'youtube.com' in link and not 'playlist' in link:
            output.append(link)

    return output


def convert_to_audio(infile, outpath=None):
    """
    Call avconv to perform the video conversion

    Arguments:
    infile -- an absolute path to a video file
    """
    if not outpath:
        outpath = os.path.dirname(infile)

    # Filename with the extension.
    filename = os.path.basename(infile)
    # Won't be needing that anymore.
    filename = ' '.join(filename.split(".")[0:-1])

    outfile = '{0}/{1}.wav'.format(outpath, filename)
    cmd = ['avconv', '-i', infile, outfile]
    subprocess.call(cmd)


class ExtendedYouTube(YouTube):
    """
    ExtendedYoutube adds get_highest_quality() to the pytube.Youtube library
    """
    def get_highest_quality(self, extension_pref='mp4'):
        """
        Take a Youtube instance as input
        and return the highest available quality
        """
        highest = 0
        preferred_ext = 'mp4'
        result = None
        for v in self.videos:
            current = int(v.resolution[:-1])
            if (current > highest) or \
               (current == highest and v.extension == extension_pref):
                highest = current
                result = v

        return result


def main():
    """
    Main program body
    """
    args = get_args()
    for subreddit in args.subreddits:
        url = 'http://www.reddit.com/r/{0}/.json?limit={1}'.format(subreddit,
                                                                   args.limit)
        data = get_page(url)
        if not data:
            print "Can't find Subreddit {0} ".format(subreddit)
            continue
        links = get_youtube_links(data)
        for link in links:
            yt = ExtendedYouTube()
            yt.url = link
            video = yt.get_highest_quality()
            if not video:
                continue
            download_path = '{0}/{1}.{2}'.format(
                args.output_dir,
                yt.filename,
                video.extension)
            if args.force or not os.path.isfile(download_path):
                try:
                    video.download(path=args.output_dir)
                except Exception, e:
                    print "Failed to download {0} due to: {1}".format(
                        yt.filename,
                        e)
                    continue
                if os.path.isfile(download_path) and args.audio:
                    # Convert the video file to audio
                    convert_to_audio(download_path)
            else:
                print "Already got {0}".format(yt.filename)

if __name__ == '__main__':
    main()
