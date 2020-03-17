import os, sys, re


def list_disk_dir (disc_num):
    path = os.path.join (base_dir, 'disc {}'.format(disc_num))

    print path

    for fn in os.listdir (path):
        print fn

class ImageRange:

    def __init__ (self, start):
        self.start = start
        self.end = None

    def __repr__ (self):
        if self.end is None:
            return self.start
        else:
            return '{}-{}'.format(self.start,self.end)

def get_num_old (filename):
    if filename[0] == '.':
        return None
    root = os.path.splitext(filename)[0]
    pat = re.compile("([0-9]+)")
    m = pat.search (root)
    if m and len(m.group(1)) > 3:
        return m.group(1)
    else:
        return None

def get_num (filename):
    if filename[0] == '.':
        return None
    root = os.path.splitext(filename)[0]
    pat = re.compile("([0-9]+)")
    m = pat.findall (root)
    m.sort (key=lambda x: -int(x))

    if m and len(m[0]) > 3:
        return m[0]
    else:
        return None

def get_file_names (path):
    names = os.listdir(path)
    return filter (lambda x:os.path.isfile(os.path.join (path, x)), names)

def list_img_spans (path):

    ranges = []
    last = None

    # file_nums = filter (None, map (get_num, os.listdir (path)))
    file_nums = filter (None, map (get_num, get_file_names(path)))
    file_nums.sort()

    # print file_nums

    for num in file_nums:
        # if len (ranges) == 0:
        #     new_range = ImageRange(num)
        #     ranges.append (new_range)
        if num == last: continue

        if last is None or int(num) != int(last) + 1:
            if len(ranges) > 0 and last is not None and last != ranges[-1].start:
                ranges[-1].end = last
            new_range = ImageRange(num)
            ranges.append (new_range)

        last = num

    if len(ranges) > 0 and last != ranges[-1].start:
        ranges[-1].end = last

    return ', '.join (map (lambda x: str(x), ranges))

INDENT = '   '

def folder_report (base_dir, level=0):

    INDENT = level*'   '

    if level == 0:
        print base_dir

    subdirs = []
    for filename in os.listdir(base_dir):
        if filename[0] == '.':
            continue

        path = os.path.join (base_dir, filename)
        if os.path.isdir(path):
            subdirs.append(path)

    print '\n{}{}'.format(INDENT, os.path.split(base_dir)[1])
    img_spans = list_img_spans (base_dir)
    if len(img_spans.strip()) > 0:
        print '{}{}'.format(INDENT,img_spans)

    for p in subdirs:
        folder_report(p, level+1)

def list_spans_from_blob(blob):
    paths = filter (None, map (lambda x:x.strip(), blob.split('\n')))
    for path in paths:
        print '\n{}'.format(path)
        print list_img_spans(path)



if __name__ == '__main__':

    # base_dir = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1'
    # from CommandLIne:
    # % p dir_lister_utils.py 6 > listings/disc_6.txt

    if len(sys.argv) > 1:
        disc_num = sys.argv[1]
    else:
        print 'disc_num required'

    if 1: # MAIN PATH
        path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc {}'.format(disc_num)
        folder_report(path)
        # for filename in os.listdir(path):
        #     path = os.path.join (foo, filename)
        #     if os.path.isdir(path):
        #         folder_report(path)
    if 0:
        blob = """/Volumes/archives/CommunicationsImageCollection/CarlyeMainDisk2/NCAR digital photos/need to be archived/SOARS-13/soars&mentors/alejandro & andy/alejandro
    /Volumes/archives/CommunicationsImageCollection/CarlyeMainDisk2/NCAR digital photos/need to be archived/SOARS-2013/alejandro & andy/alejandro
    /Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/photos/need to be archived/SOARS-13/soars&mentors/alejandro & andy/alejandro
    /Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/photos/need to be archived/SOARS-2013/alejandro & andy/alejandro"""
        list_spans_from_blob (blob)

    if 0:
        path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 17/Mesa Lab Nature Trail/'
        folder_report(path)

    if 0:
        filename = '877_7701.JPG'
        print get_num_new(filename)
