#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Motoki Wu'
SITENAME = 'Shrunken Master'
SITEURL = 'http://tokestermw.github.io'
#SITEURL = '.' # put actual URL in publishconf.py
RELATIVE_URLS = True

GITHUB_URL = 'https://github.com/tokestermw'
GOOGLE_ANALYTICS = 'UA-43076745-1'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

EXTRA_PATH_METADATA = {'extra/.htaccess': {'path':'.htaccess'}, 'extra/robots.txt': {'path': 'robots.txt'}}

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

THEME = "./theme"

ARTICLE_DIR = 'posts'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
ARTICLE_URL = 'posts/{slug}.html'

#DISQUS_SITENAME = "mowu"

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'

TAG_FEED_ATOM = 'feeds/tag_%s.atom.xml'
TAG_FEED_RSS = 'feeds/tag_%s.rss.xml'

TAG_CLOUD_STEPS = 10
TAG_CLOUD_MAX_ITEMS = 100

# Python-Markdown extensions to be included
MD_EXTENSIONS = ['codehilite(guess_lang=False)']

PLUGIN_PATH = './plugins'
# https://github.com/danielfrg/pelican-ipythonnb
MARKUP = ('md', 'ipynb')
PLUGINS = ['ipythonnb']
# https://github.com/bstpierre/pelican-comments
#COMMENTS_DIR = ['comments']

DIRECT_TEMPLATES = (['about', 'base', 'index', 'tag', 'tags'])

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

STATIC_PATHS = ['images', 'posts/compare_models_finished_files']
