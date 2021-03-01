import os


def generate_tex(doc, dst=None):
    if dst == None:
        dst = doc._files_dir
    class_text = '\\documentclass'
    if doc._article_options:
        class_text += '['+','.join(doc._article_options)+']'
    class_text += '{'+doc._article_class+'}'

    lines = [class_text]

    # Imports
    doc.imports(['graphicx'])
    for i in doc._imports:
        if i[0] == '[' or i[0] == '{':
            lines += ['\\usepackage'+i]
        else:
            lines += ['\\usepackage{'+i+'}']

    # Commands
    lines += ['\\graphicspath{{../'+doc._images_dir+'}}']
    lines += doc._commands

    # Title
    lines += ['\\title{'+doc._title+'}']

    # Authors
    for k, v in doc._authors.items():
        lines += ['\\author['+v['affil']+']{'+v['name']+'}']
        if v['address']:
            lines += ['\\affil['+v['affil']+']{'+v['address']+'}']
        if v['email']:
            lines += ['\\affil['+v['affil']+']{\\texttt{'+v['email']+'}}']

    # Date
    lines += ['\\date{'+doc._date+'}']

    # Document
    lines += ['\\begin{document}']
    lines += ['\\maketitle']

    # Abstract
    if doc._abstract != '':
        lines += ['\\begin{abstract}']
        lines += [doc._abstract]
        lines += ['\\end{abstract}']

    # Sections, Images, Tables and Text
    for k, v in doc._contents.items():
        tag = k[-3:]
        if tag == '_s1':
            lines += ['\\section{'+v['name']+'}']
            lines += ['\\label{'+v['label']+'}']
            lines += [v['lines']]
        if tag == '_s2':
            lines += ['\\subsection{'+v['name']+'}']
            lines += ['\\label{'+v['label']+'}']
            lines += [v['lines']]
        if tag == '_s3':
            lines += ['\\subsubsection{'+v['name']+'}']
            lines += ['\\label{'+v['label']+'}']
            lines += [v['lines']]
        if tag == '_gx':
            if v['figure'] == 'inline':
                lines += ['']
            else:
                top = '*' if v['top'] else ''
                lines += ['\\begin{figure'+top+'}['+v['figure']+']']
                if v['center']:
                    lines += ['\\centering']
            lines += ['\\includegraphics[' +
                      'scale='+v['scale']+',' +
                      'width='+v['width']+']' +
                      '{'+v['src']+'}']
            if v['figure'] == 'inline':
                lines += ['']
            else:
                if v['caption']:
                    lines += ['\\caption{'+v['caption']+'}']
                if v['label']:
                    lines += ['\\label{'+v['label']+'}']
                lines += ['\\end{figure'+top+'}']
        if tag == '_tb':
            lines += [v['lines']]
        if tag == '_tt':
            lines += [v['lines']]
        lines += ['\n']

    # Bibliography
    if doc._bibliography:
        lines += ['\\bibliographystyle{'+doc._bibliography['style']+'}']
        lines += ['\\bibliography{'+doc._bibliography['src']+'}']

    lines += ['\\end{document}']

    contents = '\n'.join(lines)
    open(dst+doc._name+'.tex', 'w+').writelines(contents)
    return contents


def compile(doc, dst='./', clean=True):
    doc.generate_tex()

    cmd = 'cd '+doc._files_dir
    cmd += ' &&'

    # clean
    ext = ['aux', 'bbl', 'blg', 'fdb_latexmk',
           'fls', 'log', 'out', 'pdf', 'synctex.gz']
    if clean:
        for e in ext:
            cmd += ' rm '+doc._name+'.'+e+';'

    if doc._bibliography:
        pdflatex_args = ' -draftmode'
    else:
        pdflatex_args = ''

    # pdflatex
    cmd += ' pdflatex'+pdflatex_args
    cmd += ' '+doc._name+'.tex'
    cmd += ' &&'

    if doc._bibliography:
        # bibtex
        cmd += ' bibtex'
        cmd += ' '+doc._name+'.aux'
        cmd += ' &&'

        # pdflatex
        cmd += ' pdflatex'+pdflatex_args
        cmd += ' '+doc._name+'.tex'
        cmd += ' &&'

        # pdflatex
        cmd += ' pdflatex'
        cmd += ' '+doc._name+'.tex'
        cmd += ' &&'

    # move pdf to dst
    cmd += ' cd - && mv '+doc._files_dir+doc._name+'.pdf '+dst
    cmd += ' &&'

    cmd += ' echo "All complete."'

    print(cmd)
    return os.system(cmd)
