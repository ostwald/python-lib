import os


if 0:
    for disc_num in range(50,100):
        command = 'python dir_lister.py {} > listings/disc_{}.txt'.format(disc_num, disc_num)
        print command
        os.system(command)
        print  ' ... done'