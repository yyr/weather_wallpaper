#!/usr/bin/env python
'''This program downloads weather satellite map and changes desktop wall
paper(cron it for timely). Works for Gnome 2 and 3.  Japanese Meteorological
Agency(JMA) is the relevant source for me where I live but You can adopt by
changing source.
'''

AUTHOR = "Yagnesh Raghava Yakkala"
WEBSITE = "http://yagnesh.org"
LICENSE ="GPL v3 or later"

import sys

class backgroundSetter(object):
    """set the background, based on system gnome version
    """
    SCHEMA = 'org.gnome.desktop.background'
    KEY = 'picture-uri'

    def __init__(self,img):
        """
        """
        self._img = img
        from os import path
        if path.exists("/usr/share/gnome-about/gnome-version.xml"):
            self._gnome_version = 2
        else:
            self._gnome_version = 3

    def change_background(self):
        if self._gnome_version == 2:
            try:
                import gconf
            except:
                print  'You need to install the python bindings for gconf'
                sys.exit(4)

            gconf_client = gconf.client_get_default()
            bg = gconf_client.get_string("/desktop/gnome/background/picture_filename")
            gconf_client.set_string("/desktop/gnome/background/picture_filename",self._img)

        elif self._gnome_version == 3:
            from gi.repository import Gio
            print('not yet implemented')
            sys.exit(2)
        else:
            print 'Only works for Gnome desktop right now'
            sys.exit(64)

def main():
    # current = mapDownloader()
    # bg = backgroundSetter(current.img)
    bg = backgroundSetter("/home/yagnesh/git/weather_wallpaper/201209201015-00.png")
    bg.change_background()

#client.set_string("/desktop/gnome/background/picture_filename","home/tsudot/Pictures/zombie.jpg")
#http://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/201209201015-00.png

if __name__ == '__main__':
    main()
