import os
import sys
import importlib
from create_base_files import *


class Parser:
    def __init__(self, name, files_dir, images_dir, tables_dir, detect) -> None:
        self._name = name
        self._files_dir = files_dir
        self._images_dir = images_dir
        self._tables_dir = tables_dir
        self._detect = detect

    def parse(self, src, root='./'):
        if self._detect in ['auto', 'ext', 'table']:
            if src[-3:] == '.py':
                if self._detect == 'table':
                    parsed = self.py_parser(src, mode=self._detect)
                else:
                    parsed = self.py_parser(src, mode='page')
            elif src[-4:] == '.tex':
                parsed = self.tex_parser(self._files_dir + src)
            elif src[-4:] == '.bib':
                parsed = self.tex_parser(self._files_dir + src)
            else:
                raise NotImplementedError(src + ' cannot be parsed')
        elif self._detect == 'string':
            parsed = self.string_parser(src)
        return parsed

    def py_parser(self, src, mode='page'):
        if mode == 'page':
            if not os.path.isfile(src):
                create_base_py(
                    src,
                    **{
                        'name': self._name,
                        'files_dir': self._files_dir,
                        'images_dir': self._images_dir,
                        'tables_dir': self._tables_dir,
                    }
                )
        elif mode == 'table':
            if not os.path.isfile(src):
                create_base_table(
                    src,
                    **{
                        'name': self._name,
                        'files_dir': self._files_dir,
                        'images_dir': self._images_dir,
                        'tables_dir': self._tables_dir,
                    }
                )
            if not os.path.isfile(self._tables_dir + src[:-3] + '.csv'):
                create_base_csv(self._tables_dir + src[:-3] + '.csv')
        sys.path.append(self._files_dir)
        module = importlib.import_module(src[:-3])
        page = module.main(0)
        return {'page': page}

    def tex_parser(self, src):
        if not os.path.isfile(src):
            create_base_tex(src)

        keywords = ['\\documentclass', '\\usepackage', '\\begin{document', '\\end{document']
        lines_ = open(src).read().strip().split('\n')

        lines = ['']
        for l in lines_:
            l = l.strip()
            if l == '':
                lines += '\n'
                continue
            skip = False
            for k in keywords:
                if k in l:
                    skip = True
                    break
            if not skip:
                lines += [l]
        lines += ['']
        lines = '\n'.join(lines)
        return {'lines': lines}

    def string_parser(self, src):
        lines = ['']
        lines += [x.strip() for x in src.strip().split('\n')]
        lines += ''
        lines = '\n'.join(lines)
        return {'lines': lines}
