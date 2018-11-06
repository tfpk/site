#!/usr/bin/python3

import os
from os.path import join as path_join
import json
import glob

from jinja2 import Environment, FileSystemLoader, select_autoescape

os.chdir(os.path.dirname(__file__))

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

for page in glob.glob('**/_*.html', recursive=True):
    path, file_name = os.path.split(page)
    name = file_name.replace(".html", "")[1:]
    try:
        with open(path_join(path, f"{name}.json"), 'r') as model:
            template = env.get_template(page)
            formatted = template.render(**json.load(model))
            out_path = f"../{path}"
            os.makedirs(out_path, exist_ok=True)
            with open(path_join(out_path, f"{name}.html"), 'w') as final:
                final.write(formatted)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find matching json for template.")
