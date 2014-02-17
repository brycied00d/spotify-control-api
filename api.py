#!/usr/bin/env python2
# vim: et sw=2 ts=2
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
    return """
<html>
<head><title>Spotify Control</title></head>
<body>
<h1>Spotify Control</h1>
<ul>
<li><a href="/previous">Previous</a></li>
<li><a href="/pause">Pause</a></li>
<li><a href="/playpause">Play/Pause</a></li>
<li><a href="/play">Play</a></li>
<li><a href="/next">Next</a></li>
<li><a href="/stop">Stop</a></li>
<li><a href="/quit">Quit</a></li>
<li><hr></li>
<li><a href="/nowplaying">Now Playing</a></li>
</ul>
</body>
</html>
"""

  @cherrypy.expose
  @strongly_expire
  def previous(self):
    if self.spotify_command("Previous"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  @strongly_expire
  def pause(self):
    if self.spotify_command("Pause"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  @strongly_expire
  def playpause(self):
    if self.spotify_command("PlayPause"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  @strongly_expire
  def play(self):
    if self.spotify_command("Play"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  @strongly_expire
  def next(self):
    if self.spotify_command("Next"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  @strongly_expire
  def stop(self):
    if self.spotify_command("Stop"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  @strongly_expire
  def quit(self):
    if self.spotify_command("Quit"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  @strongly_expire
  def nowplaying(self, linkback="true"):
    print linkback
    np = self.spotify_getnowplaying()
    if str2bool(linkback) and np:
      np = np + "\n<br>" + 'Done. <a href="/">Back</a>'
    if np:
      return np
    return "An error occurred."

# Doesn't quite work, no exception but fails anyways.
#  @cherrypy.expose
#  def seek(self, seek):
#    if self.spotify_command("Player.SetPosition", args=seek):
#      return 'Done. <a href="/">Back</a>'
#    return "An error occurred."

if __name__ == '__main__':
  cherrypy.config.update({'server.socket_port': 8081,
                          'tools.caching.on': False})
  cherrypy.quickstart(SpotifyCtl())

