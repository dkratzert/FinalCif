#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import unittest

from cif.text import quote


class TestText(unittest.TestCase):

    def test_quote_short(self):
        q = quote('Hello this is a test for a quoted text')
        self.assertEqual("'Hello this is a test for a quoted text'", q)

    def test_quote_long(self):
        q = quote('This is a moch longer text, because I want to see what this method does with text over 80'
                  'characters wide. Let\'s add also some special characters; ?!"§$%&/()=`? Oh yeah!#++-_.,:;')
        quoted = (";\n"
                  "This is a moch longer text, because I want to see what this method does with text over 80\n"
                  "characters wide. Let's add also some special characters; ?!\"§$%&/()=`? Oh yeah!#++-_.,:;\n"
                  ";")
        self.assertEqual(quoted, q)