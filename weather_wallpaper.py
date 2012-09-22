#!/usr/bin/env python
'''This program downloads weather satellite map and sets it as desktop wall
paper(cron it for timely). Works for Gnome 2 and 3.  Japanese Meteorological
Agency(JMA) is the relevant source for me where I live but you can adopt by
changing source.
'''

AUTHOR = "Yagnesh Raghava Yakkala"
WEBSITE = "http://yagnesh.org"
LICENSE ="GPL v3 or later"

import sys, os

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
            SCHEMA = 'org.gnome.desktop.background'
            KEY = 'picture-uri'
            from gi.repository import Gio
            gs = Gio.Settings.new(SCHEMA)
            gs.set_string(KEY, 'file://%s' % self._img)
            gs.apply()
        else:
            print 'Only works for Gnome desktop right now'
            sys.exit(64)

class mapDownloader(object):
    def __init__(self, site):
        """ download the map.

        Arguments:
        - `site`: source of maps
        """
        self._site = site
        self.url = self.construct_url()

    def construct_url(self):
        from time import strftime,localtime

        # JMA
        # eg url: http://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/201209201015-00.png
        if self._site == "jma":
            url_base = "http://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/"
            file_base = strftime("%Y%m%d%H")
            if localtime().tm_min <= 45:
                file_tail = "00-00.png"
            else:
                file_tail = "15-00.png"
            self.file_name = file_base + file_tail
            return(url_base + self.file_name)
        else:
            exit(64)

    def download_map(self):
        import urllib
        urllib.urlretrieve(self.url,self.file_name,None)

def main():
    current_map = mapDownloader("jma")
    current_map.download_map()

    bg = backgroundSetter(os.path.abspath(current_map.file_name))
    bg.change_background()




if __name__ == '__main__':
    main()
