import os, sys, shutil

WOS_metadata = "H:/python-lib/ncar_lib/citations/WOS_metadata"
dest_dir = "H:/python-lib/ncar_lib/citations/WOS"

if not os.path.exists(dest_dir):
	os.mkdir (dest_dir)

for dirname in os.listdir (WOS_metadata):

	wos_dir = os.path.join (WOS_metadata, dirname)
	metadata_files = os.listdir (wos_dir)
	print "%s (%d)" % (dirname, len (metadata_files))

	for filename in metadata_files:
		src = os.path.join (wos_dir, filename)
		dst = os.path.join (dest_dir, filename)
		# print dst
		shutil.copyfile (src, dst)
