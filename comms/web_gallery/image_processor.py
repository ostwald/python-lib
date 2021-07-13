import sys, os, re
import rawpy
from PIL import Image

from web_gallery import WebGalleryFolder

RAW_EXTENSIONS = ['.CR2']
LARGE_IMAGE_SIZE = (1200, 1200)
THUMB_IMAGE_SIZE = (200, 200)

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
        print ('processing raw')
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

    def process_images(self):
        for img_name in os.listdir(self.src_path):
            img_path = os.path.join (self.src_path, img_name)
            try:
                self.process_image (img_path)
            except ImageProcessingError:
                print ("ImageProcessingError for {}: {}".format(img_path, sys.exc_info()[1]))
                break

    def process_image (self, image_path):
        try:
            image = get_image(image_path)
            # process the image at path
            root, ext = os.path.splitext(os.path.basename (image_path))
            large_image = image.copy()
            if large_image.size[0] > LARGE_IMAGE_SIZE[0] or large_image.size[1] > LARGE_IMAGE_SIZE[1]:
                large_image.thumbnail (LARGE_IMAGE_SIZE, Image.ANTIALIAS)
            large_image.save (os.path.join (self.large_image_dir, root+'.tiff'))

            image.thumbnail (THUMB_IMAGE_SIZE, Image.ANTIALIAS)
            image.save (os.path.join (self.thumb_image_dir, root+'.jpg'))
        except Exception as err:
            raise ImageProcessingError (sys.exc_info()[1]) from err

if __name__ == '__main__':

    img_folder = WebGalleryImageProcessor (src_path)
    img_folder.process_images()