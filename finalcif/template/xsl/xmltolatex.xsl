<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <xsl:output method="text" encoding="UTF-8"/>

    <!-- root simply spits out its children -->
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <!-- paragraphs → blank lines -->
    <xsl:template match="w:p">
        <xsl:apply-templates/>
        <xsl:text>&#10;&#10;</xsl:text>
    </xsl:template>

    <!-- runs with formatting flags -->
    <xsl:template match="w:r">
        <xsl:variable name="b" select="boolean(w:rPr/w:b)"/>
        <xsl:variable name="i" select="boolean(w:rPr/w:i)"/>
        <xsl:variable name="sub" select="boolean(w:rPr/w:vertAlign[@w:val='subscript'])"/>
        <xsl:variable name="sup" select="boolean(w:rPr/w:vertAlign[@w:val='superscript'])"/>

        <xsl:choose>
            <xsl:when test="$sup">
                <xsl:text>$^{</xsl:text>
                <xsl:call-template name="fmt">
                    <xsl:with-param name="txt" select="w:t"/>
                    <xsl:with-param name="b" select="$b"/>
                    <xsl:with-param name="i" select="$i"/>
                </xsl:call-template>
                <xsl:text>}$</xsl:text>
            </xsl:when>
            <xsl:when test="$sub">
                <xsl:text>$_{</xsl:text>
                <xsl:call-template name="fmt">
                    <xsl:with-param name="txt" select="w:t"/>
                    <xsl:with-param name="b" select="$b"/>
                    <xsl:with-param name="i" select="$i"/>
                </xsl:call-template>
                <xsl:text>}$</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="fmt">
                    <xsl:with-param name="txt" select="w:t"/>
                    <xsl:with-param name="b" select="$b"/>
                    <xsl:with-param name="i" select="$i"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- nested bold/italic -->
    <xsl:template name="fmt">
        <xsl:param name="txt"/>
        <xsl:param name="b" select="false()"/>
        <xsl:param name="i" select="false()"/>
        <xsl:choose>
            <xsl:when test="$b and $i">
                <xsl:text>\textbf{\textit{</xsl:text>
                <xsl:apply-templates select="$txt"/>
                <xsl:text>}}</xsl:text>
            </xsl:when>
            <xsl:when test="$b">
                <xsl:text>\textbf{</xsl:text>
                <xsl:apply-templates select="$txt"/>
                <xsl:text>}</xsl:text>
            </xsl:when>
            <xsl:when test="$i">
                <xsl:text>\textit{</xsl:text>
                <xsl:apply-templates select="$txt"/>
                <xsl:text>}</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="$txt"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- raw text (escape LaTeX specials here if needed) -->
    <xsl:template match="w:t">
        <xsl:value-of select="."/>
    </xsl:template>

</xsl:stylesheet>
