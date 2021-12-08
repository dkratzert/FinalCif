#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from contextlib import suppress
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED


class ArchiveReport():
    def __init__(self, filename):
        self.zipfile = filename
        level = ZIP_STORED
        with suppress(Exception):
            level = ZIP_DEFLATED
        self.zip = ZipFile(file=self.zipfile, mode='w', compression=level)


if __name__ == '__main__':
    z = ArchiveReport('./test.zip')
    z.zip.write('test-data/report_DK_zucker2_0m-finalcif.docx')
    z.zip.close()
