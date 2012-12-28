Reddit Stealer
=============

A small script to download all recent videos in Subreddits and convert to audio.

Options
-----

```
positional arguments:
  subreddits            Subreddits to steal from

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Limit amount of videos downloadable per Subreddit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output directory (defaults to current
                        directory)
  -a, --audio           Rip to audio when complete
```

Examples
--------

```bash
python reddit-stealer.py exploitation ObscureMedia
```
