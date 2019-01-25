# (emacs/sublime) -*- mode: python; tab-width: 4; -st-draw_white_space: 'all'; -*-
from threading import Timer
import xbmc
import xbmcaddon
import os, sys

from utils import *

class PandaPlayer( xbmc.Player ):

	def __init__( self, core=None, panda=None ):
		log.debug( "PandaPlayer.__init__( CORE, PANDA )" )
		xbmc.Player.__init__( self )
		self.panda = panda
		self.timer = None
		self.playNextSong_delay = 0.5
		log.debug( "PandaPlayer.__init__ :: end" )

	def playSong( self, item ):
		log.debug( "PandaPlayer.playSong()" )
		log.debug( "PandaPlayer.playSong: item[url] %s" % item[0] )
		log.debug( "PandaPlayer.playSong: item[item] %s" % item[1] )
		self.play( item[0], item[1] )
		log.debug( "PandaPlayer.playSong() :: end" )

	def onPlayBackStarted( self ):
		try:
			log.debug( "PandaPlayer.onPlayBackStarted: %s" %self.getPlayingFile() )
		except:
			pass
		log.debug( "PandaPlayer.onPlayBackStarted :: end" )

	def onPlayBackEnded( self ):
		log.debug( "PandaPlayer.onPlayBackEnded()" )
		self.stop()
		log.debug( "playing = %s" %self.panda.playing )
		if self.timer and self.timer.isAlive():
			self.timer.cancel()
		if self.panda.skip:
			self.panda.skip = False
		if self.panda.playing:
			self.timer = Timer( self.playNextSong_delay, self.panda.playNextSong )
			self.timer.start()
		log.debug( "PandaPlayer.onPlayBackEnded() :: end" )

	def onPlayBackStopped( self ):
		log.debug( "PandaPlayer.onPlayBackStopped()" )
		self.stop()
		log.debug( "playing = %s" %self.panda.playing )
		if self.timer and self.timer.isAlive():
			self.timer.cancel()
		if self.panda.playing and self.panda.skip:
			self.panda.skip = False
			self.timer = Timer( self.playNextSong_delay, self.panda.playNextSong )
			self.timer.start()
		else:
			if xbmc.getCondVisibility('Skin.HasSetting(PandoraVis)'):
				# show UI
				xbmc.executebuiltin('Skin.Reset(PandoraVis)')
			self.panda.stop()
		log.debug( "PandaPlayer.onPlayBackStopped() :: end" )
