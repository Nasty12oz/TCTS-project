import os
import kivy
import shutil

if __name__ == '__main__':
    if 'gstplayer' in os.listdir(kivy.__file__[:-11]+'lib/'):
        shutil.rmtree(kivy.__file__[:-11] + 'lib/gstplayer/')
    else:
        print('Everything is okay!')
