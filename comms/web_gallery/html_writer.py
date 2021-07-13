"""
Create the html pages for the images in the given directory

----- Available Metadata -------------
folder_src_path (e.g., as cataloged in ASpace)
aspace recource URL (e.g., https://aspace.archives.ucar.edu/repositories/2/archival_objects/22449)
folder_dest_path (from which we can derive the rest given the structure above)
folder title
folder description
dates?? (each image has date information. we could show the span?)

todo: investigate how to obtain metadata directly from ASpace via webservice
"""
import collections

import sys, os, re
# from UserList import UserList
from web_gallery import WebGalleryFolder
from dominate.tags import *
from dominate import document

MAX_ROWS = 3
MAX_COLS = 3

class WebGalleryHtmlWriter (WebGalleryFolder):

    def __init__ (self, src_path):
        WebGalleryFolder.__init__(self, src_path)
        self.pages = []
        current_page = None
        image_names = os.listdir(self.large_image_dir)
        image_names.sort()
        for i, img_name in enumerate(image_names):
            if current_page is None:
                current_page = WebGalleryPage(len(self.pages), self)
            wgi = WebGalleryImage(img_name, self)
            current_page.append(wgi)
            if len(current_page) == (MAX_ROWS * MAX_COLS):
                self.pages.append (current_page)
                current_page = None
            elif i == len(image_names) -1:
                self.pages.append(current_page)

    def get_pagination (self, current_page):
        t = ul(_class="pagination")
        for page in self.pages:

            if page == current_page:
                page_link = page.num
                item = li(page_link, _class="current")
            else:
                page_link = a(page.num, href=page.page_name)
                item = li(page_link)
            t += item
        prev_item, next_item = current_page.get_prev_next_nav()
        t += prev_item
        t += next_item
        return t

    def write_index_pages(self):
        """
        todo: write all index pages
        :return:
        """
        for page in self.pages:
            rendered_page = page.as_html_page()
            index_path = os.path.join (self.dst_path, page.page_name)
            fp = open(index_path, 'w')
            fp.write(str(rendered_page))
            fp.close()
            print ('wrote to',index_path)

class WebGalleryImage:

    def __init__ (self, large_image_name, writer):
        self.large_image_name = large_image_name
        self.image_name, self.large_image_suffix = os.path.splitext(large_image_name)
        self.thumb_name = self.image_name + '.jpg'

class WebGalleryPage (collections.UserList):
    """
    contains a page worth of images (number of images depend on dimensions
    defined by MAX_ROWS and MAX_COLS
    """

    def __init__ (self, index, writer):
        self.writer = writer
        self.data = []
        self.index = index
        self.num = self.index + 1
        self.page_name = self.make_page_name()

    def make_page_name (self):
        page_name = 'index'
        if self.num > 1:
            page_name += '_' + str(self.num)
        return page_name + '.html'

    def get_thumb_table (self):
        tab = table(id="thumb-table")
        for row_num in range(MAX_ROWS):
            row = tr()
            for col_num in range(MAX_COLS):
                i = row_num * MAX_COLS + col_num
                thumb_img = ''
                if i < len(self.data):
                    thumb_name = self.data[i].thumb_name
                    thumb_img = img(src='content/images/thumb/'+thumb_name)
                cell = td(thumb_img)
                row+= cell
            tab+= row
        return tab

    def get_prev_next_nav(self):

        i = self.index
        prev_link = 'Previous'
        if i > 0:
            prev_page = self.writer.pages[i-1].page_name
            prev_link = a(prev_link, href=prev_page)

        next_link = "Next"
        if i < len(self.writer.pages) - 1:
            next_page = self.writer.pages[i+1].page_name
            next_link = a(next_link, href=next_page)

        prev_item =  li(prev_link, _class="previous")
        next_item = li(next_link, _class="next")
        return prev_item, next_item

    def as_html_page (self):
        """
        this is an index page
        :return:
        """
        d = document(title=os.path.basename(writer.src_path))

        with d.head:
            link(rel='stylesheet', href='resources/css/styles.css')
            script(type='text/javascript', src='resources/js/script.js')

        # d.body+= self.get_pev_next_nav()
        wrapper = div(id='wrapper-thumb')
        d.body.add(wrapper)

        wrapper+= (self.get_thumb_table())
        wrapper+= self.writer.get_pagination (self)

        return d

    def __repr__ (self):
        s = self.page_name
        s += '\n{}'.format(list(map (lambda x:x.image_name, self.data)))
        return s

if __name__ == '__main__':
    src_path = '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc1/center_green'
    writer = WebGalleryHtmlWriter (src_path)
    if 0:
        for page in writer.pages:
            # print (page)
            # print (str(page.get_thumb_table()))
            print ("num: ", page.num)
            print ("index: ", page.index)


    writer.write_index_pages()