from dewar import Site
from dewar.helpers import *
site = Site()

@site.register('index.html')
def index():
    return render_template('index.html', **load_json_data('index.json'))

@site.register('blogs/<name>.html')
def blogs():
    blogs = {}
    blog_data = load_data_dir('blogs')
    for blog in blog_data:
        html = load_md(blog_data[blog])
        blogs[blog.replace('.md', '')] = render_template('blog.html', mkdown=html)

    return blogs

if __name__ == '__main__':
    site.render(path='docs/')
