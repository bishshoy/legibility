import os


def create_base_py(src, **args):
    curr_dir = os.path.dirname(__file__)
    snippet = open(curr_dir + '/snippets/py_snippet.py').read()

    variables = [
        'name',
        'files_dir',
        'images_dir',
        'tables_dir',
    ]

    for v in variables:
        snippet = snippet.replace('{{' + v + '}}', eval('args[\'' + v + '\']'))

    open(src, 'w+').writelines(snippet)


def create_base_tex(src):
    curr_dir = os.path.dirname(__file__)
    snippet = open(curr_dir + '/snippets/tex_snippet.tex').read()
    open(src, 'w+').writelines(snippet)


def create_base_bib(src):
    curr_dir = os.path.dirname(__file__)
    snippet = open(curr_dir + '/snippets/bib_snippet.bib').read()
    open(src, 'w+').writelines(snippet)


def create_base_table(src, **args):
    curr_dir = os.path.dirname(__file__)
    snippet = open(curr_dir + '/snippets/table_snippet.py').read()

    variables = [
        'name',
        'files_dir',
        'images_dir',
        'tables_dir',
    ]

    for v in variables:
        snippet = snippet.replace('{{' + v + '}}', eval('args[\'' + v + '\']'))

    open(src, 'w+').writelines(snippet)


def create_base_csv(src):
    curr_dir = os.path.dirname(__file__)
    snippet = open(curr_dir + '/snippets/csv_snippet.csv').read()
    open(src, 'w+').writelines(snippet)
