class SymmetryElement():
    symm_ID = 1
    __slots__ = ['centric', 'symms', 'ID', 'matrix', 'trans']

    def __init__(self, symms):
        self.symms = symms
        self.ID = SymmetryElement.symm_ID
        SymmetryElement.symm_ID += 1
        lines = []
        trans = []
        for symm in self.symms:
            line, t = self._parse_line(symm)
            lines.append(line)
            trans.append(t)
        self.trans = trans
        self.matrix = lines

    def _parse_line(self, symm):
        symm = symm.upper().replace(' ', '')
        chars = ['X', 'Y', 'Z']
        line = []
        for char in chars:
            element, symm = self._partition(symm, char)
            line.append(element)
        if symm:
            trans = self._float(symm)
        else:
            trans = 0
        return line, trans

    def _float(self, string):
        try:
            return float(string)
        except ValueError:
            if '/' in string:
                string = string.replace('/', './') + '.'
                return eval('{}'.format(string))

    def _partition(self, symm, char):
        parts = symm.partition(char)
        if parts[1]:
            if parts[0]:
                sign = parts[0][-1]
            else:
                sign = '+'
            if sign == '-':
                return -1, ''.join((parts[0][:-1], parts[2]))
            else:
                return 1, ''.join((parts[0], parts[2])).replace('+', '')
        else:
            return 0, symm

    def translate(self, ort_code: str) -> None:
        tr = ort_code.split('_')[-1]
        for n, x in enumerate(tr):
            t = int(x) - 5
            self.trans[n] += t

    def toShelxl(self) -> str:
        """
        Generate and return string representation of Symmetry Operation in Shelxl syntax.
        """
        axes = ['X', 'Y', 'Z']
        lines = []
        for i in range(3):
            text = str(round(self.trans[i], 5)) if self.trans[i] else ''
            for j in range(3):
                s = '' if not self.matrix[i][j] else axes[j]
                if self.matrix[i][j] < 0:
                    s = '-' + s
                elif s:
                    s = '+' + s
                text += s
            lines.append(text)
        return ', '.join(lines)
