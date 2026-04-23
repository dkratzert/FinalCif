
from FakePlasTeX.FakeTokenizer import Token, DEFAULT_CATEGORIES


class FakeContext(object):
    def __init__(self):
        self.context_lets = {}

    def whichCode(self, char):
        """
        Return the character code that `char` belongs to

        Required Arguments:
        char -- character to determine the code of

        Returns: integer category code of the given character

        """
        c = DEFAULT_CATEGORIES
        if char in c[Token.CC_LETTER]:
            return Token.CC_LETTER
        if char in c[Token.CC_SPACE]:
            return Token.CC_SPACE
        if char in c[Token.CC_EOL]:
            return Token.CC_EOL
        if char in c[Token.CC_BGROUP]:
            return Token.CC_BGROUP
        if char in c[Token.CC_EGROUP]:
            return Token.CC_EGROUP
        if char in c[Token.CC_ESCAPE]:
            return Token.CC_ESCAPE
        if char in c[Token.CC_SUPER]:
            return Token.CC_SUPER
        if char in c[Token.CC_SUB]:
            return Token.CC_SUB
        if char in c[Token.CC_MATHSHIFT]:
            return Token.CC_MATHSHIFT
        if char in c[Token.CC_ALIGNMENT]:
            return Token.CC_ALIGNMENT
        if char in c[Token.CC_COMMENT]:
            return Token.CC_COMMENT
        if char in c[Token.CC_ACTIVE]:
            return Token.CC_ACTIVE
        if char in c[Token.CC_PARAMETER]:
            return Token.CC_PARAMETER
        if char in c[Token.CC_IGNORED]:
            return Token.CC_IGNORED
        if char in c[Token.CC_INVALID]:
            return Token.CC_INVALID
        return Token.CC_OTHER

    def get_let(self, command):
        try:
            return self.context_lets[command]
        except KeyError:
            pass
        return command
    # def let(self, dest, source):
    #     """
    #     Create a \\let

    #     Required Arguments:
    #     dest -- the command sequence to create
    #     source -- the token to set the command sequence equivalent to

    #     Examples::
    #         c.let('bgroup', BeginGroup('{'))

    #     """
    #     pas
    #     # Use nodeName instead of macroName to work with Macros as well as
    #     # EscapeSequence, e.g. when we do
    #     # \expandafter\let\csname foo\endcsname=1
    #     if source.catcode == Token.CC_ESCAPE:
    #         self.top[dest.nodeName] = self[source.nodeName]
    #     else:
    #         self.top.lets[dest.nodeName] = source
