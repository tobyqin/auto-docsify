"""
Script to build document site.
"""

import re
import os
from os.path import join, dirname, exists, abspath
from shutil import copyfile
from sys import argv
from pathlib import Path


assert len(argv) == 2, 'Must set parmaters for builder.py [repo]'
repo_name = argv[1]


def get_env(name, default=''):
    v = os.environ.get(name, default)
    return default if not v else v


app_dir = abspath(dirname(dirname(__file__)))
repo_dir = join(app_dir, 'repo')
site_dir = join(app_dir, 'site')
template_dir = join(app_dir, 'template')

site_name = get_env('DOC_SITE_NAME', repo_name)
site_name_safe = site_name.replace(' ', '-').lower()
doc_index = get_env('DOC_INDEX', 'README.md')  #
doc_dir = get_env('DOC_DIR', 'docs')  # from
site_path = get_env('DOC_SITE_PATH', doc_dir)  # to
site_logo = get_env('DOC_SITE_LOGO', '')
doc_repo_url = get_env('DOC_REPO_URL', '')
site_nav = get_env(
    'DOC_SITE_NAV', 'Github|https://github.com/tobyqin,Deploy Site Like This?|https://tobyqin.cn/docsify')
load_side_bar = False
load_nav_bar = True if site_nav else False


def overwrite_file(src, dest):
    print(f'{src} => {dest}')
    p_dir = dirname(dest)

    if exists(dest):
        os.remove(dest)

    if not exists(p_dir):
        os.mkdir(p_dir)

    copyfile(src, dest)


def incremental_copy_tree(src, dst):
    """copy tree with incremental:
    0. ignore files in destination if not in source.
    1. over write files in destination if existed in source.
    """
    print(f'{src} => {dst}')
    source_dir = Path(src)
    for item in source_dir.glob('**/*'):
        if item.is_file():

            from_name = str(item)
            target_name = from_name.replace(src, dst)

            print('Copy: {} => {}'.format(from_name, target_name))
            if exists(target_name):
                os.remove(target_name)

            target_dir = dirname(target_name)
            if not exists(target_dir):
                os.mkdir(target_dir)

            copyfile(from_name, target_name)


def replace_content(file, replace_from, replace_to):
    f = Path(file)
    c = f.read_text()
    c = c.replace(replace_from, replace_to)
    f.write_text(c)


def build_edit_link(url):
    return """
    var url = '{url}';
    var fileUpdated = '> Last modified {docsify-updated}'
    var editHtml = fileUpdated + ' [:memo: Edit Document](' + url + ')';
    return (editHtml + '\\n----\\n' + html);
    """.replace('{url}', url)


def better_name(name):
    def cap_first(word: str):
        return word[0].upper()+word[1:] if word else word

    words = re.split('[^\w]+', name)
    return ' '.join([cap_first(w) for w in words])


# docs/ dir
doc_dir_full = abspath(join(repo_dir, f'{repo_name}/{doc_dir}'))
doc_site_path_full = join(site_dir, site_path)
if exists(doc_dir_full):
    incremental_copy_tree(doc_dir_full, doc_site_path_full)
    load_side_bar = True

# README.md
overwrite_file(join(repo_dir, f'{repo_name}/{doc_index}'),
               join(doc_site_path_full, 'README.md'))

# redirect index
redirect_index = join(site_dir, 'index.html')
if not exists(redirect_index):
    overwrite_file(join(template_dir, 'index-redirect.html'), redirect_index)
    replace_content(redirect_index, '{doc_site_path}', site_path)


# docsify index
docsify_index = join(doc_site_path_full, 'index.html')
if not exists(docsify_index):
    overwrite_file(join(template_dir, 'index-docsify.html'), docsify_index)


replace_content(docsify_index, '{site_name}', site_name)
replace_content(docsify_index, '{site_name_safe}', site_name_safe)
replace_content(docsify_index, '{site_name_better}', better_name(site_name))

if site_logo:
    replace_content(docsify_index, '//{site_logo}', f"logo: '{site_logo}',")

replace_content(docsify_index, '{load_nav_bar}', str(load_nav_bar).lower())
replace_content(docsify_index, '{load_side_bar}', str(load_side_bar).lower())

if doc_repo_url:
    replace_content(
        docsify_index, '//{edit_doc_func}', build_edit_link(doc_repo_url))


# build side nav
if load_side_bar:
    print('build side nav ...')
    side_bar_file = join(doc_site_path_full, '_sidebar.md')
    content = "- [Home](README.md)\n"

    for f in Path(doc_dir_full).glob('*.md'):
        nav_name = better_name(f.stem)
        content += f"- [{nav_name}]({f.name})\n"

    Path(side_bar_file).write_text(content)


if load_nav_bar:
    print('build top nav...')
    # example: 'A|http://a,B|http://b'
    nav_bar_file = join(doc_site_path_full, '_navbar.md')
    content = ''

    for nav in site_nav.split(','):
        nav_name, url = nav.strip().split('|')
        content += f"- [{nav_name.strip()}]({url})\n"

    Path(nav_bar_file).write_text(content)


# docsify libs
doc_lib_dir = 'docsify-libs'
incremental_copy_tree(join(template_dir, doc_lib_dir),
                      join(doc_site_path_full, doc_lib_dir))
