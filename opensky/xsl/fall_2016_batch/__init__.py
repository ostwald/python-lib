from opensky.xsl import transform, transform_tree, ET

#
xml = '../self_xform/mods_1.xml'
xsl = 'fall_2016.xsl'

"""
run the style sheet on output of cleanup_mods
"""
cleaned = transform(xml, '../self_xform/cleanup_mods.xsl')

transformed = transform_tree (cleaned, xsl)

print(ET.tostring(transformed, pretty_print=True))
