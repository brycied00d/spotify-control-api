#!/usr/bin/env python2
# vim: et sw=2 ts=2
""" Returns responses as Aastra XML formatted messages
Notes:
periodic refresh
"""

import cherrypy
import dbus

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def strongly_expire(func):
  """Decorator that sends headers that instruct browsers and proxies not to cache.
  """
  def newfunc(*args, **kwargs):
    cherrypy.response.headers['Expires'] = 'Sun, 19 Nov 1978 05:00:00 GMT'
    cherrypy.response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    cherrypy.response.headers['Pragma'] = 'no-cache' 
    return func(*args, **kwargs)
  return newfunc

def aastra_xml(base="SoftKey:Done", text="Nothing to display."):
  cherrypy.response.headers['Refresh'] = "3; url={base:s}/".format(base=base)
  from xml.sax.saxutils import escape
  return """<?xml version="1.0" encoding="UTF-8"?>
<AastraIPPhoneTextScreen scrollLeft="{base:s}/previous" scrollRight="{base:s}/next"
                         scrollDown="{base:s}/volume_down" scrollUp="{base:s}/volume_up"
                         destroyOnExit="yes" allowAnswer="yes" allowDrop="yes" allowXfer="yes" allowConf="yes">
  <Title>Spotify Control</Title>
  <Text>{text:s}</Text>
  <SoftKey index="1"><Label>Previous</Label><URI>{base:s}/previous</URI></SoftKey>
  <SoftKey index="2"><Label>Pause</Label><URI>{base:s}/pause</URI></SoftKey>
  <SoftKey index="3"><Label>Play/Pause</Label><URI>{base:s}/playpause</URI></SoftKey>
  <SoftKey index="4"><Label>Play</Label><URI>{base:s}/play</URI></SoftKey>
  <SoftKey index="5"><Label>Next</Label><URI>{base:s}/next</URI></SoftKey>
  <SoftKey index="6"><Label>Stop</Label><URI>{base:s}/stop</URI></SoftKey>
</AastraIPPhoneTextScreen>
""".format(base=base, text=escape(text))

class SpotifyCtl(object):
  """Methods:
     u'org.mpris.MediaPlayer2.Player.OpenUri': u's',
     u'org.mpris.MediaPlayer2.Player.Pause': '',
     u'org.mpris.MediaPlayer2.Player.Previous': '',
     u'org.mpris.MediaPlayer2.Player.PlayPause': '',
     u'org.mpris.MediaPlayer2.Player.Stop': '',
     u'org.mpris.MediaPlayer2.Player.Next': '',
     u'org.mpris.MediaPlayer2.Player.Play': '',
     u'org.mpris.MediaPlayer2.Player.SetPosition':u'ox',
     u'org.mpris.MediaPlayer2.Player.Seek': u'x'
     u'org.mpris.MediaPlayer2.Quit': '',
  """
  def spotify_command(self, command, args=None):
    try:
      session = dbus.SessionBus.get_session()
      spotify = session.get_object("org.mpris.MediaPlayer2.spotify",
                                   "/org/mpris/MediaPlayer2")
      if(hasattr(spotify, command)):
        if args:
          getattr(spotify, command)(args)
        else:
          getattr(spotify, command)()
        return True
    except dbus.exceptions.DBusException as e:
      print "Warning: DBUS Error. Is Spotify running?\n%r" % e
      pass
    return False

  def spotify_getnowplaying(self):
    try:
      bus = dbus.SessionBus()
      player = bus.get_object('com.spotify.qt', '/')
      iface = dbus.Interface(player, 'org.freedesktop.MediaPlayer2')
      info = iface.GetMetadata()
      return str(info['xesam:artist'][0]) + " - " + str(info['xesam:title'])
    except:
      return ""

  @cherrypy.expose
  def index(self):
    np = self.spotify_getnowplaying()
    if not np:
      np = "Nothing playing."
    return aastra_xml(base=cherrypy.request.base, text=np)

  @cherrypy.expose
  @strongly_expire
  def previous(self):
    if self.spotify_command("Previous"):
      return aastra_xml(base=cherrypy.request.base, text="Skipped backwards. " + self.spotify_getnowplaying())
    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

  @cherrypy.expose
  @strongly_expire
  def pause(self):
    if self.spotify_command("Pause"):
      return aastra_xml(base=cherrypy.request.base, text="Paused. " + self.spotify_getnowplaying())
    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

  @cherrypy.expose
  @strongly_expire
  def playpause(self):
    if self.spotify_command("PlayPause"):
      return aastra_xml(base=cherrypy.request.base, text="Play/Pause toggled. " + self.spotify_getnowplaying())
    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

  @cherrypy.expose
  @strongly_expire
  def play(self):
    if self.spotify_command("Play"):
      return aastra_xml(base=cherrypy.request.base, text="Playing. " + self.spotify_getnowplaying())
    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

  @cherrypy.expose
  @strongly_expire
  def next(self):
    if self.spotify_command("Next"):
      return aastra_xml(base=cherrypy.request.base, text="Skipped forwards. " + self.spotify_getnowplaying())
    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

  @cherrypy.expose
  @strongly_expire
  def stop(self):
    if self.spotify_command("Stop"):
      return aastra_xml(base=cherrypy.request.base, text="Stopped. " + self.spotify_getnowplaying())
    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

  @cherrypy.expose
  @strongly_expire
  def quit(self):
    if self.spotify_command("Quit"):
      return aastra_xml(base=cherrypy.request.base, text="Quit. " + self.spotify_getnowplaying())
    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

  # Doesn't seem to work at all... But at least we don't 404
  @cherrypy.expose
  @strongly_expire
  def volume_up(self):
    return aastra_xml(base=cherrypy.request.base, text="Method not implemented. " + self.spotify_getnowplaying())
  @cherrypy.expose
  @strongly_expire
  def volume_down(self):
    return aastra_xml(base=cherrypy.request.base, text="Method not implemented. " + self.spotify_getnowplaying())

# Doesn't quite work, no exception but fails anyways.
#  @cherrypy.expose
#  def seek(self, seek):
#    if self.spotify_command("Player.SetPosition", args=seek):
#      return aastra_xml(base=cherrypy.request.base, text="Done. " + self.spotify_getnowplaying())
#    return aastra_xml(base=cherrypy.request.base, text="An error occurred. " + self.spotify_getnowplaying())

if __name__ == '__main__':
  import os
  current_dir = os.path.dirname(os.path.abspath(__file__))
  cherrypy.config.update({'server.socket_host': '::',
                          'server.socket_port': 8081,
                          'tools.caching.on': False})

  cherrypy.quickstart(SpotifyCtl(), '/')

