# Screen Curtain
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited
# Additional: copyright 2018 Babbage B.V., Joseph Lee, released under GPL

# Proof of concept of NVDA Core issue 7857 (screen curtain functionality)
# Note: this is a field test of a pull request being developed by Babbage. Permission was obtained to package this into an add-on.
# This add-on requires Windows 8 and later.

"""Screen curtain implementation based on the windows magnification API."""

import globalPluginHandler
try:
	from . import winMagnification
except:
	raise RuntimeError("Magnification attribute missing")
from ctypes import byref
import winVersion
import gui
import wx
from globalCommands import SCRCAT_TOOLS
import config
import ui

TRANSFORM_BLACK = winMagnification.MAGCOLOREFFECT()
TRANSFORM_BLACK.transform[4][4] = 1.0
TRANSFORM_DEFAULT = winMagnification.MAGCOLOREFFECT()
TRANSFORM_DEFAULT.transform[0][0] = 1.0
TRANSFORM_DEFAULT.transform[1][1] = 1.0
TRANSFORM_DEFAULT.transform[2][2] = 1.0
TRANSFORM_DEFAULT.transform[3][3] = 1.0
TRANSFORM_DEFAULT.transform[4][4] = 1.0

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	_screenCurtainActive = False
	
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if (winVersion.winVersion.major, winVersion.winVersion.minor) < (6, 2):
			raise RuntimeError("This add-on is only supported on Windows 8 and above")
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		# Translators: The label for the menu item to toggle screen curtain.
		self.toggleScreenCurtain = self.toolsMenu.AppendCheckItem(wx.ID_ANY, _("Screen curtain"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onToggleScreenCurtain, self.toggleScreenCurtain)
		if config.conf["screenCurtain"]["startup"]:
			winMagnification.Initialize()
			winMagnification.SetFullscreenColorEffect(byref(TRANSFORM_BLACK))
			import tones
			tones.beep(1024, 100)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(ScreenCurtainPanel)


	def terminate(self):
		super(GlobalPlugin, self).terminate()
		winMagnification.SetFullscreenColorEffect(byref(TRANSFORM_BLACK))
		winMagnification.Uninitialize()
		self._screenCurtainActive = False
		try:
			if wx.version().startswith("4"):
				self.toolsMenu.Remove(self.toggleScreenCurtain)
			else:
				self.toolsMenu.RemoveItem(self.toggleScreenCurtain)
		except: #(RuntimeError, AttributeError, wx.PyDeadObjectError):
			pass

	# The following functions came from NVDA Core's speech viewer toggle mechanics.

	def onToggleScreenCurtain(self, evt):
		if not self._screenCurtainActive:
			winMagnification.Initialize()
			winMagnification.SetFullscreenColorEffect(byref(TRANSFORM_BLACK))
			self._screenCurtainActive = True
			wx.CallLater(1000, ui.message, _("Screen curtain on"))
		else:
			winMagnification.SetFullscreenColorEffect(byref(TRANSFORM_BLACK))
			winMagnification.Uninitialize()
			self._screenCurtainActive = False
			wx.CallLater(1000, ui.message, _("Screen curtain off"))
		self.toggleScreenCurtain.Check(self._screenCurtainActive)
		config.conf["screenCurtain"]["active"] = self._screenCurtainActive

	def script_toggleScreenCurtain(self, gesture):
		self.onToggleScreenCurtain(None)
	script_toggleScreenCurtain.__doc__ = _("Toggles screen curtain on or off")
	script_toggleScreenCurtain.category = SCRCAT_TOOLS

# Add-on config database
confspec = {
	"active": "boolean(default=false)",
	"startup": "boolean(default=false)",
}
config.conf.spec["screenCurtain"] = confspec

class ScreenCurtainPanel(gui.SettingsPanel):
	# Translators: This is the label for the Screen curtain settings panel.
	title = _("Screen curtain")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.screenCurtainActiveCheckBox=sHelper.addItem(wx.CheckBox(self, label=_("Use &screen curtain")))
		self.screenCurtainActiveCheckBox.SetValue(config.conf["screenCurtain"]["active"])
		# Startup flag can be toggled if and only if normal configuration is in use.
		if config.conf.profiles[-1].name is None:
			self.screenCurtainStartupCheckBox=sHelper.addItem(wx.CheckBox(self, label=_("Enable screen curtain at startup")))
			self.screenCurtainStartupCheckBox.SetValue(config.conf["screenCurtain"]["startup"])

	def onSave(self):
		if config.conf.profiles[-1].name is None:
			config.conf["screenCurtain"]["startup"]=self.screenCurtainStartupCheckBox.IsChecked()
		config.conf["screenCurtain"]["active"] = self.screenCurtainActiveCheckBox.IsChecked()
