import os, sys, time
import globals

class Walker:
    """
    Abstract version of walker. Concrete instances overwrite process_image, etc
    """

    def __init__ (self, start_dir):
        self.start_dir = start_dir
        self.file_cnt = 0
        self.image_cnt = 0
        self.dir_cnt = 0
        self.elapsed = 0
        self.unknown_extensions = []
        self.skipped_directories = []


    def process_image (self, path):
        pass

    def walk (self):
        tics = time.time()
        for root, dirs, files in os.walk(self.start_dir, topdown=True):
            print root

            to_remove = []
            for d in dirs:
                path = os.path.join (root, d)
                if not self.accept_dir(path):
                    to_remove.append(d)
                    self.skipped_directories.append(path)
            for d in to_remove:
                dirs.remove(d)


            for name in files:
                path = os.path.join (root, name)
                ext = os.path.splitext(name)[1]

                if os.path.islink(path):
                    continue

                if not ext in globals.KNOWN_EXTENSIONS and not ext in self.unknown_extensions:
                    self.unknown_extensions.append(ext)

                self.file_cnt += 1

                if ext.lower() in globals.IMAGE_EXTENSIONS:
                    self.image_cnt += 1
                    self.process_image(path)

            for name in dirs:
                # print(os.path.join(root, name))
                self.dir_cnt += 1

        self.elapsed = time.time() - tics

    def accept_dir_strict(self, path):
        dirname = os.path.basename(path)
        if dirname[0] == '.':
            return 0
        # print ' --- ', dirname
        if dirname in globals.SKIP_DIR_NAMES:
            return 0
        for frag in globals.SKIP_DIR_NAME_FRAGS:
            if frag.lower() in dirname.lower():
                return 0
        return 1

    def accept_dir(self, path):
        dirname = os.path.basename(path)
        if dirname[0] == '.':
            return 0
        return 1

if __name__ == '__main__':
    root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/photos/'
    walker = Walker(root)
    walker.walk()
    print '\n{}'.format(root)
    print 'files: {}   imnage files: {}   dirs: {}  elapsed: {}'.format(walker.file_cnt, walker.image_cnt, walker.dir_cnt, walker.elapsed)
    print 'unknown_extensions:', walker.unknown_extensions
    print 'skipped directories'
    for d in walker.skipped_directories:
        print '-', d