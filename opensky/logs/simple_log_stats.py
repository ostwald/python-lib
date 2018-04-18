import sys, os
# from subprocess import call

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'arg required'
        sys.exit()
    file = sys.argv[1]
    if not os.path.exists(file):
        print 'file does not exist at %s' % file
        sys.exit()

    # call (['wc', '-l', file])
    # call (['grep', 'heap', file, '|', 'wc', '-l'])
    os.system('wc -l ' + file)
    os.system("grep heap " + file + " | wc -l")
    os.system("grep 'java.net.SocketException: Broken pipe' " + file + " | wc -l")
