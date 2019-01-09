"""
Change the top-container for Archival_objects
"""
import json

from ncar_lib.aspace.aspace_proxy import AspaceProxy
from ncar_lib.aspace.aspace_db import ArchivesSpaceDB, ArchivalObjectTable

def pp (obj):
    print json.dumps(obj, indent=4)

class MyProxy (AspaceProxy):
    """
    used to obtain Objects from the API and to update objects via API
    """
    baseurl = 'http://aspace-t.dls.ucar.edu:7089'
    default_user = 'admin'
    default_passwd = 'tornado'

def get_archival_objects_to_update (root_record_id, component_id):
    """
    these will get their top_container normalized
    :return:
    """
    db = ArchivesSpaceDB()
    table = ArchivalObjectTable(db)

    return table.select_objects_to_container_update(root_record_id, component_id)

def set_top_container (archival_record_id, top_container_id):
    proxy = MyProxy()
    archival_record = proxy.get_archival_object(archival_record_id)

    current = str(archival_record.get_top_container())

    if current.endswith(str(top_container_id)):
        return {"status" : 'top container is already %s' % top_container_id}
    else:
        archival_record.set_top_container(top_container_id)
        # pp(obj.get_instance())
        return proxy.update_archival_object(archival_record_id, archival_record.data)

def set_top_container_tester():
    id = '16166'
    top_container_id = '1256'
    proxy = MyProxy()
    obj = proxy.get_archival_object(id)

    resp = set_top_container (id, top_container_id)

    print resp

def batch_container_update (root_record_id, component_id, top_container_id):
    """
    set the top container for all archival objects with matching root_record and component id
    with provided top_container_id
    :return:
    """
    TEST = 1

    to_update = get_archival_objects_to_update(root_record_id, component_id)
    archival_object_ids = map (lambda x:x[0], to_update)
    for id in archival_object_ids:
        if TEST:
            print id
        else:
            result = set_top_container (id, top_container_id)
            print "- %s - %s" % (id, result['status'])

def batch_delete_empty_top_containers (indicator, created_for_collection):
    from aspace_db import get_empty_top_containers

    TEST = 0

    proxy = MyProxy()
    empty_top_containers = get_empty_top_containers(indicator, created_for_collection)
    print 'TEST MODE - no objects will be deleted'

    for id in empty_top_containers:
        if TEST:
            print id, ' - not deleted'
        else:
            resp = proxy.delete_top_container (id)
            print ' - %s - %s' % (id, resp['status'])

if __name__ == "__main__":

    if 0:  #batch container update
        root_record_id = '77'
        component_id = 'RAL Box 16'
        top_container_id = '1643'

        batch_container_update (root_record_id, component_id, top_container_id)

    if 1:  # delete empty top level containers

        indicator = "1"
        created_for_collection = "77"
        batch_delete_empty_top_containers (indicator, created_for_collection)



