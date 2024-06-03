<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
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
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="w:t">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="w:rPr/w:i">
        <i>
            <xsl:apply-templates select="../following-sibling::w:t"/>
        </i>
    </xsl:template>

    <xsl:template match="w:rPr/w:vertAlign[@w:val='subscript']">
        <sub>
            <xsl:apply-templates select="../following-sibling::w:t"/>
        </sub>
    </xsl:template>

    <xsl:template match="w:rPr/w:vertAlign[@w:val='superscript']">
        <sup>
            <xsl:apply-templates select="../following-sibling::w:t"/>
        </sup>
    </xsl:template>
</xsl:stylesheet>
