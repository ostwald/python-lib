<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:mods="http://www.loc.gov/mods/v3"
                xmlns="http://www.loc.gov/mods/v3"
                exclude-result-prefixes="mods">
    <xsl:output method="xml" version="1.0"  omit-xml-declaration="yes" encoding="UTF-8" indent="yes" media-type="text/xml"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="*[not(node())]"/>
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node()[normalize-space()] | @*[normalize-space()]"/>
        </xsl:copy>
    </xsl:template>


    <!--
    Name and UPD stuff - for name elements having a UPID:
    1 - make a new nameIdenfier element, e.g.,
         <nameIdentifier type="UPID">14577</nameIdentifier>
    2 - remove the following attributes from name
       - valueURI
       - authorityURI
       - authority

    NOTE: this will supercede the other selectors for name (e.g., cleanup_mods). Therefore,
    this transform can be run on OUTPUT of cleanup_mods but cannot include cleanup_mods
    -->
    <xsl:template match="/mods:mods/mods:name[@valueURI]">
        <name>
            <xsl:copy-of select="@*[name()!='valueURI' and name()!='authority' and name()!='authorityURI']"/>
            <nameIdentifier type="UPID"><xsl:value-of select="@valueURI"/></nameIdentifier>
            <xsl:apply-templates select="*" />
        </name>
    </xsl:template>

    <!--    git rid of the roleTerm[@type='code'] element-->
    <xsl:template match="/mods:mods/mods:name/mods:role/mods:roleTerm[@type='code']" />

    <!--    git rid of displayForm element-->
    <xsl:template match="/mods:mods/mods:name/mods:displayForm" />

    <!--    remove the authority="marcgt" attribute for genre-->
    <xsl:template match="/mods:mods/mods:genre[@authority='marcgt']">
        <genre>
            <xsl:copy-of select="@*[name()!='authority']"/>
            <xsl:apply-templates select="node()"/>
        </genre>
    </xsl:template>

</xsl:stylesheet>
