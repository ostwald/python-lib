identityMapping = "European Centre for Medium Range Weather Forecasts"

nullMapping = """value: Altschuler, Bruce R.
map to: null"""

simpleMapping = """Fremont, CA : Nielsen Norman Group
map to: instName: Nielsen Norman Group"""

regularMapping = """High Altitude Observatory
map to: instName: National Center for Atmospheric Research (NCAR)
                instDiv: High Altitude Observatory (HAO)"""

multiMapping = """value: Climate and Global Dynamics Division
value: Climate and Global Dynamics Division.
value: Climate And Global Dynamics Division.
value: Climate And Global Dynamics Division
map to:         instName: National Center for Atmospheric Research (NCAR)
                instDiv: Climate And Global Dynamics Division (CGD)"""
				
toughOne = """value: Research Aviation Facility. Earth Observing Laboratory.
map to: 	instName: National Center for Atmospheric Research (NCAR)
		instDiv: Research Aviation Facility (RAF)
		instName: National Center for Atmospheric Research (NCAR)
		instDiv: Earth Observing Laboratory (EOL)"""
				
allMappings = [
	"identityMapping", 
	"nullMapping",
	"simpleMapping", 
	"regularMapping",
	"multiMapping",
	"toughOne"
	]


