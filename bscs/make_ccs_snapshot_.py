"""
Automatic Snapshots - CCS prod

each day we make a snapshot and save it in the daily dir
if it is the first day of the month we save it in the monthly dir

Save last four dailies - in daily directory
Save last four months - in monthly directory

Snapshot components: userContent, curriculum and docRoot
approximate sizes (zipped)
- userContent - .5G
- docRoot - 2G
- curriculum - 2M

- total ~3G - so backups will take ~24G total when daily and monthly are full
"""
import os, sys, time,shutil, tempfile
import tarfile

base = '/users/Home/ostwald/tmp'

snapshots_home = os.path.join (base, 'snapshots')
daily_dir = os.path.join (snapshots_home, 'daily')
monthly_dir = os.path.join (snapshots_home, 'monthly')

# Snapshot components
userContent_path = os.path.join (base, 'file_uploads')
# docRoot_path = os.path.join (base, 'protected-bscs') # a larger directory
docRoot_path = os.path.join (base, 'rs1')
curriculum_path = os.path.join (base, 'icons')


def makeSnapshot ():
	"""
	Make a tarball named for the date (2014-05-25.tgz). 
	
	When uncompressed the result is a directory named for the date (2014-05-25)
	containing the three component directories (userContentRpo, curriculumRepo,
	docRoot)
	"""
	tics = time.time()
	today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
	print '\nmakeSnapshot - %s' % today
	
	# cp the data (uncompressed) into a tmp directory
	tmp_dir = os.path.join (tempfile.gettempdir(), today)
	os.mkdir (tmp_dir)
	for path in [userContent_path, docRoot_path, curriculum_path]:
		shutil.copytree(path, os.path.join(tmp_dir, os.path.basename(path)))
		
	# make a tarball of compressed data in daily directory
	if not os.path.exists(daily_dir):
		os.mkdir (daily_dir)
	tarfile_path = os.path.join (daily_dir, today + '.tar.gz')
	tar = tarfile.open(tarfile_path, "w:gz")
	tar.add (tmp_dir, arcname=os.path.basename(today))
	tar.close()
	print 'wrote tarball to %s' % tarfile_path
	shutil.rmtree(tmp_dir)
	
	cleanup (daily_dir)
	
	# if this is first day of month make monthly backup
	dayNum =  time.strftime('%d', time.localtime(time.time()))
	if dayNum == '27': 
		# copy tarball to monthly_dir
		if not os.path.exists(monthly_dir):
			os.mkdir (monthly_dir)
		shutil.copy (tarfile_path, monthly_dir)
		cleanup (monthly_dir)
		pass
		
	
	print '... elapsed seconds: %d' % (time.time() - tics)
	
def cleanup (dirname):
	"""
	keep only the most recent 4 snapshots in both the daily and weekly dirs
	"""
	files_to_keep = 4
	print 'cleanup: ' + dirname
	filenames = os.listdir(dirname)
	filenames.sort()
		
	files_to_delete = len(filenames) - files_to_keep
	if files_to_delete > 0:
		for f in filenames[:files_to_delete]:
			print '- remove', f
			try:
				os.remove(os.path.join (dirname, f))
			except Exception, msg:
				print 'WARN: unable to delete %s: %s' % (os.path.join (dirname, f), msg)
				
	
	
if __name__ == '__main__':
	print '\n'
	makeSnapshot()
	# cleanup('fo')
