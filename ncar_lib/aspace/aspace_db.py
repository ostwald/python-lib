from mysql import GenericDB, TableRow
import MySQLdb
from UserDict import UserDict
from UserList import UserList
import codecs

class GenericTable (UserDict):
    """
    table and schema must be overwritten
    """
    table = ''

    def __init__ (self, db):
        """
        :param db: instance of GenericDB
        """
        self.data = {}
        self.db = db
        self.table_schema = self.db.getSchema(self.table)

    def get_results (self, query):
        return self.db.doSelect (query)

    def show_results(self, rows):
        print len(rows), " found"
        for row in rows:
            print row

class ArchivesSpaceDB (GenericDB):

    host = "aspace-t-staff.dls.ucar.edu"
    user = "archivesspace"
    password = "archivesisspace!"
    db = "archivesspace"

    def __init__ (self, host=None, user=None, password=None, db=None):
        # GenericDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)
        GenericDB.__init__ (self)

    def getConnection (self):
        return MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)

class ArchivalObjectTable (GenericTable):
    """
    wrapper for table
    """
    table = 'archival_object'
    schema = ["id", "title", "display_string"]

    def get_object_children(self, parent_id):
        fields = ['id','title']
        query = "SELECT %s FROM %s.%s WHERE parent_id='%s'" % \
                (','.join(fields), self.db.db, self.table, parent_id)
        # print "QUERY: %s" % query
        return self.get_results(query)

    def select_objects_to_container_update (self, root_record_id, component_id):
        fields = ['id','root_record_id', 'component_id']
        query = """SELECT %s
                   FROM %s.%s
                   WHERE root_record_id = '%s' AND component_id = '%s'
                      AND  parent_id is NOT NULL; """ % \
                (','.join(fields), self.db.db, self.table, root_record_id, component_id)
        return self.get_results(query)

    def get_unique_component_ids (self, root_record_id):
        query = "SELECT DISTINCT component_id  FROM archivesspace.archival_object WHERE root_record_id = '%s';" % root_record_id
        return map (lambda x:x[0], self.get_results(query))

class TopContainerLinkTable (GenericTable):
    """
    wrapper for table
    """
    table = 'top_container_link_rlshp'
    schema = ["id", "top_container_id", "sub_container_id"]

    def get_children (self, top_container_id):
        query = "SELECT %s  FROM %s.%s WHERE top_container_id='%s';" % \
            (','.join(self.schema), self.db.db, self.table, top_container_id)

        return self.get_results(query);

class TopContainerTable (GenericTable):
    table = 'top_container'
    schema = ["id", "indicator", "created_for_collection"]


    def select_containers (self, indicator, created_for_collection):
        query = """SELECT %s
                   FROM %s.%s
                   WHERE indicator='%s'
                   AND created_for_collection='/repositories/2/resources/%s';""" % \
                (','.join(self.schema), self.db.db, self.table, indicator, created_for_collection)
        results = self.get_results(query);
        return map (lambda x:int(x[0]), results)

    def get_distinct_indicators (self, created_for_collection):
        """
        return list of distinct indicators sorted numerically
        :param created_for_collection:
        :return:
        """
        query = """SELECT DISTINCT indicator
                   FROM %s.%s
                   WHERE created_for_collection='/repositories/2/resources/%s';""" % \
                (self.db.db, self.table, created_for_collection)
        results = self.get_results(query);
        num_results = map (lambda x:int(x[0]), results)
        return map (lambda x:str(x), sorted(num_results))


class InstanceTable (GenericTable):
    table = 'instance'

    def get_archival_object_id (self, id):
        query = """SELECT archival_object_id
                   FROM %s.%s
                   WHERE id='%s';""" % \
                (self.db.db, self.table, id)
        results = self.get_results(query);
        # we expect only one result
        return results[0][0]

class SubContainerTable (GenericTable):
    table = 'sub_container'

    def get_instance_id (self, sub_container_id):
        query = "SELECT instance_id FROM %s.%s WHERE id='%s';" % \
                (self.db.db, self.table, sub_container_id)
        # print query
        results = self.get_results(query);

        # we expect only one result
        return results[0][0]

class NoteTable (GenericTable):
    table = 'note'

    def get_note_blob (self, note_id):
        query = "SELECT id, notes FROM %s.%s WHERE id='%s';" % (self.db.db, self.table, note_id)
        results = self.get_results(query)

        # single result, notes field
        return results[0][1]

def find_archival_object_children (parent_id):
    """
    return the ids of the children of specified archival_object
    :param parent_id:
    :return:
    """
    db = ArchivesSpaceDB()
    table = ArchivalObjectTable(db)

    results = table.get_object_children(parent_id)

    if 0: # verbose
        print 'CHILDREN of %s (%d results)' % (parent_id, len(results))
        for row in results:
            print "- %s - %s" % (row[0], truncate(row[1]))

    return map (lambda x:x[0], results)

def truncate (s, max_len=100):
    if len(s) > max_len - 4:
        return s[:(max_len - 4)] + " ..."
    return s

def find_archival_object_children_tester():
    parent_id = '15996'
    ids = find_archival_object_children(parent_id)

    for id in ids:
        print id

def top_container_children_count (top_container_id):
    db = ArchivesSpaceDB()
    table = TopContainerLinkTable(db)
    results = table.get_children(top_container_id)
    # table.show_results(results)
    return len(results)


def tally_top_container_counts_for_indicator (indicator, created_for_collection):
    tally = {}
    db = ArchivesSpaceDB()
    table = TopContainerTable(db)
    # ids = table.select_containers("18", "77")
    ids = table.select_containers(indicator, created_for_collection)

    for top_container_id in ids:
        children_count = top_container_children_count(top_container_id)
        tally[top_container_id] = children_count

    return tally

def report_top_containers (indicator, created_for_collection):
    """
    report containers having the same indicator and created_for_collection valiues
    :param indicator:
    :param created_for_collection:
    :return:
    """
    # db = ArchivesSpaceDB()
    # table = TopContainerTable(db)
    # # ids = table.select_containers("18", "77")
    # ids = table.select_containers(indicator, created_for_collection)
    #
    # for top_container_id in ids:
    #     children_count = top_container_children_count(top_container_id)
    #     print ' - %s (%s)' % (top_container_id, children_count)

    tally = tally_top_container_counts_for_indicator (indicator, created_for_collection)
    for top_container_id in tally.keys():
        children_count = tally[top_container_id]
        print ' - %s (%s)' % (top_container_id, children_count)

def get_empty_top_containers (indicator, created_for_collection):
    # db = ArchivesSpaceDB()
    # table = TopContainerTable(db)
    # # ids = table.select_containers("18", "77")
    # top_container_ids = table.select_containers(indicator, created_for_collection)

    top_container_ids = get_top_containers_for_indicator(indicator, created_for_collection)

    empty_top_container_ids = []

    for top_container_id in top_container_ids:
        children_count = top_container_children_count(top_container_id)
        if children_count == 0:
            empty_top_container_ids.append(top_container_id)
    return empty_top_container_ids

def get_archival_objects_in_top_container (top_container_id):

    archival_object_ids = []
    # get children (sub_containers) of top_container_id

    db = ArchivesSpaceDB()
    top_container_table = TopContainerLinkTable(db)
    sub_container_table = SubContainerTable(db)
    instance_table = InstanceTable(db)


    results = top_container_table.get_children(top_container_id)
    sub_container_ids = map (lambda x:x[0], results)

    for sub_container_id in sub_container_ids:

        # get instance_id from sub_container_id
        instance_id = sub_container_table.get_instance_id (sub_container_id)

        # get archival_object_id from instance id
        archival_object_id = instance_table.get_archival_object_id (instance_id)

        archival_object_ids.append(archival_object_id)
    return archival_object_ids

def report_archival_objects_in_top_container (top_container_id):
    ids = get_archival_objects_in_top_container(top_container_id)
    print 'archival objects (%d) in container #%s' % (len(ids), top_container_id)
    for id in sorted(ids):
        print '-',id


def report_unique_component_ids (root_record_id):
    """
    report the number of archival objects having each of the values for component ids
    :param root_record_id:
    :return:
    """
    db = ArchivesSpaceDB()
    table = ArchivalObjectTable(db)
    component_ids = table.get_unique_component_ids(root_record_id)
    for comp_id in component_ids:
        query = "SELECT COUNT(*)  FROM archivesspace.archival_object WHERE component_id = '%s';" % comp_id
        # result =  map (lambda x:x[0], table.get_results(query)[0])
        result =  table.get_results(query)

        print result

    print '%s (%s)' % (comp_id, result[0][0])


def print_note_data (note_id):
    import json
    db = ArchivesSpaceDB()
    table = NoteTable(db)
    note_json = json.loads(table.get_note_blob(note_id))
    print json.dumps(note_json, indent=4)
    if note_json.has_key('content'):
        if type(note_json['content']) == type([]):
            for para in  note_json['content']:
                print '\n',para
        else:
            print note_json['content']

# def collection_top_containers_by_indicator ():
#     """
#     For each distinct indicator for given collection,
#     show all top_containers and contents count
#     :return:
#     """
#     db = ArchivesSpaceDB()
#     table = TopContainerTable(db)
#     created_for_collection = '77'
#     indicators = table.get_distinct_indicators (created_for_collection)
#     for indy in indicators:
#         print '\nIndicator %s' % indy
#
#         report_top_containers (indy, created_for_collection)
#
#         # get the

def get_top_containers_for_indicator (indicator, created_for_collection):
    db = ArchivesSpaceDB()
    table = TopContainerTable(db)
    # ids = table.select_containers("18", "77")
    return table.select_containers(indicator, created_for_collection)





if __name__ == "__main__":
    # print top_container_children_count ('843')
    # find_archival_object_children_tester()

    # collection_top_containers_by_indicator()
    indicator = '7'
    created_for_collection = '77'
    ip = IndicatorProcessor (indicator, created_for_collection)

    print '%s aggregator: %s' % (indicator, ip.aggregator_container_id)
    print ' -- agg count: %s' % ip.get_container_count(ip.aggregator_container_id)
    ip.process()



    # ids = table.select_containers("18", "77")
    #
    # for top_container_id in ids:
    #     children_count = top_container_children_count(top_container_id)
    #     print ' - %s (%s)' % (top_container_id, children_count)

    # indicator = "1"
    # created_for_collection = "77"
    # report_top_containers (indicator, created_for_collection)


    # get_archival_objects_in_top_container ('1')

    # get children (sub_containers) of top_container_id
    # top_container_id = '1231'
    # report_archival_objects_in_top_container(top_container_id)

    # root_record_id = '77'
    # report_unique_component_ids (root_record_id)

    #show all the notes from resource 53
    # for i in range(3674,3683):
    #     print i
    #     print_note_data (i)