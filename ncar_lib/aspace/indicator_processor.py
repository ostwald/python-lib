import sys, os, json
from UserList import UserList
from aspace_db import ArchivesSpaceDB, TopContainerTable, TopContainerLinkTable, get_archival_objects_in_top_container
from aspace_proxy import AspaceProxy
from archival_object_container import set_top_container

class MyProxy (AspaceProxy):
    """
    used to obtain Objects from the API and to update objects via API
    """
    baseurl = 'http://aspace-t.dls.ucar.edu:7089'
    default_user = 'admin'
    default_passwd = 'tornado'

class IndicatorProcessor (UserList):
    """
    self.data is a list of dict objects:

    [
        {
            'top_container_id' : 'X',
            'children_count' : 'N'
        },
    ]
    """

    TEST_MODE = 0

    def __init__ (self, indicator, created_for_collection):
        self.indicator = indicator
        self.created_for_collection = created_for_collection
        self.root_record_id = int(self.created_for_collection)

        self.proxy = MyProxy()

        db = ArchivesSpaceDB()
        self.top_container_table = TopContainerTable(db)
        self.top_container_link_table = TopContainerLinkTable(db)

        self.data = None
        self.count_map = None
        self.aggregator_container_id = None

        self.initialize_data()  # initialize data, count_map and aggregator_container_id



    def initialize_data (self):
        """
        Re-evalutate self.data and self.count_map.

        Must be run after changing structure (e.g., deleting, or moving children)
        :return:
        """
        self.data = self.tally_top_container_counts()
        self.count_map = {}
        for item in self.data:
            self.count_map[item['top_container_id']] = item['children_count']
        self.aggregator_container_id = self.data[0]['top_container_id']

    def get_top_container_ids (self):
        return map (lambda x:x['top_container_id'], self.data)

    def get_container_count(self, top_container_id):
        return self.count_map[top_container_id]

    def remove_empty_containers (self):
        """
        get rid of all the empty containers for this indicator
        :return:
        """
        print 'remove_empty_containers()'
        removed = []

        for container_id in self.get_top_container_ids():
            count = self.get_container_count(container_id)
            # print '\n', container_id
            # print ' - count: %d' % count
            if count > 0:
                continue
            else:
                if self.TEST_MODE:
                    print ' - would have Deleted %s' % container_id
                else:
                    # print ' - deleting %s' % container_id
                    resp = self.proxy.delete_top_container (container_id)
                    removed.append(container_id)
                    try:
                        print ' - %s - %s' % (container_id, resp['status'])
                    except:
                        # ignore TopContainer not found
                        if resp.has_key('error') and not resp['error'] == 'TopContainer not found':
                            print json.dumps(resp, indent=3)

        print '- %d top_containers removed' % len(removed)
        # print removed

        self.initialize_data()


    def move_archival_objects_to_aggregator (self):
        """
        for each container, move each of the archival_objects to
        the aggregator containter
        :return:
        """

        print 'move_archival_objects_to_aggregator()'
        moved = []
        for container_id in self.get_top_container_ids():
            # print '- container_id', container_id
            for archival_object_id in get_archival_objects_in_top_container(container_id):
                # print '  - child %s' % archival_object_id
                if self.TEST_MODE:
                    print 'would have moved to %s' % self.aggregator_container_id
                else:
                    #do the move!
                    try:
                        resp = set_top_container (archival_object_id, self.aggregator_container_id)

                        if resp.has_key('error'):
                            if not resp['error'] =="TopContainer not found":
                                print resp

                        if resp.has_key('status'):
                            if resp['status'].startswith ("top container is already"):
                                pass # ignore
                            else:
                                if resp['status'] == 'Updated':
                                    moved.append(archival_object_id)
                                else:
                                    print resp

                    except Exception, msg:
                        print 'WARN: archival_object_%s could not be moved? %s' % (archival_object_id, msg)

        print '- %d archival_objects moved to %s' % (len(moved), self.aggregator_container_id)
        self.initialize_data()

    def process (self):

        self.remove_empty_containers()

        self.move_archival_objects_to_aggregator()

        self.remove_empty_containers()

        # container_ids = self.get_top_container_ids()
        # for container_id in container_ids:
        #     print container_id

    def tally_top_container_counts (self):
        """
        tally will become this IndicatorProcessor's  data list
        :return:
        """
        tally = []

        # ids = table.select_containers("18", "77")
        ids = self.top_container_table.select_containers(self.indicator, self.created_for_collection)

        for top_container_id in ids:
            children_count = self.top_container_children_count(top_container_id)
            tally.append ({
                'top_container_id':top_container_id,
                'children_count' : children_count
            })

        tally.sort (key=lambda x:-int(x['children_count']))

        return tally

    def report_container_counts(self):
        tally = self.tally_top_container_counts()
        for item in tally:
            print " - %s (%d)" % (item['top_container_id'], item['children_count'])


    def top_container_children_count (self, top_container_id):
        return  len(self.top_container_link_table.get_children(top_container_id))



class CollectionProcessor:

    def __init__ (self, id):
        self.id = id
        db = ArchivesSpaceDB()
        self.top_container_table = TopContainerTable(db)
        self.indicators = self.top_container_table.get_distinct_indicators (self.id)

    def process(self):
        for indicator in self.indicators:
            print '\nINDICATOR - %s' % indicator
            ip = IndicatorProcessor (indicator, self.id)

            ip.process()

    def report(self):
        for indicator in self.indicators:
            print '\nINDICATOR - %s' % indicator
            ip = IndicatorProcessor (indicator, self.id)

            ip.report_container_counts ()


if __name__ == "__main__":
    if 0:
        # print top_container_children_count ('843')
        # find_archival_object_children_tester()

        # collection_top_containers_by_indicator()
        indicator = '25'
        created_for_collection = '77'
        ip = IndicatorProcessor (indicator, created_for_collection)

        print '%s aggregator: %s' % (indicator, ip.aggregator_container_id)
        print ' -- agg count: %s' % ip.get_container_count(ip.aggregator_container_id)
        print '------------------------------------------------'

        # ip.process()

        print '------------------------------------------------'
        ip.report_container_counts()

        # print 'top_container_ids: %s' % ip.get_top_container_ids()

    elif 1:
        collection = CollectionProcessor('54')
        collection.report()
        # collection.process()