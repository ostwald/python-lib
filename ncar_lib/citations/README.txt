Big Picture

We have a few data sources, including PubsDB and WOS. First, figure out how to
pull info from these sources, with an eye toward unifying "schema".

Then define a class "Citation" and the methods to cast info from different data
sources into Citation objects.

Then, implement CitationXmlRecord so that we can create xml that will go into
DCS.

Current Status

PubsDB - able to read info from Pubs tables and "flesh" a publication record,
even through there is not python class defined for publication. See
"fleshRecord" - this can be converted into constructor ...

WOS - need to read records from WOS into fields that are "close" to those
required for Citation.


citataion record schema: http://nldr.library.ucar.edu/metadata/citation/0.1/citation.xsd