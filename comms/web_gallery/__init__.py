"""
This module depends on python 3.9.x
"""
import os, sys, re
import shutil

SRC_PATH_BASE = '/Volumes/cic-de-duped/CIC-ExternalDisk1'
DST_PATH_BASE = '/Users/ostwald/tmp/COMMS_DEST'

class WebGalleryFolder:
    """
        ------- Directory structure --------:

        content
        - images
        -- thumb
        -- large
        - photo1_large.html
        - photo2_large.html
        - photoN_large.html

        resources (note: these could be shared among the webGalleries ...)
        - css
        - js
        - misc

        index.html
        index_2.html
        index_n.html
    """
    def __init__ (self, src_path):
        """
        initialize the directory structure
        - dst_path
            - content
                - images
                    - large_images
                    - thumbnails
                <large_image html pages>
            <index html pages>
            - resources
                - css
                - js
        :param src_path:
        """
        self.src_path = src_path
        self.images_dir = self.large_image_dir = self.thumb_image_dir = None
        self.dst_path = self.src_path.replace (SRC_PATH_BASE, DST_PATH_BASE)
        self.init_file_structure()

    def init_file_structure (self):
        if not os.path.exists(DST_PATH_BASE):
            raise Exception ('DST_PATH_BASE does not exist at', DST_PATH_BASE)

        # print ('DEST:', self.dst_path)
        if not os.path.exists (self.dst_path):
            os.makedirs (self.dst_path)

        # prepare directory folders
        self.content_dir = os.path.join (self.dst_path, 'content')
        if not os.path.exists (self.content_dir):
            os.mkdir (self.content_dir)

        self.images_dir = os.path.join (self.content_dir, 'images')
        if not os.path.exists (self.images_dir):
            os.mkdir (self.images_dir)

        self.large_image_dir = os.path.join (self.images_dir, 'large')
        if not os.path.exists (self.large_image_dir):
            os.mkdir (self.large_image_dir)

        self.thumb_image_dir = os.path.join (self.images_dir, 'thumb')
        if not os.path.exists (self.thumb_image_dir):
            os.mkdir (self.thumb_image_dir)

        # resources
        self.resources_dir = os.path.join (self.dst_path, 'resources')
        if os.path.exists (self.resources_dir):
            shutil.rmtree(self.resources_dir)
        shutil.copytree('resources', self.resources_dir)