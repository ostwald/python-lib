"""
Convert images to the accessibility format (TIF, x pixels on a side),
and produce thumbnails
"""
import traceback

import sys, os, re
import rawpy
from PIL import Image

from web_gallery import WebGalleryFolder, get_config

RAW_EXTENSIONS = ['.CR2', '.CRW']
LARGE_IMAGE_SIZE = (1200, 1200)
THUMB_IMAGE_SIZE = (500, 500)

def raw_to_tiff (path):
    """
    returns an rgb object, which is basically a tiff (technically a post-processed rawpy image).
    - it can be written to disk as a tiff (this is the default) using imageio.imsave(dest, rgb)
    - it can be read by PIL/Image using im = Image.fromarray(rgb)
    :param path: pate to a raw file
    :return: an rgb object
    """
    raw = rawpy.imread(path)
    rgb = raw.postprocess()
    return rgb

def get_image (path):
    """
    return an Image instance
    :param path:
    :return: an Image instance
    """
    root, ext = os.path.splitext(os.path.basename (path))
    # print (root,'   ', ext)
    if ext in RAW_EXTENSIONS:
        print ('processing raw: {}'.format(os.path.basename(path)))
        rgb = raw_to_tiff (path)
        im = Image.fromarray(rgb)
    else:
        im = Image.open(path)
    return im

class ImageProcessingError (Exception):
    pass

class WebGalleryImageProcessor (WebGalleryFolder):
    """
    how to pass in metadata?
    """
    def __init__ (self, src_path):
        WebGalleryFolder.__init__(self, src_path)

    def process_images(self, safe=False):
        """
        consider a safe mode, where existing files would not be overriden
        :return:
        """
        img_names = os.listdir(self.src_path)
        for i, img_name in enumerate(img_names):
            img_path = os.path.join (self.src_path, img_name)
            # print ("img_path:", img_path)
            if img_name[0] == '.' or img_name in ['Thumbs.db']:
                continue
            try:
                # print ('- {}/{} - processing {}'.format(i, len(img_names), img_name))
                self.process_image (img_path, safe)
            except ImageProcessingError:
                print ("ImageProcessingError for {}: {}".format(img_path, sys.exc_info()[1]))


    def process_image (self, image_path, safe=False):
        """

        :param image_path:
        :param safe: if safes we won't reprocess image
        :return:
        """
        root, ext = os.path.splitext(os.path.basename (image_path))
        tiff_image_path = os.path.join (self.tiff_image_dir, root+'.tiff')
        large_image_path = os.path.join (self.large_image_dir, root+'.jpg')
        if safe and os.path.exists(large_image_path):
            # print ('  -  skipped {}'.format(os.path.basename(image_path)))
            return

        try:
            image = get_image(image_path)
            # process the image at path
            tiff_image = image.copy()

            if not safe or not os.path.exists(tiff_image_path):
                if tiff_image.size[0] > LARGE_IMAGE_SIZE[0] or tiff_image.size[1] > LARGE_IMAGE_SIZE[1]:
                    tiff_image.thumbnail (LARGE_IMAGE_SIZE, Image.ANTIALIAS)
                tiff_image.save (tiff_image_path)
                tiff_image.save (large_image_path)

                image.thumbnail (THUMB_IMAGE_SIZE, Image.ANTIALIAS)
                image.save (os.path.join (self.thumb_image_dir, root+'.jpg'))
        except Exception as err:
            traceback.print_exc()
            raise ImageProcessingError (sys.exc_info()[1]) from err

if __name__ == '__main__':
    CONFIG = get_config()
    src_path = os.path.join (CONFIG['src_img_filesystem_base'], 'disc2/awards2004')
    img_folder = WebGalleryImageProcessor (src_path)
    img_folder.process_images()

    if 0:  # experiement with one image
        source_image_path = '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc2/awards2004/CRW_7955.CRW'
        try:
            if not os.path.exists(source_image_path):
                raise Exception('FILE DOES NOT EXIST at {}'.format(source_image_path))

            img_folder.process_image(source_image_path)

        except Exception:
            print ("FATAL: {}".format(sys.exc_info()[1]))