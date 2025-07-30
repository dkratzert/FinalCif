#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os

os.environ['RUNNING_TEST'] = 'True'
import unittest

import gemmi
from qtpy import QtWidgets
from packaging.version import Version

# noinspection PyUnresolvedReferences
from finalcif.appwindow import app
from finalcif.cif.text import quote, utf8_to_str, retranslate_delimiter, delimit_string, characters, string_to_utf8
from finalcif.gui.custom_classes import MyCifTable
from finalcif.report.report_text import gstr


class TestText(unittest.TestCase):

    def setUp(self) -> None:
        d = gemmi.cif.Document()
        self.block: gemmi.cif.Block = d.add_new_block('new-block')

    def test_quote_short(self):
        q = quote('Hello this is a test for a quoted text')
        self.assertEqual("'Hello this is a test for a quoted text'", q)

    def test_quote_quotation_mark(self):
        q = quote("Jesus' live")
        self.assertEqual('"Jesus\' live"', q)

    def test_quote_long(self):
        q = quote('This is a moch longer text, because I want to see what this method does with text over 80 '
                  'characters wide. Let\'s add also some special characters; ?!"§$%&/()=`? Oh yeah!#++-_.,:;')
        quoted = (";This is a moch longer text, because I want to see what this method does with \n"
                  "text over 80 characters wide. Let's add also some special characters; \n"
                  "?!\"§$%&/()=`? Oh yeah!#++-_.,:;\n"
                  ";")
        self.assertEqual(quoted, q)

    def test_set_pair_delimited_empty(self):
        self.block.set_pair('_foobar', delimit_string(''))
        if Version(gemmi.__version__) >= Version('0.5.7'):
            self.assertEqual(('_foobar', ''), self.block.find_pair('_foobar'))
        else:
            self.assertEqual(['_foobar', ''], self.block.find_pair('_foobar'))

    def test_set_pair_delimited_question(self):
        self.block.set_pair('_foobar', delimit_string('?'))
        if Version(gemmi.__version__) >= Version('0.5.7'):
            self.assertEqual(('_foobar', '?'), self.block.find_pair('_foobar'))
        else:
            self.assertEqual(['_foobar', '?'], self.block.find_pair('_foobar'))

    def test_set_pair_delimited_number(self):
        self.block.set_pair('_foobar', delimit_string('1.123'))
        if Version(gemmi.__version__) >= Version('0.5.7'):
            self.assertEqual(('_foobar', '1.123'), self.block.find_pair('_foobar'))
        else:
            self.assertEqual(['_foobar', '1.123'], self.block.find_pair('_foobar'))

    def test_set_pair_delimited_with_newline(self):
        self.block.set_pair('_foobar', delimit_string('abc\ndef foo'))
        if Version(gemmi.__version__) >= Version('0.5.7'):
            self.assertEqual(('_foobar', 'abc\ndef foo'), self.block.find_pair('_foobar'))
        else:
            self.assertEqual(['_foobar', 'abc\ndef foo'], self.block.find_pair('_foobar'))

    def test_delimit_ut8_to_cif_str(self):
        s = utf8_to_str('100 °C')
        self.assertEqual(r'100 \%C', s)

    def test_cif_str_to_utf8(self):
        r = retranslate_delimiter(r'100 \%C')
        self.assertEqual('100 °C', r)

    def test_retranslate_sentence(self):
        r = retranslate_delimiter(r"Crystals were grown from thf at -20 \%C.")
        self.assertEqual('Crystals were grown from thf at -20 °C.', r)

    def test_delimit_umlaut(self):
        self.assertEqual(r'\"a\"o\"u\,c', delimit_string('äöüç'))

    def test__backwards_delimit_umlaut(self):
        self.assertEqual('ä ö ü ç', retranslate_delimiter(r'\"a \"o \"u \,c'))

    def test_retranslate_all(self):
        for char in characters:
            if char in ('Å', 'Å'):
                continue
            self.assertEqual(char, retranslate_delimiter(delimit_string(char)))

    def test_translate_wrong_cif_umlauts(self):
        self.assertEqual('ä ö ü', string_to_utf8(r'\"a \"o \"u'))

    def test_translate_wrong_cif_umlauts_next_to_each_other(self):
        self.assertEqual(r'äöü', string_to_utf8(r'\"a\"o\"u'))


class TestHeavyUtf8(unittest.TestCase):
    def setUp(self) -> None:
        # We have an utf-8 string with characters that CIF does not know:
        self.txt = "∮ E⋅da = Q,  n → ∞, ∑ f(i) = ∏ g(i), ∀x∈ℝ: ⌈x⌉ = −⌊−x⌋, α ∧ ¬β = ¬(¬α ∨ β), " \
                   "ℕ ⊆ ℕ₀ ⊂ ℤ ⊂ ℚ ⊂ ℝ ⊂ ℂ, ⊥ < a ≠ b ≡ c ≤ d ≪ ⊤ ⇒ (A ⇔ B), " \
                   "2H₂ + O₂ ⇌ 2H₂O, R = 4.7 kΩ, ⌀ 200 mm"
        # The expected result is a mix of CIF and html entities:
        self.quoted = r"&#8750; E&#8901;da = Q,  n \\rightarrow \\infty, &#8721; f(i) = &#8719; g(i), " \
                      r"&#8704;x&#8712;&#8477;: &#8968;x&#8969; = &#8722;&#8970;&#8722;x&#8971;, \a " \
                      r"&#8743; &#172;\b = &#172;(&#172;\a &#8744; \b), " \
                      r"&#8469; &#8838; &#8469;&#8320; &#8834; &#8484; &#8834; &#8474; &#8834; &#8477; " \
                      r"&#8834; &#8450;, &#8869; < a \\neq b &#8801; c &#8804; d &#8810; &#8868; &#8658; " \
                      r"(A &#8660; B), " \
                      r"2H~2~ + O~2~ &#8652; 2H~2~O, R = 4.7 k\W, &#8960; 200 mm"

    def test_encode_heavy_utf8(self):
        # Test for the quoted string
        self.assertEqual(self.quoted, utf8_to_str(self.txt))

    def test_encode_and_decode_utf8(self):
        # Test for quote and immediate decode to utf-8 again:
        self.assertEqual(self.txt, retranslate_delimiter(utf8_to_str(self.txt)))


class TestLongTextinField(unittest.TestCase):
    def setUp(self):
        os.environ["RUNNING_TEST"] = 'True'
        self.w = QtWidgets.QMainWindow()
        self.table = MyCifTable()
        self.w.setCentralWidget(self.table)
        self.table.vheaderitems.append('_foo')
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        self.table.setMinimumHeight(200)
        self.table.horizontalHeader().setDefaultSectionSize(200)
        self.w.show()

    def tearDown(self) -> None:
        self.w.close()
        self.table.close()
        app.quit()

    def test_long_text_in_texedit_and_gstr(self):
        txt = ('This is a much longer text, because I want to see what this method does with text '
               'over 80 characters wide. Let\'s add also some special characters; '
               '?!"§$%&/()=`? Oh yeah!#+±_.,:;')
        self.table.setText(key='_foo', row=0, column=2, txt=txt)
        # app.exec()
        self.assertEqual(('This is a much longer text, because I want to see what this method does with '
                          "text over 80 characters wide. Let's add also some special characters; "
                          '?!"§$%&/()=`? Oh yeah!#+±_.,:;'), gstr(self.table.getText(row=0, col=2)))
