"""
SMall Images

collect from database and write to json
read from json into SparseTree class

all we need are paths, one per line (right?

"""
import sys, os
from UserDict import UserDict
from comms import CommsDBTable
from comms import globals
from HyperText.HTML40 import *
from html import HtmlDocument

counter_path = "/Users/ostwald/tmp/counter.txt"


def init_counter ():
    fp = open(counter_path, 'w')
    fp.write ('0')
    fp.close()

def bump_counter ():
    count = int(open(counter_path,'r').read())
    count += 1
    fp = open(counter_path, 'w')
    fp.write (str(count))
    fp.close()


class Node:

    file_system_root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/'

    def __init__ (self, path):
        self.path = path
        self.relative_path = self.path.replace(self.file_system_root, '')
        self.level = len(self.path.replace(self.file_system_root,'').split('/'))
        self.name = os.path.basename(path)

    def as_html (self):
        wrapper = DIV(self.name)

class Leaf(Node):

    def __init__ (self, path):
        Node.__init__(self, path)
        self.node_type = 'LEAF'

    def as_html (self):
        wrapper = DIV(self.name, klass='leaf')
        bump_counter()
        return wrapper

class Branch (Node):

    def __init__ (self, path, db):
        self.children = []
        self._recursive_file_count = None
        Node.__init__(self, path)
        self.db = db
        self.node_type = 'BRANCH'

        for child in db.list_dir(self.path):
            child_path = os.path.join (self.path, child)
            if self.db.count_selected("WHERE path = '{}'".format(child_path)) > 0:
                self.children.append(Leaf (child_path))
            else:
                self.children.append(Branch (child_path, self.db))

    def get_recursive_file_count (self):
        if self._recursive_file_count is None:
            self._recursive_file_count = len(self.get_items())
            for sub in self.get_sub_branches():
                self._recursive_file_count += sub.get_recursive_file_count()
        return self._recursive_file_count

    def add_child (self, path):
        self.children.append(node)

    def get_items (self):
        return filter (lambda x:isinstance(x, Leaf), self.children)

    def get_sub_branches(self):
        return filter (lambda x:isinstance(x, Branch), self.children)

    def __repr__(selfs):
        s = 'Branch: {}'.format(self.path)
        s += '\n- {} children'.format(len(self.children))
        for child in self.children:
            print '  -', child.name
        return  s

    def as_html (self, max_levels=100):
        level_str = 'level{}'.format(self.level)
        wrapper = DIV (klass='branch ' +  level_str.format(self.level))
        # header = DIV ('{} ({})'.format(self.name, self.level), klass="header")

        name = DIV(self.name, klass="label", title=self.relative_path)
        count = DIV(self.get_recursive_file_count(), klass="count")

        # label_str = "{} ({})".format(self.name, self.get_recursive_file_count())
        label = DIV(name, count, klass="foolabel", title=self.relative_path)

        header = DIV (label, klass="header")
        body = DIV (klass="body " + level_str)

        for item in self.get_items():
            body.append (item.as_html())

        # subs = self.get_sub_branches()
        # for sub in subs:
        #     print sub.__class__

        if self.level < max_levels:
            for subbranch in self.get_sub_branches():
                body.append(subbranch.as_html(max_levels))

        wrapper.append(header)
        wrapper.append(body)
        return wrapper

class HtmlWriter:

    def __init__(self, root_directory, sqlite_path):
        self.root = root_directory
        self.db = CommsDBTable(sqlite_path)
        self.title = "Small Images"

    def get_top_nodes (self):
        top_nodes = []
        for filename in self.db.list_dir(self.root):
            # print filename
            if filename.startswith('disc'):
                top_nodes.append (os.path.join (file_system_root, filename))

        def key_fn (path):
            name = os.path.basename(path)
            index = name.split(' ')[1]
            try:
                return int(index)
            except:
                # print 'warn: could not handle "{}"'.format(path)
                return 134

        # top_nodes.sort(lambda x:int(os.path.basename(x).split(' ')[1]))
        top_nodes.sort(key=key_fn)
        return top_nodes

    def render_tree (self):
        max_node_count = 300
        max_node_depth = 30
        top_nodes = self.get_top_nodes()
        print '{} top_nodes'.format(len(top_nodes))
        tree = UL(klass='root-node')
        for path in top_nodes[:min(len(top_nodes),max_node_count)]:
            base_path = path
            branch = Branch (base_path, self.db)
            tree.append(LI (branch.as_html(max_node_depth)))
        return tree


    def as_html(self):
        doc = HtmlDocument (title=self.title, stylesheet="styles.css")
        # doc.body["onload"] = "init();"

        # <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

        doc.head.append (META(http_equiv="Content-Type",
                              content="text/html; charset=utf-8"))

        doc.addJavascript ("https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js")
        doc.addJavascript ("https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js")
        doc.addJavascript ("script.js")

        doc.append (self.render_tree())
        return doc

    def write_html (self, outpath="html/SMALL_IMAGE.html"):
        fp = open(outpath, 'w')
        fp.write (self.as_html().__str__())
        fp.close()
        print 'wrote ', outpath

if __name__ == '__main__':
    sqlite_path = '/Users/ostwald/Documents/Comms/Small_Images/PC_Disk_Small_Images.sqlite'
    file_system_root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1'
    init_counter()
    writer = HtmlWriter(file_system_root, sqlite_path)
    # for path in writer.get_top_nodes():
    #     print path
    writer.write_html()



