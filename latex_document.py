from collections import OrderedDict
import yaml

from parsers import Parser
from profiles import *
from tex_processor import *
from create_base_files import *


class LaTeXDocument:
    def __init__(self, name, files_dir, images_dir, tables_dir) -> None:
        # Document attributes
        self._profile = None
        self._article_class = 'article'
        self._article_options = None

        # Project Name
        self._name = name.replace(' ', '_')

        # Folder locations
        self._files_dir = files_dir
        self._images_dir = images_dir
        self._tables_dir = tables_dir

        # Authors Info
        self._authors = OrderedDict()

        # All contents
        self._imports = []
        self._commands = []
        self._title = ''
        self._date = None
        self._frontmatter = ''
        self._abstract = ''
        self._keywords = []
        self._contents = OrderedDict()
        self._bibliography = {}

        # Graphics Info
        self._captions = {}
        self._labels = {}

    def __parse__(self, src, name, detect='auto'):
        parser = Parser(name, self._files_dir, self._images_dir, self._tables_dir, detect=detect)
        parsed = parser.parse(src)
        parsed_type = next(iter(parsed))
        return parsed, parsed_type

    def __append_page__(self, page, lines_only=False, is_appendix=False):
        self.imports(page._imports)
        self.commands(page._commands)
        for k, v in page._contents.items():
            if lines_only:
                if 'lines' in v.keys():
                    self._contents[self.__idx__() + k[-3:]] = v
            else:
                tag = '_ap' if is_appendix else k[-3:]
                self._contents[self.__idx__() + tag] = v

    def __section_handler__(self, level, src, name, label=None):
        tag = '_s' + str(level)
        parsed, parsed_type = self.__parse__(src, name)
        if parsed_type == 'lines':
            self._contents[self.__idx__() + tag] = {
                'name': name,
                'label': label or self.__default_label__(name),
                'lines': parsed[parsed_type],
            }
        elif parsed_type == 'page':
            self._contents[self.__idx__() + tag] = {
                'name': name,
                'label': label or self.__default_label__(name),
                'lines': '',
            }
            self.__append_page__(parsed[parsed_type], is_appendix=(True if level == 'a' else False))

    def profile(self, profile):
        process_profile(self, profile)

    # TODO: May not be required anymore
    #       since we have profiles
    def article_class(self, src, options=None):
        self._article_class = src.strip().split('.cls')[0]
        self._article_options = options

    def imports(self, packages):
        for p in packages:
            if p not in self._imports:
                self._imports.append(p)

    def commands(self, commands):
        for command in commands:
            if command not in self._commands:
                self._commands.append(command)

    def title(self, title):
        self._title = title.strip()

    def author(self, name, email, address):
        self._authors[len(self._authors)] = {'name': name, 'email': email, 'address': address}

    def date(self, date_str='today'):
        self._date = date_str.strip()

    def frontmatter(self, text):
        parsed, parsed_type = self.__parse__(text, None, detect='string')
        self._frontmatter = parsed[parsed_type]

    def abstract(self, src):
        parsed, parsed_type = self.__parse__(src, 'Abstract')
        if parsed_type == 'lines':
            self._abstract = parsed[parsed_type]
        elif parsed_type == 'page':
            lines = []
            for k, v in parsed[parsed_type]._contents.items():
                if k[-3:] == '_tt':
                    lines += [v['lines'].strip()]
            self._abstract += '\n\n'.join(lines)

    def keywords(self, words):
        self._keywords += words

    def section(self, src, name, label=None):
        return self.__section_handler__(1, src, name, label)

    def subsection(self, src, name, label=None):
        return self.__section_handler__(2, src, name, label)

    def subsubsection(self, src, name, label=None):
        return self.__section_handler__(3, src, name, label)

    def text(self, text):
        parsed, _ = self.__parse__(text, None, detect='string')
        self._contents[self.__idx__() + '_tt'] = {'lines': parsed['lines']}

    def page(self, page):
        name = page.split('.')[0]
        parsed, parsed_type = self.__parse__(page, name, detect='ext')
        self._contents[self.__idx__() + '_tt'] = {'lines': ''}
        self.__append_page__(parsed[parsed_type], lines_only=True)

    def table(self, src):
        assert (src[-3:] == '.py') or (
            src[-4:] == '.tex'
        ), '''
            Only .py or .tex files allowed for creating tables.
            Include captions and labels in the body of the table.
            '''
        name = src.split('.')[0]
        if src[-3:] == '.py':
            parsed, parsed_type = self.__parse__(src, name, detect='table')
        elif src[-4:] == '.tex':
            parsed, parsed_type = self.__parse__(src, name, detect='ext')
        if parsed_type == 'lines':
            self._contents[self.__idx__() + '_tb'] = {'lines': parsed[parsed_type]}
        elif parsed_type == 'page':
            parsed[parsed_type].finalize()
            self._contents[self.__idx__() + '_tb'] = {'lines': ''}
            self.__append_page__(parsed[parsed_type], lines_only=True)

    def graphics(self, src, figure='inline', top=False, centered=True, scale=1.0, width='textwidth'):
        self._contents[self.__idx__() + '_gx'] = {
            'src': src,
            'figure': figure,
            'top': top,
            'centered': centered,
            'scale': str(scale),
            'width': str(width),
            'caption': self._captions.get(src, None),
            'label': self._labels.get(src, None),
        }

    def newpage(self):
        self.text('\\newpage')

    def bibliography(self, src, style='plain'):
        if not os.path.isfile(self._files_dir + src):
            create_base_bib(self._files_dir + src)
        self._bibliography['style'] = style
        self._bibliography['src'] = src[:-4]

    def appendix(self, src, name=None, label=None):
        return self.__section_handler__('a', src, name or 'Appendix', label)

    def generate_tex(self, dst=None, images=True):
        generate_tex(self, dst, images)

    def compile(self, dst='./', processor='latexmk', images=True, clean=True, live=False):
        compile(self, dst, processor, images, clean, live)

    def __idx__(self):
        return str(len(self._contents))

    def __default_label__(self, s):
        s = s.strip().split(' ')
        s = ''.join(s)
        return 'sec:' + s[:4]

    def graphics_info(self, src):
        gs = yaml.load(open(self._files_dir + src), Loader=yaml.SafeLoader)
        if gs:
            for k, v in gs.items():
                if 'caption' in v:
                    self._captions[k] = v['caption']
                if 'label' in v:
                    self._labels[k] = v['label']

    def authors_info(self, src):
        au = yaml.load(open(self._files_dir + src), Loader=yaml.SafeLoader)
        if au:
            for k, v in au.items():
                self._authors[k] = {
                    'affil': v['affil'],
                    'name': v['name'],
                    'email': v.get('email', None),
                    'address': v.get('address', None),
                }

    def theme(self, theme='default'):
        if theme == 'default':
            page_color = '{white!100}'
            text_color = 'black'
        if theme == 'moonlight':
            page_color = '{black!80}'
            text_color = 'white'
        elif theme == 'dark':
            page_color = '{black!100}'
            text_color = 'white'
        elif theme == 'sepia':
            self.commands(
                ['\\definecolor{sepia_background}{RGB}{248,241,227}', '\\definecolor{sepia_text}{RGB}{79,50,28}']
            )
            page_color = '{sepia_background}'
            text_color = 'sepia_text'
        elif theme == 'dusk':
            self.commands(
                ['\\definecolor{dusk_background}{RGB}{43,41,37}', '\\definecolor{dusk_text}{RGB}{243,232,212}']
            )
            page_color = '{dusk_background}'
            text_color = 'dusk_text'

        self.imports(['xcolor', 'pagecolor'])
        self.commands(['\\pagecolor' + page_color, '\\color{' + text_color + '}'])
