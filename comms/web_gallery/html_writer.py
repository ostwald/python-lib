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

import sys, os, re, json
# from UserList import UserList
from web_gallery import WebGalleryFolder, get_config
from image_processor import WebGalleryImageProcessor
from dominate.tags import *
from dominate import document
from aspace_model import get_archival_object, get_person_name

MAX_ROWS = 3
MAX_COLS = 3



class WebGalleryHtmlWriter (WebGalleryImageProcessor):
    """
    extends WebGalleryImageProcessor, which provides
    - proccess_images
    - process_image, which creates access and thumbnail versions of this image

    writes the HTML for a webgallery folder

    pages are INDEX pages
    """
    def __init__ (self, src_path, archival_object=None):
        WebGalleryImageProcessor.__init__(self, src_path)
        self.pages = []
        self.archival_object = archival_object
        self.images = None

    def init_images(self):
        image_names = os.listdir(self.large_image_dir)
        image_names.sort()
        self.images = []
        current_page = None
        for i, img_name in enumerate(image_names):
            if current_page is None:
                current_page = WebGalleryIndexPage(len(self.pages), self)
            wgi = WebGalleryImage(img_name, current_page)
            self.images.append(wgi)
            current_page.append(wgi)
            if len(current_page) == (MAX_ROWS * MAX_COLS):
                self.pages.append (current_page)
                current_page = None
            elif i == len(image_names) -1:
                self.pages.append(current_page)

    def get_child (self, image_name):
        return self.archival_object.get_child(image_name)

    def get_pagination (self, current_page):
        t = ul(_class="pagination")
        for page in self.pages:

            if page == current_page:
                page_link = page.num
                item = li(page_link, _class="button current")
            else:
                page_link = a(page.num, href=page.page_name)
                item = li(page_link, _class="button")
            t += item
        prev_item, next_item = current_page.get_prev_next_nav()
        t += prev_item
        t += next_item
        return t

    def get_metadata_display (self, archival_object=None, finding_aid_uri=None):
        # print ("get_metadata_display: {}".format(self.archival_object.uri))
        # if archival_object is not None:
        #     print (" - provided: {}".format(archival_object.uri))
        CONFIG = get_config()
        if archival_object is None:
            archival_object = self.archival_object
            # print (" archival_object is: {}".format(archival_object.uri))

        # print (json.dumps (self.archival_object.data, indent=2))

        wrapper = div(_class='resource-metadata')
        series_name = 'Digital photographs, 2000-2018'
        if archival_object.level == "file":
            # href = CONFIG['aspace_base_url'] + self.archival_object.parent_uri
            if finding_aid_uri is not None:
                href = CONFIG['aspace_base_url'] + finding_aid_uri
            else:
                href = CONFIG['aspace_base_url'] + self.archival_object.uri
            # print ("  - href: " + self.archival_object.uri)
            series_aspace_link = a ("Back to Finding Aid", href=href, _class="button")
            floater = div (series_aspace_link, _class="parent-aspace-link")
            wrapper += floater
            wrapper += (div (series_name, _class="series-title"))

        # title link: ' CONFIG['aspace_base_url'] + self.archival_object.rel_path
        wrapper += div (archival_object.title, _class="resource-title")
        wrapper += div (archival_object.description, _class="resource-description")
        if archival_object.creator:
            wrapper += div ('Creator: ', get_person_name(archival_object.creator), _class="resource-creator")
        wrapper += div (archival_object.date, _class="resource-date")
        return wrapper

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

    def write_item_pages (self):
        print ('write_item_pages - {} images found'.format(len(self.images)))
        for image in self.images:
            # print ("Writing image page for ", image.image_name)
            child_object = self.get_child (image.image_name)
            # if child_object is not None:
            #     # print (json.dumps(child_object.data, indent=3))
            #     print ('   item level metadata foound')
            page_writer = WebGalleryImagePage (image, self, child_object)
            rendered_page = page_writer.as_html_page()
            image_html_path = os.path.join (self.dst_path, 'content', image.image_name+'.html')

            # print ('image_html_path:', image_html_path)
            fp = open(image_html_path, 'w')
            fp.write (str (rendered_page))
            fp.close()
            print ('wrote to', image_html_path)

class WebGalleryImage:

    def __init__ (self, large_image_name, index_page):
        """

        :param large_image_name:
        :param index_page: a WebGalleryIndexPage
        """
        self.large_image_name = large_image_name
        self.image_name, self.large_image_suffix = os.path.splitext(large_image_name)
        self.thumb_name = self.image_name + '.jpg'
        self.index_page = index_page

class WebGalleryImagePage:
    """
    image is a WebGalleryImage
    writer is a WebGalleryHtmlWriter
    """
    def __init__ (self, image, writer, archival_object):
        self.image = image
        self.writer = writer
        self.archival_object = archival_object

    def as_html_page (self):
        """
        this is an index page
        :return:
        """
        d = document(title=self.image.image_name)

        with d.head:
            link(rel='stylesheet', href='../resources/css/styles.css')
            script(type='text/javascript', src='../resources/js/script.js')

        # d.body+= self.get_pev_next_nav()
        # d.body.add (self.writer.get_metadata_display())
        #
        # d.body.add (self.get_item_navbar())

        layout = div(id='page-layout')

        finding_aid_uri = self.archival_object is not None and self.archival_object.uri or None
        layout.add (self.writer.get_metadata_display(finding_aid_uri=finding_aid_uri))
        layout.add (self.get_item_navbar())

        wrapper = div(id='wrapper-large-image')
        wrapper += img(src='images/large/'+self.image.large_image_name)

        layout.add (wrapper)

        if self.archival_object is not None:
            print (".. calling metaeata_display with {}".format(self.writer.archival_object.uri))
            layout.add (self.writer.get_metadata_display(self.archival_object))

        d.body.add(layout)

        # wrapper+= (self.get_thumb_table())

        # wrapper+= self.writer.get_pagination (self)

        return d

    def get_item_navbar(self):

        index_link = "Index"

        index_classes = "button"
        if len(self.writer.images) < 2:
            index_classes += " disabled"
        else:
            index_page_name = self.image.index_page.page_name
            index_link = a("Index", href='../' + index_page_name)

        i = self.writer.images.index(self.image)
        prev_link = 'Previous'
        prev_classes = "previous button"

        if i > 0:
            prev_image_href = self.writer.images[i-1].image_name + '.html'
            prev_link = a(prev_link, href=prev_image_href)
        else:
            prev_classes += " disabled"

        next_link = "Next"
        next_classes = "next button"
        if i < len(self.writer.images) - 1:
            next_image_href = self.writer.images[i+1].image_name + '.html'
            next_link = a(next_link, href=next_image_href)
        else:
            next_classes += " disabled"

        # index_item = li(index_link, _class=index_classes)
        # prev_item =  li(prev_link, _class=prev_classes)
        # next_item = li(next_link, _class=next_classes)

        t = ul(_class='item-navbar')
        # t += prev_item
        # t += index_item
        # t += next_item

        t += li(prev_link, _class=prev_classes)
        t += li(index_link, _class=index_classes)
        t += li(next_link, _class=next_classes)


        return t

class WebGalleryIndexPage (collections.UserList):
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
                thumb_link = ''
                if i < len(self.data):
                    wgi = self.data[i] # a WebGalleryImage
                    thumb_img = img(src='content/images/thumb/'+wgi.thumb_name)
                    image_href = 'content/'+wgi.image_name+'.html'
                    thumb_link = a(thumb_img, href=image_href)
                cell = td(thumb_link)
                row+= cell
            tab+= row
        return tab

    def get_prev_next_nav(self):

        i = self.index
        prev_link = 'Previous'
        prev_classes = "previous button"
        if i > 0:
            prev_page = self.writer.pages[i-1].page_name
            prev_link = a(prev_link, href=prev_page)
        else:
            prev_classes += " disabled"

        next_link = "Next"
        next_classes = "next button"
        if i < len(self.writer.pages) - 1:
            next_page = self.writer.pages[i+1].page_name
            next_link = a(next_link, href=next_page)
        else:
            next_classes += " disabled"

        prev_item =  li(prev_link, _class=prev_classes)
        next_item = li(next_link, _class=next_classes)
        return prev_item, next_item

    # def get_metadata_display (self):
    #     archival_object = self.writer.archival_object
    #
    #     wrapper = div(_class='file-metadata-wrapper')
    #     md_table = wrapper.add (table (_class="metadata-display-table"))
    #     md_table += tr (th ('title'), td(archival_object.title))
    #     md_table += tr (th ('description'), td(archival_object.description))
    #     md_table += tr (th ('date'), td(archival_object.date))
    #
    #     return wrapper

    def as_html_page (self):
        """
        this is an index page
        :return:
        """
        d = document(title=os.path.basename(self.writer.src_path))

        with d.head:
            link(rel='stylesheet', href='resources/css/styles.css')
            script(type='text/javascript', src='resources/js/script.js')

        # d.body+= self.get_pev_next_nav()
        page_layout = div(id="page-layout")
        d.body.add (page_layout)
        page_layout.add (self.writer.get_metadata_display())
        wrapper = div(id='wrapper-thumb')
        page_layout.add(wrapper)

        wrapper+= (self.get_thumb_table())
        wrapper+= self.writer.get_pagination (self)

        return d

    def __repr__ (self):
        s = self.page_name
        s += '\n{}'.format(list(map (lambda x:x.image_name, self.data)))
        return s

if __name__ == '__main__':
    src_path = '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc2/awards2004'
    archives_file_id = 'archival_objects/22578'
    my_archival_object = get_archival_object(archives_file_id)

    writer = WebGalleryHtmlWriter (src_path, my_archival_object)
    writer.init_images()
    if 1:
        for image in writer.images:
            print ('-',image.image_name)
            page_writer = WebGalleryImagePage (image, writer, my_archival_object)
            html_page = page_writer.as_html_page()
            # print (str(html_page))
            # break
     # writer.write_index_pages()