from pathlib import Path

from dewar import Site
from dewar.helpers import *

site = Site()

@site.register('index.html')
def index():
    data = eval(load_data('index.py'))
    data['bio_md'] = load_md(data['bio'])
    return render_template('index.html', **data)

def load_list_from_md(file_list):
    md_list = {}
    for key in file_list:
        _, html = load_pymd(file_list[key])
        md_list[get_stem(key)] = render_template('markdown.html', mkdown=html)
    return md_list

def get_stem(name):
    return Path(name).stem

@site.register('blog_list.html')
def blog_list():
    blogs_list = load_data_dir('blogs')
    blogs = []
    for blog in blogs_list:
        blog_data, _ = load_pymd(blogs_list[blog])
        blog_data['link'] = url_for('blogs', name=get_stem(blog))
        blogs.append(blog_data)
    return render_template('blog_list.html', blogs=blogs)

@site.register('project_list.html')
def project_list():
    projects_data = load_json_data('projects.json')
    return render_template('project_list.html', projects=projects_data)

@site.register('experience/<name>.html')
def experience():
    experience_data = load_data_dir('experience')
    return load_list_from_md(experience_data)

@site.register('blogs/<name>.html')
def blogs():
    blogs_data = load_data_dir('blogs')
    return load_list_from_md(blogs_data)

@site.register("CNAME")
def cname():
    return "tfpk.io"

if __name__ == '__main__':
    site.render(path='docs/')
