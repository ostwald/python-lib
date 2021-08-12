"""
Comms Site Builder

- Access ArchivesSpace to obtain folder metadata
- Use location to
    - create directories and process images via

"""
from aspace_model import ArchivalObject
from aspace_api_client import get_object

if __name__ == '__main__':
    archives_file_id = 'archival_objects/22578'
    file_data = get_object (archives_file_id)
    file_obj = ArchivalObject(file_data)

    # use location to setup dst_dir and process images



    metadata_fields = [
        'title', 'description', 'location', 'date'
    ]
    metadata = {}
    for field in metadata_fields:
        metadata[field] = getattr(file_obj, field)

    print (metadata)