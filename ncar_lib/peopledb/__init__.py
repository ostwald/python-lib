"""
Some PeopleDB calls (API: https://wiki.ucar.edu/display/weg/People+REST+API)

Organizations
ORGS PROPERTIES -
# orgId: 54
# acronym: "MMM"
# name: "Mesoscale and Microscale Meteorology Division"
# level: "Division / Section"
# levelCode: 700
# parentOrg: "NESL"

REQUESTS
* Get Organization Detail
doc - https://wiki.ucar.edu/display/weg/Get+Organization+Detail
ex - https://api.ucar.edu/people/orgs/<org id or org acronym>

returns org properties, people and subOrgs

* Get Organization Hierarchy
doc - https://wiki.ucar.edu/display/weg/Get+Organization+Hierarchy
e.g., https://api.ucar.edu/people/orgHierarchy?org=<Org Id or Org Acronym>

returns a list of parent orgs (that can be sorted by levelCode to get hierarchy??)
Q: how does this hierarchy agree with our instDiv vocab??

* Get Sub Organizations
doc - https://wiki.ucar.edu/display/weg/Get+Sub+Organizations
ex - https://api.ucar.edu/people/subOrgs?org=MMM

returns list of CHILDREN for given org (for MMM these all have same levelCode, but this may not always be the case)

* Search Organizations
doc - https://wiki.ucar.edu/display/weg/Search+Organizations
ex - https://api.ucar.edu/people/orgs?name=Education

search by acronym, level, name
"""

from internalPerson import InternalPerson
from searchInternalPerson import InternalPersonSearch, peopleDB_1, peopleDB_2
from getInstDivision import getInstDivisionVocab
from searchInternalPerson import InternalPersonSearch
