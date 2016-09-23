"""
curriculum-reorg-workflow.py - tools for reorganizing the protected directory and 
syncing the curriculum repository to use the new protected dir structure.

WORKFLOW

we first take some measurments of the curriclumRepo and old protectedDirs before they are
reorganized.

1 - make sure that bscs.cuuriculum_view is set "old" or None. This assures us that
we are looking at the right files.

2 - run tools.doCacheUrls(). This will calculate the unique protected urls that
are cataloged in the reorgCurriculumRepo. The urls are then written to disk one url per line

3 - run curricula.reportFormatTally(). This traverses the curriculum repository and
tallies the files that have at least one protectedUrl. The tally reports total number
of metadata files in the reorgCurriculumRepo, and then the number of files for each format. 

4 - run curricula.reportMissingAssets() to find the urls in the metadata
(i.e. the cachedUrls from step 1) that cannot be resolved to an asset. In other words,
the urls for which the asset is missing.

X - use Scanner.report to see the following:
- how many unique filenames there are
- how many duplicate names there are. 
- how many total asset files there are
- how many asset files were not cataloged in the curriculum

5 - now we're ready to do the actual update using curricula.doUpdate(). You 
should try it in test mode first, just for fun.

6 - now its time to take another snapshot. So first
	make sure bscs.cuuriculum_view is set to "new"
	
	go through steps 2 through 4.

"""
import os, sys, re, time
# from bscs.protected import *
from protected_urls import ProtectedUrls
import bscs.protected

if __name__ == '__main__':

	import curricula_reorg_tools as tools
		
	# use 'merge' until after update, then 'reorg'
	bscs.protected.curriculum_view = "reorg"
		
	unique_urls_filename = bscs.protected.curriculum_view == 'reorg' \
							and "REORG_UNIQUE_URLS.txt" \
							or "MERGE_UNIQUE_URLS.txt"
		
		
	if 0:
		# cache unique_urls
		tools.doCacheUrls(unique_urls_filename)
		
	elif 0:
		# report on cached urls
		ProtectedUrls (unique_urls_filename).report()

	elif 0: ## couldn't a bunch of these reports be run at once?
		tools.reportFormatTally()

	elif 0:
		tools.reportMissingAssets()
	
	elif 1:
		import protected_scanner as protected
		protectedDir = bscs.protected.getProtectedDir()
		protected.report(protectedDir, unique_urls_filename)
		
	elif 1:
		tools.dowrites = 0
		tools.doUpdate()
		
	else:
		print 'no ACTION specified'
		
