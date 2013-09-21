title: Static blogging using Pelican for quasi-hackers
date: 2013-07-24
tags: pelican
author: Motoki Wu
summary: just another Pelican blog and just another Pelican blog tutorial

[Pelican](http://blog.getpelican.com/) was a natural choice for a *quasi-hacker* like me, which I define as people who like to tinker around than rebuilding the wheel from scratch (at least in terms of web dev skills, [stats is another story](http://columbiadatascience.com/2012/12/03/in-defense-of-statistics-or-why-data-scientists-should-make-understanding-statistics-a-priority/)). A static blog generator like Pelican is comfy because it acts as an extension of my workflow. All of my writing, equations and coding are written in text files so it's a breeze to organize them in [Markdown](http://daringfireball.net/projects/markdown/) and [Jinja2](http://jinja.pocoo.org/docs/). I wanted this site to look and act minimalist, so it's nice to have full control and not have to fiddle with databases, server maintenance, security, etc. Hosting is easy, I just have to copy and paste all of the generated files to a hosting service.

What follows will be my notes on the structure of this website, I hope it's useful. I'm assuming people have already installed the Python packages and have done ```pelican-quickstart``` (choose "yes" on the Makefile and simpleHTTP script).

*Last updated: 2013-08-28 (Pelican 3.2.2)*

## File structure of the Pelican

It's important to understand the default file structure in Pelican. Unlike [Jekyll](http://jekyllrb.com), not everything in the working directory gets copied over to the ```output``` directory. 

	yourproject/
	|--- content
		 |--- pages
		 |---(posts)
		 |---images
	|--- output
	|--- develop_server.sh
	|--- Makefile
	|--- pelicanconf.py       # Main settings file
	|--- publishconf.py       # Settings to use when ready to publish

Any Markdown or reStructuredText files inside the ```content``` folder will be used to generate articles to the ```output``` folder. The default behavior for the ```pages``` and ```images``` adds ancillary pages and images respectively into ```output/static```. If you want to specify other directories, you can configure them inside the config file ```pelicanconf.py```.  

# pelicanconf.py

The main configuration file is a bunch of [configurable Python variables](http://docs.getpelican.com/en/3.2/settings.html#basic-settings) (in all caps) that you can reference through Jinja2 templating. Start with the basics:

	:::python
	AUTHOR = 'Motoki Wu'
	SITENAME = 'Shrunken Master'

As mentioned before, you can set your static paths inside the ```content``` folder. Create a ```posts``` to have Pelican deploy it to ```output/posts```:

	:::python
	STATIC_PATHS = ['posts']

Alternatively, you can customize the ```slug``` for more dynamic URLs. The ```slug``` of each article is either specified in the Markdown files, or Pelican makes one from the title.

	:::python
	ARTICLE_DIR = 'posts'
	ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
	ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}.html'

Most importantly, you'll need to set the [URL settings](http://docs.getpelican.com/en/3.2/settings.html#url-settings) of the blog. For testing, I think it's good to set ```RELATIVE_URLS = True```. Then when you publish your blog, you can set it ```False``` in your ```publishconf.py``` file. 

	:::python
	SITEURL = 'http://tokestermw.github.io'
	RELATIVE_URLS = True

## Stylin'

The [file structure for each theme](http://docs.getpelican.com/en/3.1.1/themes.html
) will need to follow this structure:

	|--- static
		 |--- css
		 |--- images
	|--- templates
		 |--- archives.html    // to display archives
		 |--- article.html     // processed for each article
		 |--- author.html      // processed for each author
		 |--- authors.html     // must list all the authors
		 |--- categories.html  // must list all the categories
		 |--- category.html    // processed for each category
		 |--- index.html       // the index. List all the articles
		 |--- page.html        // processed for each page
		 |--- tag.html         // processed for each tag
		 |--- tags.html        // must list all the tags. Can be a tag cloud.

All of the files inside ```static``` will be copied over to the ```output``` folder, while any non-default template file needs to be directly linked. 

You can specify the location of the theme by specifying it in ```pelicanconf.py```:

	:::python
	THEME = "./theme"

It is good to download an example theme to get things started. I liked [Tim Poisot's](http://timotheepoisot.fr/) Jekyll site so I adopted that to my blog. I liked the general look of [Tufte's](http://www.edwardtufte.com/tufte/index) site so you can see its influence.

# Jinja2 templating

With Jinja templating, I can define variables, use inheritance to template the website and take advantage of basic programming functions (e.g. for loops). 

Variables defined in ```pelicanconf.py``` can be referenced to a Jinja template. Say in ```index.html```, I can link to my CSS file within my theme:

	:::html+jinja
	<link rel="stylesheet" type="text/css" href="{{ SITEURL }}/theme/styles.css" />
	
Inheritance happens in conjunction with template tags. Say in ```parent.html```, you can use the ```block``` tag to include content from another file. The most common usage in a blog is to keep the overall structure of the site in ```parent.html``` while putting individual blog posts inside say ```child.html```.

	:::html+jinja
	bla bla html+jinja code
	{% block content %}
	{% endblock %}
	bla bla more html+jinja code

Then ```extends``` the parent in ```child.html``` (make sure the name of the block matches):

	:::html+jinja
	{% extends "parent.html" %}
	{% block content %}
	blabla html code
	{% endblock %}

<span class="margin">All the action is in [context.py](https://github.com/getpelican/pelican/blob/master/pelican/contents.py) and [generators.py](https://github.com/getpelican/pelican/blob/master/pelican/generators.py) of the source code but I have to spend time understanding it.
	</span>You can add ```for``` loops to lists (e.g. ```articles```, ```dates```, ```tags```, ```pages```) generated in Pelican. For example, my ```archives.html``` look like this:
	
	{% for article in dates %}
	<ul class="leaders">
		<li><span><a href='{{ article.url }}'>{{ article.title }}</a></span>
			<span>{{ article.locale_date }}</span></li>
	</ul>
	{% endfor %}

The attributes of the list (e.g. ```url```, ```title```) come from metatags specified in the Markdown files. It sucks that documentation is light for variables called inside Jinja2. For example,  ```{{ article.content }}``` inside your ```article.html``` pastes the content from your Markdown files. I wouldn't have known about it without sample themes. 

# CSS

A note on CSS. I added a ```margin``` class so I can put sidenotes beside my blog posts. I basically created a big div for two columns (```content```) and make one div that is narrower (```pbody```). The HTML hierarchy looks like this:

	> body 
		> content 
			> margin 
			> pbody

Fix the position of the ```margin``` to where you want the sidenote located:

	:::css
	.margin{
		position: absolute;
		right: 0px;
		width: 19%;
		font-size: small;
	}

<span class="margin">This is a sidenote.</span>Then add a span inside your paragraph.

	:::html
	<p><span class="margin">This is a sidenote.</span>
	Then add a span inside your paragraph.</p>

## Writing articles, aka I thought we were supposed to focus on content

The metadata that you set in Markdown (or reStructuredText) is hugely important in how the files are generated. 

# Markdown

The only metadata that is necessary is ```title```, but you should have ```date``` as well (for sorting other functions). Here is mine for this very article:

	:::rst
	title: Static blogging using Pelican for quasi-hackers
	slug: Static-blogging-using-Pelican-for-quasi-hackers
	date: 2013-07-24
	tags: pelican
	author: Motoki Wu
	summary: Just another Pelican blog and just another Pelican blog tutorial.
	status: draft

Include something similar in every ```.md``` file. The ```status:draft``` allows me to output a Pelican generated file to the ```output/drafts``` folder without publishing it. If not specified, the ```slug``` is taken from ```title``` and adds hyphens in place of spaces. 

# Comments

Adding [DISQUS](http://disqus.com/) comments is easy. In your ```pelicanconf.py```, add:

	:::python
	DISQUS_SITENAME = "your disqus username"

Then include it in your templates (probably ```article.html```).

	:::jinja
	{% if DISQUS_SITENAME %}
	{% include 'disqus_comments.html' %}
	{% endif %}

I added ```disqus_comments.html``` so I can put the javascript code in a separate file.

I played with static(-ish) commenting platforms ([jekyll static commenting](http://theshed.hezmatt.org/jekyll-static-comments/), [pelican-comments](https://github.com/bstpierre/pelican-comments), [wt-comments](https://gitorious.org/wt-comments/wt-comments), [jskomment](https://code.google.com/p/jskomment/), [talkatv](http://talka.tv/)) for a bit, but none were satisfactory. 

# Code highlighting

Code highlighting is done in [Pygments](http://pygments.org/). First add the ```codehilite``` extension to your ```pelicanconf.py```.

	:::python
	MD_EXTENSIONS = ['codehilite(guess_lang=False)']

To add Python code like this,

	:::python
	@deterministic(plot=False)
	def rate(s=switchpoint, e=early_mean, l=late_mean):
	    ''' Concatenate Poisson means '''
	    out = empty(len(disasters_array))
	    out[:s] = e
	    out[s:] = l
	    return out

just put this in your Markdown file:

	:::md
		:::python
		@deterministic(plot=False)
		def rate(s=switchpoint, e=early_mean, l=late_mean):
		    ''' Concatenate Poisson means '''
		    out = empty(len(disasters_array))
		    out[:s] = e
		    out[s:] = l
		    return out

All of the lexers can be found [here](http://pygments.org/docs/lexers/).

# Equations

To use [MathJax](http://docs.mathjax.org/en/latest/start.html), add something like this to the ```<head>```:
	
	:::javascript
	<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
	<script type="text/x-mathjax-config">
	MathJax.Hub.Config({
	    imageFont: null,
	    messageStyle: "none", 
	    extensions: ["tex2jax.js"],
	    jax: ["input/TeX", "output/HTML-CSS"],
	    tex2jax: {
	          inlineMath: [ ['$','$'] ],
	          displayMath: [ ['$$','$$'] ],
	    processEscapes:true
	    }
	  });
	</script>
	<script type="text/javascript" src="https://d3eoax9i5htok0.cloudfront.net/mathjax/latest/MathJax.js"></script>

Test:

$$ I = \int_a^b e^{-\lambda g(y)} h(y)dy $$

	:::latex
	$$ I = \int_a^b e^{-\lambda g(y)} h(y)dy $$

# Fonts

I thought about using [web fonts](http://www.smashingmagazine.com/2010/10/20/review-of-popular-web-font-embedding-services/), but I wanted something local so at least the loading times would be consistent. From what I understand, using custom fonts may have [issues](http://www.stevesouders.com/blog/2009/10/13/font-face-and-performance/) with FOUT and slow load times but the distinct look that it gives is worth it. You might notice that the different fonts do load in staggered fashion.

To use custom fonts, I first downloaded the font kit from [Font Squirrel](http://www.fontsquirrel.com/) that I liked ([Ubuntu in my case](http://www.fontsquirrel.com/fonts/ubuntu?q=ubuntu)). Font Squirrel has [good cross-browser support](http://webdesignandsuch.com/fix-fonts-that-dont-work-with-google-font-api-in-internet-explorer-or-chrome-with-font-face/), it's free and it's easy to install. You just need to use the ```@font-face``` property in CSS. Link to the regular, bold and italic fonts, from your CSS file,

	:::css
	@font-face {
		font-family: 'ubuntu';
		src: url('../theme/font/ubuntu/Ubuntu-R.ttf');
		font-weight: normal;
	    font-style: normal;
	}

	@font-face {
		font-family: 'ubuntu';
		src: url('../theme/font/ubuntu/Ubuntu-B.ttf');
		font-weight: bold;
	    font-style: normal;
	}

	@font-face {
		font-family: 'ubuntu';
		src: url('../theme/font/ubuntu/Ubuntu-RI.ttf');
		font-weight: normal;
	    font-style: italic;
	}

then you can use your font in the appropriate places:

	:::css
	it, em{
		font-style: italic;
		font-weight: inherit;
	    font-family: ubuntu, "Helvetica Neue", Helvetica;
	}

	b, strong{
		font-weight: bold;
		font-style: inherit;
		font-family: ubuntu, "Helvetica Neue", Helvetica;
	}

## Optimize, optimize

I realized the site was slow, so I <a href="http://www.webpagetest.org/">checked the load times of each component</a>. I first put my [Google Analytics](http://www.google.com/analytics/) script to the bottom of the page so the website at least tries to load even with a bad connection. But the biggest culprit for slow load times were the fonts. So I followed [these directions here](http://www.artzstudio.com/2012/02/web-font-performance-weighing-fontface-options-and-alternatives/) to minimize the file size for fonts.

I uploaded my fonts to [Font Squirrel generator](http://www.fontsquirrel.com/tools/webfont-generator) to remove glyphs that will not be in use, and then gzipped the files by putting this to my ```.htaccess``` file. 

	:::apache
	# compress text, html, javascript, css, xml:
	AddOutputFilterByType DEFLATE text/plain
	AddOutputFilterByType DEFLATE text/html
	AddOutputFilterByType DEFLATE text/xml
	AddOutputFilterByType DEFLATE text/css
	AddOutputFilterByType DEFLATE application/xml
	AddOutputFilterByType DEFLATE application/xhtml+xml
	AddOutputFilterByType DEFLATE application/rss+xml
	AddOutputFilterByType DEFLATE application/javascript
	AddOutputFilterByType DEFLATE application/x-javascript

	# cache font files for 30+ days
	<FilesMatch "\.(woff|ttf|svg)$">
	Header set Cache-Control "max-age=2030400, public"
	</FilesMatch>

## Hosting 

I decided to host my site on [GitHub Pages](https://help.github.com/articles/user-organization-and-project-pages) where I can keep track of the code and the output files all in one place. The two types of Pages are User Pages and Project Pages. To use User Pages, you need to create a repo named  ```username/username.github.io```, and push the output folder to the master branch. The URL for the site then becomes ```username.github.io```. The Project Pages can put all the source code of your site alongside a ```gh-pages``` branch for the ```output``` folder. Mine is hosted via User Pages (so far). 

# Makefile

I use ```make html``` from the [Makefile](https://github.com/getpelican/pelican/blob/master/pelican/tools/templates/Makefile.in) a lot when developing my site to clean the ```output``` folder and deploy a new version of the site. When I'm ready to publish, I use ```make publish```, then the ```output``` folder is pushed to a remote. 

When I am editing posts, I use ```make devserver``` to locally host my website to ```localhost:8000``` and work in the ```drafts``` folder. Any time I need to fix the look of the website, I use ```make html``` then I reload the page. To stop the local server, I do ```make devstop```:

	:::bash
	devstop:
		$(BASEDIR)/develop_server.sh stop

# Git

Admittedly, I am a little wary of my Git skills. So what I have is the default ```output``` folder when testing my website, and a clone of my website in another. I use ```rsync``` when I'm ready to sync, so I put this in my Makefile:

	:::bash
	rsync_git:
		rsync -a $(OUTPUTDIR) $(OUTPUTDIR_GIT)

Now before the ```push```, I use the ```-A``` option to [commit the deletes](http://stackoverflow.com/questions/2190409/whats-the-difference-between-git-add-and-git-add-u/2190440#2190440). 

	:::console
	git add . -A
	git commit -am 'message here'
	git push origin master

## Further left to do

I'm very satisfied overall. Once you get the hang of it, it's a joy to tinker with the look of the website and committing multiple posts in parallel. I still would like to optimize for mobile browsing, cross-browser support and integrate stuff like IPython Notebooks, but those could come later. 


<!-- 
notes:

- mobile
- https://github.com/posativ/acrylamid
- local files
- low traffic
- notes for stuffffvf
- markdown, ipython notebooks, knitr
- mathjax
- margin
- disqus comments
- fonts, ubuntu, http://www.edwardtufte.com/tufte/index
- similar tim poisot
- scroll bar
- make file
- pygments
- email
- .gitignore
- pelicanconf
- make html to check, make html_github to publish
- status:draft
- writing posts
- github pages, user or gh-pages
- still to do: tags, little iffy on Jinja2, d3js graphic (http://raichev.net/blog.html)
- workflow
- d3js
- rss 
-->