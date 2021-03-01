from latex_document import LaTeXDocument


class LaTeXPage(LaTeXDocument):

    def __init__(self, name, files_dir, images_dir) -> None:
        super().__init__(name, files_dir, images_dir)

    # Override Super Methods
    def text(self, src):
        super().text(src)

    def graphics(self, src,
                 figure='inline',
                 top=False,
                 center=True,
                 scale=1.0,
                 width='\\textwidth'):
        super().graphics(src, figure=figure, top=top,
                         center=center, scale=scale, width=width)

    def table(self, src):
        super().table(src)

    # Restrict Super Access
    def block_method(self, var):
        err = '''
            Adding `{{var}}' to a LaTeXPage is prohibited.
            Add it to the LaTeXDocument that includes this LaTeXPage.
        '''
        err = err.replace('{{var}}', var)
        raise SyntaxError(err)

    def title(self, *a, **k):
        self.block_method('title')

    def author(self, *a, **k):
        self.block_method('author')

    def date(self, *a, **k):
        self.block_method('date')

    def abstract(self, *a, **k):
        self.block_method('abstract')

    def section(self, *a, **k):
        self.block_method('section')

    def subsection(self, *a, **k):
        self.block_method('subsection')

    def subsubsection(self, *a, **k):
        self.block_method('subsubsection')

    def bibliography(self, *a, **k):
        self.block_method('bibliogrpahy')

    def authors_info(self, *a, **k):
        self.block_method('authors_info')
