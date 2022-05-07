from latex_document import LaTeXDocument


class LaTeXPage(LaTeXDocument):
    def __init__(self, name, files_dir, images_dir, tables_dir) -> None:
        super().__init__(name, files_dir, images_dir, tables_dir)

        # Allowed super function
        # imports
        # commands
        # text
        # theme

    # Restrict access to certain functions
    def block_method(self, var):
        err = '''
            Adding `{{var}}' to a LaTeXPage is prohibited.
            Add it to the LaTeXDocument that includes this LaTeXPage.
        '''
        err = err.replace('{{var}}', var)
        raise SyntaxError(err)

    def profile(self, *a, **k):
        self.block_method('profile')

    def article_class(self, *a, **k):
        self.block_method('article_class')

    def title(self, *a, **k):
        self.block_method('title')

    def author(self, *a, **k):
        self.block_method('author')

    def date(self, *a, **k):
        self.block_method('date')

    def frontmatter(self, *a, **k):
        self.block_method('frontmatter')

    def abstract(self, *a, **k):
        self.block_method('abstract')

    def keywords(self, *a, **k):
        self.block_method('keywords')

    def section(self, *a, **k):
        self.block_method('section')

    def subsection(self, *a, **k):
        self.block_method('subsection')

    def subsubsection(self, *a, **k):
        self.block_method('subsubsection')

    def page(self, *a, **k):
        self.block_method('page')

    def table(self, *a, **k):
        self.block_method('table')

    def graphics(self, *a, **k):
        self.block_method('graphics')

    def bibliography(self, *a, **k):
        self.block_method('bibliogrpahy')

    def graphics_info(self, *a, **k):
        self.block_method('graphics_info')

    def authors_info(self, *a, **k):
        self.block_method('authors_info')
