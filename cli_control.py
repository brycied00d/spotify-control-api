#!/usr/bin/env python2

import dbus
import sys

if __name__ == '__main__':
  bus = dbus.SessionBus()
  # Setup the interfaces required to fetch Now Playing
  player = bus.get_object('com.spotify.qt', '/')
  iface = dbus.Interface(player, 'org.freedesktop.MediaPlayer2')
  info = iface.GetMetadata()
  # Print Now Playing
  print str(info['xesam:artist'][0]) + " - " + str(info['xesam:title'])

  # Set volume - doesn't work
  print iface.SetVolume(50)
  print iface.Volume()

  session = bus.get_session()
  spotify = session.get_object("org.mpris.MediaPlayer2.spotify",
                               "/org/mpris/MediaPlayer2")
  # Hopefuly only good commands are passed
  for command in sys.argv[1:]:
    getattr(spotify, command)()

