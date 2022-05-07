from utils import *

import psutil
import os


def generate_tex(doc, dst, images):
    if not images:
        generate_blank_images(doc)

    if dst == None:
        dst = doc._files_dir

    _class_text = '\\documentclass'

    if doc._article_options:
        _class_text += '[' + ','.join(doc._article_options) + ']'
    _class_text += '{' + doc._article_class + '}'

    lines = [_class_text]

    # Imports
    doc.imports(['graphicx'])
    for i in doc._imports:
        if i[0] == '[' or i[0] == '{':
            lines += ['\\usepackage' + i]
        else:
            lines += ['\\usepackage{' + i + '}']

    # Commands
    if images:
        lines += ['\\graphicspath{{../' + doc._images_dir + '}}']
    else:
        lines += ['\\graphicspath{{../' + doc._images_dir + '__images__/}}']
    lines += doc._commands

    # Title
    if doc._title is not '':
        lines += ['\\title{' + doc._title + '}']

    # Authors
    for k, v in doc._authors.items():
        lines += ['\\author[' + v['affil'] + ']{' + v['name'] + '}']
        if v['address']:
            lines += ['\\affil[' + v['affil'] + ']{' + v['address'] + '}']
        if v['email']:
            lines += ['\\affil[' + v['affil'] + ']{\\texttt{' + v['email'] + '}}']

    # Frontmatter
    if doc._frontmatter is not '':
        lines += [doc._frontmatter]

    # Date
    if doc._date:
        lines += ['\\date{\\' + doc._date + '}']

    # Document
    lines += ['\\begin{document}']

    # Maketitle before abstract for ICLR
    if doc._profile == 'iclr':
        lines += ['\\maketitle']

    # Abstract
    if doc._abstract is not '':
        lines += ['\\begin{abstract}']
        lines += [doc._abstract]
        lines += ['\\end{abstract}']

    # Keywords
    if doc._keywords != []:
        lines += ['\\begin{keyword}']
        lines += [' \sep '.join(doc._keywords)]
        lines += ['\\end{keyword}']

    # Maketitle before abstract for Elsevier
    if doc._profile == 'elsevier':
        lines += ['\\maketitle']

    # Sections, Images, Tables and Text
    for k, v in doc._contents.items():
        tag = k[-3:]
        if tag == '_s1':
            lines += ['\\section{' + v['name'] + '}']
            lines += ['\\label{' + v['label'] + '}']
            lines += [v['lines']]
        if tag == '_s2':
            lines += ['\\subsection{' + v['name'] + '}']
            lines += ['\\label{' + v['label'] + '}']
            lines += [v['lines']]
        if tag == '_s3':
            lines += ['\\subsubsection{' + v['name'] + '}']
            lines += ['\\label{' + v['label'] + '}']
            lines += [v['lines']]
        if tag == '_gx':
            if v['figure'] == 'inline':
                lines += ['']
            else:
                top = '*' if v['top'] else ''
                lines += ['\\begin{figure' + top + '}[' + v['figure'] + ']']
                if v['centered']:
                    lines += ['\\centering']
            lines += [
                '\\includegraphics['
                + 'scale='
                + v['scale']
                + ','
                + 'width=\\'
                + v['width']
                + ']'
                + '{'
                + v['src']
                + '}'
            ]
            if v['figure'] == 'inline':
                lines += ['']
            else:
                if v['caption']:
                    lines += ['\\caption{' + v['caption'] + '}']
                if v['label']:
                    lines += ['\\label{' + v['label'] + '}']
                lines += ['\\end{figure' + top + '}']
        if tag == '_tb':
            lines += [v['lines']]
        if tag == '_tt':
            lines += [v['lines']]
        lines += ['\n']

    # Bibliography
    if doc._bibliography:
        lines += ['\\bibliographystyle{' + doc._bibliography['style'] + '}']
        lines += ['\\bibliography{' + doc._bibliography['src'] + '}']

    # Appendix
    for k, v in doc._contents.items():
        tag = k[-3:]
        if tag == '_sa':
            lines += ['\\newpage']
            lines += ['\\appendix']
            lines += ['\\section{' + v['name'] + '}']
            lines += ['\\label{' + v['label'] + '}']
        if tag == '_ap':
            lines += [v['lines']]
        lines += ['\n']

    lines += ['\\end{document}']

    contents = '\n'.join(lines)
    open(dst + doc._name + '.tex', 'w+').writelines(contents)
    if images:
        print('The TeX file has been generated.')
    else:
        print('The TeX file with blank images has been generated.')
    return contents


def compile(doc, dst, processor, images, clean, live):
    # check is latexmk is already running
    if is_live_server_running():
        print('live server already running. genereting tex...')
        doc.generate_tex(images=images)
        return

    cmd = 'cd ' + doc._files_dir
    cmd += ' &&'

    # clean
    ext = ['aux', 'bbl', 'blg', 'fdb_latexmk', 'fls', 'log', 'out', 'pdf', 'synctex.gz']
    if clean:
        for e in ext:
            cmd += ' rm ' + doc._name + '.' + e + ';'

    if processor == 'pdflatex':
        if doc._bibliography:
            pdflatex_args = ' -draftmode'
        else:
            pdflatex_args = ''

        # pdflatex
        cmd += ' pdflatex' + pdflatex_args
        cmd += ' ' + doc._name + '.tex'
        cmd += ' &&'

        if doc._bibliography:
            # bibtex
            cmd += ' bibtex'
            cmd += ' ' + doc._name + '.aux'
            cmd += ' &&'

            # pdflatex
            cmd += ' pdflatex' + pdflatex_args
            cmd += ' ' + doc._name + '.tex'
            cmd += ' &&'

            # pdflatex
            cmd += ' pdflatex'
            cmd += ' ' + doc._name + '.tex'
            cmd += ' &&'

    elif processor == 'latexmk':
        cmd += ' latexmk -pdf'
        if live:
            cmd += ' -pvc'
        cmd += ' ' + doc._name + '.tex'
        cmd += ' &&'

    # copy pdf to dst
    cmd += ' cd - && cp ' + doc._files_dir + doc._name + '.pdf ' + dst
    cmd += ' &&'

    cmd += ' echo "All complete."'

    print(cmd)
    doc.generate_tex(images=images)
    return os.system(cmd)


def is_live_server_running():
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if 'perl' in p.name():
            if 'latexmk' in p.cmdline()[1]:
                return 1

    return 0
