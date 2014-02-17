#!/usr/bin/env python2
# vim: et sw=2 ts=2
import cherrypy
import dbus
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
</ul>
</body>
</html>
"""

  @cherrypy.expose
  def previous(self):
    if self.spotify_command("Previous"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  def pause(self):
    if self.spotify_command("Pause"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  def playpause(self):
    if self.spotify_command("PlayPause"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  def play(self):
    if self.spotify_command("Play"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  def next(self):
    if self.spotify_command("Next"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  def stop(self):
    if self.spotify_command("Stop"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

  @cherrypy.expose
  def quit(self):
    if self.spotify_command("Quit"):
      return 'Done. <a href="/">Back</a>'
    return "An error occurred."

# Doesn't quite work, no exception but fails anyways.
#  @cherrypy.expose
#  def seek(self, seek):
#    if self.spotify_command("Player.SetPosition", args=seek):
#      return 'Done. <a href="/">Back</a>'
#    return "An error occurred."

if __name__ == '__main__':
  cherrypy.config.update({'server.socket_port': 8081})
  cherrypy.quickstart(SpotifyCtl())

