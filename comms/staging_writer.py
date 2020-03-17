"""
Use comms writer to write Staging files to "Field Projects" in de-duped
"""

from comms_writer import Writer

class StageWriter (Writer):

    src_base_dir = '/Volumes/archives/CommunicationsImageCollection/Staging'
    dest_base_dir = '/Volumes/cic-de-duped/Field Projects'
    start_with_frest_dest_sqlite_file = False

if __name__ == '__main__':

    sqlite_file = globals.composite_sqlite_file
    # dest_sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    dest_sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/field_projects_duped.sqlite'

    # path_pat = 'disc 1/360 lobby tour/IMG_2613.JPG'
    path_pat = '/Volumes/archives/CommunicationsImageCollection/Staging'
    # path_pat = None
    writer = Writer(globals.composite_sqlite_file, dest_sqlite_file, path_pat)
    start = 18000
    writer.write_all_records(start=start)