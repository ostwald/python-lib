"""
convert webcat record into library_dc record
"""
import os, sys
from ncar_lib.lib.globals import *

# ids of records that do not have issues embedded in their titles (but fool the program into thinking they do)
issueTitleSkipList = [
        "TECH-NOTE-000-000-000-100",
        "TECH-NOTE-000-000-000-101",
        "TECH-NOTE-000-000-000-102",
        "TECH-NOTE-000-000-000-188",
        "TECH-NOTE-000-000-000-491",
        "TECH-NOTE-000-000-000-492",
        "TECH-NOTE-000-000-000-493",
        "TECH-NOTE-000-000-000-498",
        "TECH-NOTE-000-000-000-559",
]


# ids that we don't want to touch for splitting into issue / title
title_skip_list = [

]

