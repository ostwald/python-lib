
import os, json
import sys

from aspace_model import get_archival_object
from aspace_api_client import get_children
from html_writer import WebGalleryHtmlWriter
from web_gallery import SRC_PATH_BASE

class UnpublishedException (Exception):
    pass

def pp (obj):
    print (json.dumps(obj, indent=2))

def location_to_path (location):
    return os.path.join (os.path.dirname(SRC_PATH_BASE), location)

def is_prefix_less_singlton (path):
    if not os.path.exists(path):
        filenames = filter (lambda x:"DS_Store" not in x, os.listdir(os.path.dirname(path)))
        if len (list(filenames))     == 1:
            return True

def render_object(archives_file_id):
    """

    :param archives_file_id: e.g., 'archival_objects/23057'
    :return:
    """
    archival_object = get_archival_object (archives_file_id)

    if not archival_object.publish:
        raise UnpublishedException ("{} is an unpublished object. Cannot create webgallery.".format(archives_file_id))

    metadata_fields = [
        'title', 'description', 'location', 'date'
    ]
    metadata = {}
    for field in metadata_fields:
        metadata[field] = getattr(archival_object, field)

    # print (metadata)
    image_dir = location_to_path (archival_object.location)
    if not os.path.exists(image_dir) and is_prefix_less_singlton(image_dir):
        image_dir = os.path.dirname(image_dir)

    htmlwriter = WebGalleryHtmlWriter (image_dir, archival_object)
    print ("html writer instantiated for {}".format(archives_file_id))
    htmlwriter.process_images(safe=True)  # don't generate if they already exist

    htmlwriter.init_images()

    # obj = htmlwriter.get_child ('CRW_7964')
    # print (obj)

    htmlwriter.write_item_pages()
    if len(htmlwriter.images) > 1:
        htmlwriter.write_index_pages()

    print ('location: ' + htmlwriter.archival_object.location);
    print ('rel_path: ' + htmlwriter.archival_object.rel_path);
    print ('publish: ', htmlwriter.archival_object.publish);
    # pp (htmlwriter.archival_object.data)


if __name__ == '__main__':
    if 1:   # render these test object uris

        archives_file_ids = [
            'archival_objects/22578', # vanilla (test)
            'archival_objects/23123', # singleton (prod) no filename
            'archival_objects/23057', # singleton (prod) filename no suffix
            'archival_objects/23115' # singleton (prod) not published
            # 'archival_objects/22262' # nested (prod?)
        ]

        for archives_file_id in archives_file_ids:
            try:
                render_object('/repositories/2/' + archives_file_id)
            except UnpublishedException as err:
                print ('WARN: {}'.format(err))

    if 0:
        from aspace_model import ArchivalObject
        parent_api = '/repositories/2/archival_objects/22261'
        children_api_response = get_children(parent_api)
        image_metadata_map = {}
        for image_metadata in children_api_response[5:20]:
            # pp (image_metadata)
            aspace_id = image_metadata['uri'].replace (image_metadata['repository']['ref']+'/', '')
            # print ('-', aspace_id)
            # print ('-', image_metadata['uri'])
            image_metadata_map[image_metadata['uri']] = ArchivalObject(image_metadata)
            try:
                render_object(image_metadata['uri'])
            except UnpublishedException as err:
                print ('WARN: {}'.format(err))

        # print (len(image_metadata_map), 'children items found for {}'.format(parent_api))

        # for key in image_metadata_map:
        #     image_metadata = image_metadata_map[key]
        #     try:
        #         filename = os.path.basename(image_metadata.location)
        #         # print (' - ', filename)
        #         print (' - {} - {}'.format(key, image_metadata.location))
        #     except:
        #         print (sys.exc_info())

        # now create the html ...
        # for page in htmlwriter.pages:
        #     print (page)