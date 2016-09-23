README

How are the reports generated?

1 - search the 'osgc' collection for 'Done' records in the FY10
 - fy10 - search from FY >= 2009 and FY < 10/1/10
 
2 - go through the hits and characterize the strength of match as follows

a best matching author is determined. this is generally the author with the same last name. if there
are more than one matching author we choose one (based on??)

we compare the best matching author with the target author to determine strength of match

- upid match 
	note: if matching author has different upid than target, this hit is discarded
	e.g., if our target is Smith (1234) and the best matching author from the pub is Smith (4567),
		  this pub is discared (it's strength is 0)
- name match
- lastname_only match

