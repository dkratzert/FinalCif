<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <xsl:output method="html" encoding="UTF-8"/>

    <xsl:template match="/">
        <html>
            <xsl:apply-templates/>
        </html>
    </xsl:template>

    <xsl:template match="w:r">
        <xsl:choose>
            <xsl:when test="w:rPr/w:i">
                <i>
                    <xsl:apply-templates select="w:t"/>
                </i>
            </xsl:when>
            <xsl:when test="w:rPr/w:vertAlign[@w:val='subscript']">
                <sub>
                    <xsl:apply-templates select="w:t"/>
                </sub>
            </xsl:when>
            <xsl:when test="w:rPr/w:vertAlign[@w:val='superscript']">
                <sup>
                    <xsl:apply-templates select="w:t"/>
                </sup>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="w:t">
        <xsl:value-of select="."/>
    </xsl:template>

</xsl:stylesheet>
