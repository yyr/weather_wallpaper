#!/usr/bin/env python
# [[[cog import cog; cog.out('"""\n{0}\n"""'.format(file('./README.rst').read()))]]]

"""
Weather Wallpaper
=================

Tiny python script to update wallpaper with satellite weather map from a
server (IMD and JMA currently). Works for Gnome 2 and 3.  Indian
Meteorological Department (IMD) is the relevant server for me. It can be
extended for other servers as well.

# one may want add crontab as following to update the wallpaper for every hour
# at 6th minute
6 * * * * /path/to/weather_wallpaper/weather_wallpaper.py


License
=======
GPL v3 (or later)

"""
# [[[end]]]

AUTHOR = "Yagnesh Raghava Yakkala"
WEBSITE = "http://yagnesh.org"
LICENSE ="GPL v3 or later"

import sys, os

class mapDownloader(object):
    """Dummy parent class for map server"""
    def map_url(self):
        pass

    def download_map(self):
        import urllib
        p, status = urllib.urlretrieve(self.url,self.file_name,None)
        return(status)


class JMA(mapDownloader):
    def __init__(self,at_time='latest'):
        self._url_root = "http://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/"
        self._at_time = at_time
        self.url = self.map_url(self._at_time)

    def map_url(self,at_time):
        """Construct url with given time, if at_time is 'latest' construct url for
        latest image. JMA updates hourly twice.

        """
        from time import strftime, localtime
        if at_time == 'latest':
            file_base = strftime("%Y%m%d%H")
            if localtime().tm_min <= 45:
                file_tail = "00-00.png"
            else:
                file_tail = "15-00.png"
            self.file_name = file_base + file_tail
            return(self._url_root + self.file_name)
        else:
            return None



class IMD(mapDownloader):
    """Images from Indian Meteorological Department(IMD) site"""
    def __init__(self,at_time='latest'):
        self._url_root = 'http://satellite.imd.gov.in/img/'
        self._at_time  = at_time
        self.url = self.map_url(self._at_time)
        self.file_name = "3Dasiasec_ir1.jpg"

    def map_url(self, at_time):
        """IMD only keeps latest images."""
        if not at_time == 'latest':
            print('IMD only keeps latest images.')
            sys.exit(2)
        else:
            return('http://satellite.imd.gov.in/img/3Dasiasec_ir1.jpg')




class backgroundSetter(object):
    """set the background, based on system gnome version
    """
    def __init__(self,img):
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
                print('You need to install the python bindings for gconf')
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
            print('Only works for Gnome desktop right now')
            sys.exit(64)


def arg_parse(at_time, server, log=None, log_level=None):
    current_map = globals()[server](at_time)

    if current_map.download_map():
        bg = backgroundSetter(os.path.abspath(current_map.file_name))
        bg.change_background()
    else:
        print("Failed to download weather map")


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__)
    parser.add_argument('-s','--server', dest='server',choices=['JMA', 'IMD'],
                        default='IMD')
    parser.add_argument('-t','--at-time', help='Where AT_TIME=YYYY-MM-DD-HH'
                        ,default='latest')
    parser.add_argument('--log', help='log file.')
    parser.add_argument('--log-level',
        choices=['WARN', 'INFO'],
        help='Logging level for log file.')

    arg_parse(**vars(parser.parse_args(args)))


if __name__ == '__main__':
    main()
