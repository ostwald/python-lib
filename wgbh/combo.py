from rpcclient import WGBH_Client

terms = "121, 122"
jurisdiction = "NY"
grade_range = "k-12"

client = WGBH_Client()
client.verbose = 1
stds = client.lexicon_to_asn_id (jurisdiction, grade_range, terms)
tree = client.get_standards_hierarchical_json (jurisdiction, terms, grade_range)

