~~~
md_name = "cse_site"
name = "Making a CSE Site"
desc = "A guide to making a website on CSE"
image = "images/unsw_computing.jpg"
~~~

# CSE HTML

One thing every programmer should know how to do is make a website. UNSW makes this a lot easier, giving us free hosting and a free domain name.
With a website, you can work on projects and do cool stuff.

This guide will run through some of the basics of website hosting, and how to confiugre a website using the CSE services provided.
NOTE: This guide is provided AS-IS and WITHOUT ANY WARRANTY. It is possible the hosting services will change from when it is written (November 2018).
Users should check the UNSW CSE responsible use policies. In short, don't be evil.

## Assumptions

For this guide, it will be assumed the user has a basic understanding of UNIX and HTML. The concepts here should be covered in COMP1511/COMP1917 and COMP1531/COMP2041.

# Your Website

On CSE servers, you have two automatic URLs. They are:

-   `http://web.cse.unsw.edu.au/~zXXXXXXX/`
-   `http://z5205060.web.cse.unsw.edu.au/`

By default, these addresses don't serve anything. They may return a 403 (Access Denied) or 404 (File not Found) error. Let's fix that.

## Serving Static HTML

1) Create a public HTML directory. 

    mkdir ~/public_html/

This is the root directory from which all web accesses take place. Files are prohibited from going above this directory as a security measure.
For example, you can't try and access `~` from `~/public_html/`, so you can't steal a lecturer's `~/secret_exam_files`

2) Create an HTML file

    $ touch ~/public_html/<your_html>.html

And fill it with HTML.

3) Set the access permissions

    $ chmod 644 ~/public_html/<your_html>.html

4) Access the page

 - `http://web.cse.unsw.edu.au/~zXXXXXXX/<your_html>.html`


## Configuring your page

All the controls for what redirects happen within your site are contained in a `.htaccess` file. It also specifies the way files are served.
You can set up a `.htaccess`in any directory. Some useful configuration for a base directory:

    RewriteEngine On
    RewriteCond %{HTTP_HOST} !zXXXXXXX.web.cse.unsw.edu.au [NC]
    RewriteRule (.*) http://zXXXXXXX.web.cse.unsw.edu.au/$1 [R=301,L]

    # TURN ON DEBUG MODE:
    # SetHandler application/x-setuid-cgid

    <Files "robots.txt">
        SetHandler text/plain
    </Files>
    <Files "my_app">
        SetHandler application/x-setuid-cgi
    </Files>

    ErrorDocument 404 /errors/404.html

Here are four of the most useful constructs you can use to modify your site:

*   The first (when you replace the X's with your zID) will redirect from http://cse.unsw.edu.au/~zXXXXXXX/... to http://zXXXXXXX.cse.unsw.edu.au/...
*   The second, when the comment is removed, will set all files into debug mode. This is really useful if you get unknown errors, you can see a full error from the server/your programs.
*   The third is the "Files" tag which lets you apply settings (such as a SetHandler) to individual files or to files matching a regular expression.
*   The fourth is the "ErrorDocument" tag which allows custom error pages.

## Interactive apps

Using CGI and Python Flask, it's easy to create interactive apps.

### CGI

CGI (Common Gateway Interface) is a protocol which allows internet connected users to request programs be run remotely. Those programs then output their responses over the internet.
This allows you to write a program that prints out a HTTP response, and thus create a web server.

### Setup

First, create a directory structure like so:

    - directory/ [either `~/public_html` or a subdirectory of it]
      - static/
        - example.css
        - example.js
        - example.png
      - templates/
        - main.html
      - <yourapp>.cgi

#### `static`

This is where you will link to your "static" files, such as images and css.
Set it up with:

    $ chmod 755 static/
    $ chmod 644 static/*

(You need to repeat the second command every time you add files)

You can access these files in templates using:

    url_for('static', filename='example.js')

#### `templates`

Here is where you can keep your jinja/flask templates. 
No setup is required.

#### `<yourapp>.cgi`

Here is where the business of your application is.

Set up the file with:

    $ chmod 755 <yourapp>.cgi

Here is some starter code:

    #!/usr/bin/python3
    # This tells the computer that we want to execute this cgi script using python3

    from wsgiref.handlers import CGIHandler
    from werkzeug.contrib.fixers import ProxyFix

    from flask import render_template
    from flask import Flask
    from flask import Response

    app = Flask(__name__)

    @app.route('/hello/<name>')
    def hello(name=None):
        return Response(render_template('hello.html', name=name))
    # NOTE: You have to wrap "render_template" in this Response object
    # This ensures that it's given proper return headers

    if __name__ == '__main__':
        app.wsgi_app = ProxyFix(app.wsgi_app) # Setup HTTP headers
        CGIHandler().run(app)

## Where to go from here

Lots more information can be found at:

-   [Taggi: Creating a Website](https://taggi.cse.unsw.edu.au/FAQ/Creating_a_website/)
-   [Taggi: CGI Scripts](https://taggi.cse.unsw.edu.au/FAQ/CGI_scripts/)

## Weird stuff that happens

*   `TypeError: Response is not iterable`: Use `make_repsonse` instead.

