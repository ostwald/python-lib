from opensky.xsl import transform, transform_tree, ET

#
xml = '../self_xform/foo.xml'
xsl = 'fall_2016.xsl'


if 0:
	"""
	run the style sheet on output of cleanup_mods
	"""
	cleaned = transform(xml, '../self_xform/cleanup_mods.xsl')

	transformed = transform_tree (cleaned, xsl)

	print(ET.tostring(transformed, pretty_print=True))


if 1:
	"""
	run the cleanup style sheet on output of fall_2016.xsl - this is PREFERRED because
	the empty stuff created by fall_2016.xsl will be cleaned up
	"""
	transformed = transform(xml, xsl)

	cleaned = transform_tree (transformed, '../self_xform/cleanup_mods.xsl')

	print(ET.tostring(cleaned, pretty_print=True))

if 0:
	"""
	fall_2016.xsl - contains its own prune - don't use cleanup
	THIS DOESNT WORK!
	"""
	transformed = transform(xml, xsl)

	print(ET.tostring(transformed, pretty_print=True))