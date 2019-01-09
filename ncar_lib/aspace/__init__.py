# -*- coding: utf-8 -*-

import requests
from UserDict import UserDict
from model import SearchResponse, SearchResult, ArchivalObject, TopContainer
import json

from archival_object_container import batch_container_update, batch_delete_empty_top_containers, get_archival_objects_to_update
from aspace_db import report_top_containers


def show_objects_to_update(root_record_id, component_id):
    objects = get_archival_objects_to_update (root_record_id, component_id)

if __name__ == "__main__":

    indicator = "6"
    created_for_collection = "77"
    top_container_id = "1231"
    # component_id =
    root_record_id = created_for_collection

    report_top_containers (indicator, created_for_collection)
    # batch_delete_empty_top_containers (indicator, created_for_collection)

    # batch_container_update (root_record_id, component_id, top_container_id)

    # ONE OFF
    # top_container_id =
    # set_top_container (archival_record_id, top_container_id)