<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <xsl:output method="html" encoding="UTF-8"/>

    <xsl:template match="/">
        <html>
            <body>
                <p>
                    <xsl:apply-templates/>
                </p>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="w:r">
        <xsl:variable name="isBold" select="boolean(w:rPr/w:b)"/>
        <xsl:variable name="isItalic" select="boolean(w:rPr/w:i)"/>
        <xsl:variable name="isSubscript" select="boolean(w:rPr/w:vertAlign[@w:val='subscript'])"/>
        <xsl:variable name="isSuperscript" select="boolean(w:rPr/w:vertAlign[@w:val='superscript'])"/>

        <xsl:choose>
            <xsl:when test="$isSuperscript">
                <sup>
                    <xsl:call-template name="apply-formatting">
                        <xsl:with-param name="isBold" select="$isBold"/>
                        <xsl:with-param name="isItalic" select="$isItalic"/>
                        <xsl:with-param name="text" select="w:t"/>
                    </xsl:call-template>
                </sup>
            </xsl:when>
            <xsl:when test="$isSubscript">
                <sub>
                    <xsl:call-template name="apply-formatting">
                        <xsl:with-param name="isBold" select="$isBold"/>
                        <xsl:with-param name="isItalic" select="$isItalic"/>
                        <xsl:with-param name="text" select="w:t"/>
                    </xsl:call-template>
                </sub>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="apply-formatting">
                    <xsl:with-param name="isBold" select="$isBold"/>
                    <xsl:with-param name="isItalic" select="$isItalic"/>
                    <xsl:with-param name="text" select="w:t"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="apply-formatting">
        <xsl:param name="isBold"/>
        <xsl:param name="isItalic"/>
        <xsl:param name="text"/>

        <xsl:choose>
            <xsl:when test="$isBold and $isItalic">
                <b>
                    <i>
                        <xsl:apply-templates select="$text"/>
                    </i>
                </b>
            </xsl:when>
            <xsl:when test="$isBold">
                <b>
                    <xsl:apply-templates select="$text"/>
                </b>
            </xsl:when>
            <xsl:when test="$isItalic">
                <i>
                    <xsl:apply-templates select="$text"/>
                </i>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="$text"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="w:t">
        <xsl:value-of select="."/>
    </xsl:template>
</xsl:stylesheet>
