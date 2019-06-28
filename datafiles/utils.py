from pathlib import Path


class ParserMixin():
    """
    A Mxin class for all file parsers for data/list files.
    """

    def __init__(self, filename: str):
        self._fileobj = Path(filename)
        self.filename = self._fileobj.absolute()
