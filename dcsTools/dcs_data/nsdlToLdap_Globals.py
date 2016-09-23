# nsdlToLdap_Globals

import re

DCS_DATA_DIR = "/home/ostwald/Documents/NSDL/TransitionToLdap/Data_Manipulation/dcs_data"

datePat = re.compile ("[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}Z");

TEST_DATA_DIR = "test_collection"

from DcsDataRecord_v1 import DcsDataRecord_v1
DcsDataRecord = DcsDataRecord_v1
del DcsDataRecord_v1

# print "Globals executed"

USERNAME_XLS = "/home/ostwald/Documents/NSDL/TransitionToLdap/Data_Manipulation/MgrVsLdap.txt"
USER_DATA_DIR = "/home/ostwald/Documents/NSDL/TransitionToLdap/Data_Manipulation/users"
