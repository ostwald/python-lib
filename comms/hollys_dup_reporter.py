import sys, os, re
from dup_manager import DupManager

accept_pat = re.compile('[a-zA-Z]{2}') #require four ajacent letters
stop_phrases = ["IMG", "CR2", 'jpg', 'tif','tiff', "JPG",]

def accept (s):
    """
    return True if this filename contains a "name" (see self.accept_pat),
    AND if that name does not contain any of the stop phrases
    :param s:
    :return:
    """
    for stop_phrase in stop_phrases:
        s = s.replace (stop_phrase, '')
    m = accept_pat.search (s)
    if not m:
        return False

    return True


def hollys_report():
    """
    IN the original de-duping, we sometimes tossed a file with a human-readable name and kept
    the dup with camera-given name.

    In this report we try to find those instances....
    """
    dup_data = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'
    print dup_data
    da = DupManager (dup_data)

    dup_map = da.dup_map
    checksums = dup_map.keys()

    for cs in checksums:
        dupset = dup_map[cs]

        has_name = False
        all_same = True
        last_filename = None

        for path in dupset:
            filename = os.path.split(path)[1]
            if "Canon EOS" in filename:
                has_name = False # we don't want to list this one
                break
            if accept (filename):
                has_name = True
            if last_filename is not None and last_filename != filename:
                all_same = False
            last_filename = filename


        if has_name and not all_same:
            print ''
            for path in dupset:
                dirname = os.path.split(path)[0]
                path_frag = dirname.replace ('/Volumes/archives/CommunicationsImageCollection/','')
                filename = os.path.split(path)[1]
                print '- {}  ({})'.format(filename, path_frag)

if __name__ == '__main__':

    hollys_report()

    if 0:
        filename = 'suzyq 349.png'

        pat = re.compile('[a-zA-Z]{4}')
        m = pat.search (filename)
        if m:
            print m.group()
        else:
            print 'NOT found'