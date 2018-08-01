# screenCurtain/installTasks.py
# Copyright 2018 Joseph Lee, released under GPL.

# Provides needed routines during add-on installation and removal.
# Mostly checks compatibility.
# Routines are partly based on other add-ons, particularly Place Markers by Noelia Martinez (thanks add-on authors).

import sys
import gui
import wx
import addonHandler
addonHandler.initTranslation()

def onInstall():
	if sys.getwindowsversion().build < 9200:
		wx.CallAfter(gui.messageBox, _("You are using an older version of Windows. This add-on requires Windows 8 or later."), _("Incompatible Windows version"), wx.OK | wx.CENTER | wx.ICON_ERROR)
		raise RuntimeError("Old Windows version detected")
