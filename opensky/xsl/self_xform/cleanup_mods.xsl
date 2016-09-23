<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:mods="http://www.loc.gov/mods/v3"
                xmlns="http://www.loc.gov/mods/v3"
                exclude-result-prefixes="mods">
    <xsl:output method="xml" version="1.0" omit-xml-declaration="yes" encoding="UTF-8" indent="yes" media-type="text/xml"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="*[not(node())]"/>
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node()[normalize-space()] | @*[normalize-space()]"/>
        </xsl:copy>
    </xsl:template>


    <!-- put osm namespace declaration on the root element (thus removing it from descendents) -->
    <xsl:template match="/mods:mods">
        <mods xmlns="http://www.loc.gov/mods/v3"
              xmlns:osm="http://nldr.library.ucar.edu/metadata/osm"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd"
              version="3.6">
            <xsl:apply-templates select="*"/>
        </mods>
    </xsl:template>

    <!-- give first name element usage = primary -->
    <xsl:template match="/mods:mods/mods:name[position()=1]">
        <name usage="primary" >
            <xsl:apply-templates select="@*[name()!='usage']"/>
            <xsl:apply-templates select="*"/>
        </name>
    </xsl:template>

    <!-- make sure no other name has usage attribute -->
    <xsl:template match="/mods:mods/mods:name[position()>1]">
        <name>
            <xsl:copy-of select="@*[name()!='usage']"/>
            <xsl:apply-templates select="*" />
        </name>
    </xsl:template>

</xsl:stylesheet>
