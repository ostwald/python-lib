
import os, json
from aspace_model import get_archival_object
from aspace_api_client import get_children
from html_writer import WebGalleryHtmlWriter
from web_gallery import SRC_PATH_BASE

def pp (obj):
    print (json.dumps(obj, indent=2))

def location_to_path (location):
    return os.path.join (os.path.dirname(SRC_PATH_BASE), location)

if __name__ == '__main__':
    archives_file_id = 'archival_objects/22578'
    file_obj = get_archival_object (archives_file_id)

    print ('ARCHIVAL OBJECT CREATED')
    metadata_fields = [
        'title', 'description', 'location', 'date'
    ]
    metadata = {}
    for field in metadata_fields:
        metadata[field] = getattr(file_obj, field)

    # print (metadata)
    image_dir = location_to_path (file_obj.location)
    htmlwriter = WebGalleryHtmlWriter (image_dir, file_obj)
    print ("html writer instantiated")
    htmlwriter.process_images(safe=True)  # don't generate if they already exist

    # obj = htmlwriter.get_child ('CRW_7964')
    # print (obj)

    htmlwriter.write_item_pages()
    htmlwriter.write_index_pages()


    # children_api_response = get_children(archives_file_id)
    # image_metadata_map = {}
    # for image_metadata in children_api_response:
    #     pp (image_metadata)
    #     aspace_id = image_metadata['uri'].replace (image_metadata['repository']['ref']+'/', '')
    #     print ('-', aspace_id)
    #     image_metadata_map[aspace_id] = ArchivalObject(image_metadata)
    # print (len(image_metadata_map), 'metadata items')
    #
    # for key in image_metadata_map:
    #     print (key)
    #     image_metadata = image_metadata_map[key]
    #     filename = os.path.basename(image_metadata.location)
    #     print (' - ', filename)

    # now create the html ...
    # for page in htmlwriter.pages:
    #     print (page)