#!/usr/bin/env python

import dbus
import sys

if __name__ == '__main__':
  session = dbus.SessionBus.get_session()
  spotify = session.get_object("org.mpris.MediaPlayer2.spotify",
                               "/org/mpris/MediaPlayer2")
  # Hopefuly only good commands are passed
  for command in sys.argv[1:]:
    getattr(spotify, command)()

