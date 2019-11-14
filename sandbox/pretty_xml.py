import os, sys
from lxml import etree as ET

def beautify (path):
    try:
        tree = ET.parse (path)
    except:
        print 'failed to parse {}: {}'.format(path, sys.exc_info()[1])
        return
    fp = open(path, 'w')
    fp.write (ET.tostring(tree, pretty_print=1))
    fp.close()
    print  'beautified file at {}'.format(path)

def beautify_dir (dir_path):
    for filename in os.listdir(dir_path):
        if not filename.endswith('.xml'):
            continue
        beautify(os.path.join (dir_path, filename))

if __name__ == '__main__':
    if 0:
        path = '/Users/ostwald/devel/opensky/pubs_to_grants/DOI-based_Testing/wos/articles_21966.xml'
        beautify(path)

    if 1:
        path = '/Users/ostwald/devel/opensky/pubs_to_grants/DOI-based_Testing/wos'
        beautify_dir(path)