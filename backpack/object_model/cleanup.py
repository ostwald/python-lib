"""
clean-up - utility scripts to delete records from repository
"""

import os, sys, shutil
from bp_share import repository

curricula_dir = os.path.join (repository, 'concepts', 'curricula_bp')
units_dir = os.path.join (repository, 'concepts', 'units_bp')
chapters_dir = os.path.join (repository, 'concepts', 'chapters_bp')
topics_dir = os.path.join (repository, 'concepts', 'topics_bp')
org_config_dir = os.path.join (repository, 'ccs_org_config', 'org_config')

def clear_dir (dirname):
	for filename in os.listdir(dirname):
		os.remove(os.path.join (dirname, filename))
		
def clearTopics ():
	clear_dir (topics_dir)
	print "topics is clear"
	
def clearAll ():
	collections = [org_config_dir, curricula_dir, units_dir, chapters_dir, topics_dir]
	for dirname in collections:
		clear_dir(dirname)
	print 'all clear'
	
if __name__ == '__main__':
	clearAll()
