from latex_page import LaTeXPage


class LaTeXTable(LaTeXPage):
    def __init__(self, name, files_dir, images_dir, tables_dir):
        super().__init__(name, files_dir, images_dir, tables_dir)

        # Super functions
        # imports
        # commands
        # text
        # theme

        super().imports(['booktabs', 'multirow', 'soul', 'changepage', 'threeparttable'])

        self._csv = self._tables_dir + name + '.csv'
        self._values = []
        self._num_rows = 0
        self._num_columns = 0
        self._alignment = {}
        self._initialized = False
        self._finalized = False

        self._location = 't'
        self._centered = True

        self._full_horizontal_locations = {}
        self._horizontal_locations = {}
        self._vertical_locations = {}

        self._cell_merges = {}

        self._bold_values = []
        self._underlined_values = []

        self._caption = None
        self._label = None

    def initialize(self):
        lines_ = open(self._csv).read().strip().split('\n')

        self._num_rows = len(lines_)

        for l in lines_:
            vals = l.strip().split(',')
            self._num_columns = max(self._num_columns, len(vals))

        self._values = []
        for x in range(self._num_rows):
            self._values.append([''] * self._num_columns)

        for x, l in enumerate(lines_):
            vals = l.strip().split(',')
            for y, v in enumerate(vals):
                self._values[x][y] = v

        for x in range(self._num_columns):
            self._alignment[x] = 'center'

        for x in range(self._num_rows + 1):
            self._full_horizontal_locations[x] = False
            self._horizontal_locations[x] = []

        for x in range(self._num_columns + 1):
            self._vertical_locations[x] = False

        self._initialized = True

    def location(self, location='top', centered=True):
        _location = {'top': 't', 'here': 'h', 'bottom': 'b'}
        assert location in _location.keys(), 'location must be ' + ' '.join(_location.keys())
        self._location = _location[location]
        self._centered = centered

    def left_align(self, *columns):
        assert self._initialized, 'table is not initialized'
        for column in columns:
            assert column > 0 and column <= self._num_columns, 'column ' + str(column) + ' does not exist'
            self._alignment[column - 1] = 'left'

    def right_align(self, *columns):
        assert self._initialized, 'table is not initialized'
        for column in columns:
            assert column > 0 and column <= self._num_columns, 'column ' + str(column) + ' does not exist'
            self._alignment[column - 1] = 'right'

    def center_align(self, *columns):
        assert self._initialized, 'table is not initialized'
        for column in columns:
            assert column > 0 and column <= self._num_columns, 'column ' + str(column) + ' does not exist'
            self._alignment[column - 1] = 'center'

    def full_horizontal_line(self, *locations):
        for l in locations:
            assert l >= 0 and l <= self._num_rows, 'row ' + str(l) + ' does not exist'
            self._full_horizontal_locations[l] = True

    def horizontal_line(self, row, start, end):
        assert row >= 0 and row <= self._num_rows, 'row outside the table'
        for c in [start, end]:
            assert c >= 0 and c <= self._num_columns, 'column outside the table'
        assert start < end, 'end must be greater than start'
        self._horizontal_locations[row].append((start, end))

    def vertical_line(self, *locations):
        for l in locations:
            assert l >= 0 and l <= self._num_columns, 'column ' + str(l) + ' does not exist'
            self._vertical_locations[l] = True

    def grid(self):
        [self.full_horizontal_line(x) for x in range(self._num_rows + 1)]
        [self.vertical_line(x) for x in range(self._num_columns + 1)]

    def horizontal_merge(self, from_cell, num_columns=2, alignment='center'):
        assert from_cell[0] > 0 and from_cell[0] <= self._num_rows, 'from_cell outside the table'
        assert from_cell[1] > 0 and from_cell[1] <= self._num_columns, 'from_cell outside the table'
        _alignment = {'left': 'l', 'right': 'r', 'center': 'c'}
        assert alignment in _alignment.keys(), 'alignment must be ' + ' '.join(_alignment.keys())
        self._cell_merges[(from_cell[0] - 1, from_cell[1] - 1)] = ('horizontal', num_columns, _alignment[alignment])

    def vertical_merge(self, from_cell, num_rows):
        assert from_cell[0] > 0 and from_cell[0] <= self._num_rows, 'from_cell outside the table'
        assert from_cell[1] > 0 and from_cell[1] <= self._num_columns, 'from_cell outside the table'
        self._cell_merges[(from_cell[0] - 1, from_cell[1] - 1)] = ('vertical', num_rows, '')

    def bold(self, *cells):
        for cell in cells:
            assert isinstance(cell, list) or isinstance(cell, tuple), 'cell coordinates must be tuples or lists'
            assert len(cell) == 2, 'cell coordinates must contain two values'
            self._bold_values.append([cell[0] - 1, cell[1] - 1])

    def bold_rows(self, *rows):
        for row in rows:
            assert row > 0 and row <= self._num_rows, 'row outside the table'
            for j in range(self._num_columns):
                self.bold([row, j + 1])

    def underline(self, *cells):
        for cell in cells:
            assert isinstance(cell, list) or isinstance(cell, tuple), 'cell coordinates must be tuples or lists'
            assert len(cell) == 2, 'cell coordinates must contain two values'
            self._underlined_values.append([cell[0] - 1, cell[1] - 1])

    def underline_rows(self, *rows):
        for row in rows:
            assert row > 0 and row <= self._num_rows, 'row outside the table'
            for j in range(self._num_columns):
                self.underline([row, j + 1])

    def caption(self, text):
        self._caption = text

    def label(self, label):
        self._label = label

    def finalize(self):
        if self._finalized:
            raise SyntaxError('table has already been finalized once')

        lines = []
        lines += ['\\begin{table}[!' + self._location + ']']

        if self._centered:
            lines += ['\\centering']

        if self._caption:
            lines += ['\\caption{' + self._caption + '}']

        if self._label:
            lines += ['\\label{' + self._label + '}']

        if self._caption:
            lines += ['\\vspace{5pt}']

        lines += ['\\begin{tabular}']

        _alignment_text = ''
        if self._vertical_locations[0]:
            _alignment_text += '|'
        for x in range(self._num_columns):
            _alignment_text += self._alignment[x][0]
            if self._vertical_locations[x + 1]:
                _alignment_text += '|'

        lines[-1] += '{' + _alignment_text + '}'

        if self._full_horizontal_locations[0]:
            lines += ['\\toprule']

        # Add table values
        for x in range(self._num_rows):
            _line = ''

            if x > 0 and x < self._num_rows and self._full_horizontal_locations[x]:
                lines += ['\\midrule']

            for _x, _y in self._horizontal_locations[x]:
                lines += ['\\cmidrule{' + str(_x + 1) + '-' + str(_y) + '}']

            skip_next = 0
            for y in range(self._num_columns):
                if skip_next:
                    skip_next -= 1
                    continue

                braces = 0

                if not (y == 0):
                    _line += ' & '

                # Mergers
                target_merge, num_positions, alignment = self._cell_merges.get((x, y), (None, None, None))

                if target_merge == 'horizontal':
                    vert_line = '|' if self._vertical_locations[y] else ''
                    _line += '\\multicolumn{' + str(num_positions) + '}{' + alignment + vert_line + '}{'
                    skip_next = num_positions - 1
                    braces += 1

                elif target_merge == 'vertical':
                    _line += '\\multirow{' + str(num_positions) + '}{*}{'
                    braces += 1

                if [x, y] in self._underlined_values:
                    _line += '\\ul{'
                    braces += 1

                if [x, y] in self._bold_values:
                    _line += '\\textbf{'
                    braces += 1

                _line += self._values[x][y] + '}' * braces

            lines += [_line + ' \\\\']

        if self._full_horizontal_locations[self._num_rows]:
            lines += ['\\bottomrule']

        lines += ['\\end{tabular}']
        lines += ['\\end{table}']

        lines = '\n'.join(lines)
        self.text(lines)
        self._finalized = True

    def generate_tex(self, dst=None, images='png'):
        if not self._finalized:
            self.finalize()
        return super().generate_tex(dst, images)

    def compile(self, dst='./', processor='latexmk', images='png', clean=True, live=False):
        if not self._finalized:
            self.finalize()
        return super().compile(dst, processor, images, clean, live)
