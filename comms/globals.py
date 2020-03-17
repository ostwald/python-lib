import os, sys

composite_sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'


# during initial disk scan, we can use these to halt the traversal (and not descend into
# these dirs. But after stuff is in the database we can concat them together to filter.
SKIP_DIR_NAMES = [
    'Fonts', 'Links', '_notes', 'Previews', 'Thumbnails'
]

SKIP_DIR_NAME_FRAGS = [
    'iMovie', 'Application Support', '.Trash', 'Applications','Caches','Mail', 'System', 'Library'
]

SKIP_DIR_PATHS = [
]

def make_path (frag):
    base_path = '/Volumes/archives/CommunicationsImageCollection/'
    return os.path.join (base_path, frag)

def normalize_db_path(path):
    return path.replace("'", "''").replace (u'\u2019', "''")

def normalize_file_path(path):
    return path.replace ("%27", "'")

IMAGE_EXTENSIONS = [
    '.2jpg',
    '.cr2',
    '.crw',
    '.dng',
    '.eps',
    '.gif',
    '.gif3',
    '.jfif',
    '.jpe',
    '.jpeg',
    '.jpg',
    # '.jsp',
    '.nef',
    '.png',
    '.tif',
    '.tiff',
    '.pict',
]

db_folder_names = [
    'CarlyeMainDisk1',
    'CarlyeMainDisk2',
    'CIC-ExternalDisk1',
    'CIC-ExternalDisk2',
    'CIC-ExternalDisk4',
    'CIC-ExternalDisk6',
    'CIC-ExternalDisk7',
]

def isImage(filename):
    try:
        return os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS
    except:
        print 'isImage error: {}'.format(sys.exc_info()[1])
        return False

def get_dir_iamges (dirname):
    return filter (isImage, os.listdir(dirname))


KNOWN_EXTENSIONS = [
    '', '.psd', '.css', '.html', '.shtml', '.jsp', '.doc', '.swf', '.rpm', '.LCK',
    '.php', '.jpg', '.gif', '.tif', '.eps', '.txt', '.pdf', '.zip', '.JPG', '.htm',
    '.png', '.jfif', '.mov', '.js', '.xml', '.out', '.pps', '.ico', '.wmv', '.ai',
    '.db', '.save', '.bak', '.ps', '.ppsx', '.ppt', '.xls', '.redirect', '.00',
    '.01', '.02', '.old', '.99', '.tar', '.after', '.20091012', '.new', '.sorted',
    '.pm', '.bogus', '.03', '.04', '.05', '.06', '.07', '.08', '.final', '.dbx',
    '.dwt', '.000511', '.orig', '.wmz', '.mso', '.jpeg', 'JPEG','.GIF', '.lbi', '.tiff',
    '.docx', '.flv', '.jsp#', '.', '.avi', '.mp3', '.mpeg', '.spring', '.php~',
    '.html~', '.phpYY', '.inc', '.bak2', '.php#', '.tld', '.properties', '.class', '.jar',
    '.CR2', '.xmp', '.CRW',
    '.dmg', '.xlsx', '.pptx', '.indd', '.lst', '.dfont', '.otf', '.ttf', '.2jpg',
    '.eot', '.svg', '.woff', '.TIF', '.mpg', '.dv', '.MOV', '.THM', '.rm', '.epsi',
    '.vol2', '.edu_iss_dmc_v', '.WAV', '.gif3', '.doc ', '.iMovieProj', '.webarchive',
    '.TTF', '.java', '.m4v', '.mp4', '.wav', '.~iMovieProj', '.plist', '.bmp', '.fcp',
    '.fla', '.AVI', '.m2v', '.TDT', '.TID', '.BDM', '.CPI', '.MPL', '.MTS', '.TMP',
    '.pictClipping', '.ivr', '.h3r', '.exe', '.JPG_', '.XMP', '.3', '.PNG',
    '.textClipping', '.NEF', '.dng', '.jpg alias', '.cr2', '.url', '.ttc',
    '.suit', '. 20', '.TXT', '.rtf', '.5', '.dylib', '.nib', '.icns', '.strings',
    '.prl', '.conf', '.colorFillLayerPreset', '.EPS', '.AFM', '.bom', '.gz', '.info',
    '.DAT', '.PSD', '.advisory', '.dot', '.fp7', '.log', '.qxd', '.pg', '.1', '.qt',
    '.09', '.Green', '.jpe', '.mno', '.ase', '.aiff', '.par', '.srt', '.LW', '.recordphp',
    '.json', '.odt', '.sub', '.tmp', '.sit', '.mxp', '.PDF', '.img', '.PICT'

]

VIDEO_EXTENSIONS = [
    '.afm',
    '.ai',
    '.aiff',
    '.aif',
    '.avi',
    '.avi',
    '.cpi',
    '.cr2',
    '.cr2',
    '.crw',
    '.dng',
    '.dv',
    '.dwt',
    '.dylib',
    '.fla',
    '.flv',
    '.fp7',
    '.h3r',
    '.imovieproj',
    '.ivr',
    '.jfif',
    '.jpe',
    '.lw',
    '.m2v',
    '.m4v',
    '.mov',
    '.mov',
    '.mp3',
    '.mp4',
    '.mpeg',
    '.mpg',
    '.mts',
    '.nef',
    '.odt',
    '.otf',
    '.par',
    '.pg',
    '.pm',
    '.png',
    '.psd',
    '.qt',
    '.qxd',
    '.rtf',
    '.svg',
    '.swf',
    '.thm',
    '.tid',
    '.ttc',
    '.ttf',
    '.ttf',
    '.wav',
    '.wmv',
    '.wmz',
]