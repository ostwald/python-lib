from sys import platform
from os.path import join

if platform == "win32":
	sat_data_dir = "H:/Documents/Syracuse/SAT-analysis/data"
	suggestionSet_dir =  "H:/Documents/Syracuse/SAT-eval/data/suggestionSets"
else:
	sat_data_dir = "/home/ostwald/Documents/Syracuse/SAT-analysis/data"
	suggestionSet_dir =  "/home/ostwald/Documents/Syracuse/SAT-eval/data/suggestionSets"

analysis_data_dir = join (sat_data_dir, "txtFiles")
mass_analysis_data_dir = join (sat_data_dir, "MAdone_txt")
	
