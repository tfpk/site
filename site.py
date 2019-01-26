from dewar import Site
from dewar.helpers import *

site = Site(create_backups=True)

@site.register('index.html')
def index():
    return render_template('index.html', **eval(load_data('index.py')))

@site.register('blog_list.html')
def blog_list():
    blogs = load_json_data('blogs.json')
    for blog in blogs:
        blog['link'] = url_for('blogs', name=blog['md_name'])
    return render_template('blog_list.html', blogs=blogs)

@site.register('project_list.html')
def project_list():
    return render_template('project_list.html')

@site.register('blogs/<name>.html')
def blogs():
    blogs = {}
    blog_data = load_data_dir('blogs')
    for blog in blog_data:
        html = load_md(blog_data[blog])
        blogs[blog.replace('.md', '')] = render_template('blog.html', mkdown=html)
    return blogs

@site.register("CNAME")
def cname():
    return "tfpk.io"

if __name__ == '__main__':
    site.render(path='docs/')
