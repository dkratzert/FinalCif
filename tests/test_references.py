from finalcif.report.references import Nosphera2Reference, SAINTReference


def test_nosphera2reference():
    assert str(Nosphera2Reference()) == (
        "F. Kleemiss, O. V. Dolomanov, M. Bodensteiner, N. Peyerimhoff, L. Midgley, L. J. Bourhis, A. Genoni, "
        "L. A. Malaspina, D. Jayatilaka, J. L. Spencer, F. White, B. Grundkotter-Stock, S. Steinhauer, "
        "D. Lentz, H. Puschmann, S. Grabowsky, Chem. Sci. 2021, 12, 1675–1692, doi:10.1039/D0SC05526C.")


def test_saint_reference():
    assert str(SAINTReference('SAINT', 'V7.68a')) == "Bruker, SAINT, V7.68a, Bruker AXS SE, Karlsruhe, Germany."
