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

TRANSFORM_BLACK = winMagnification.MAGCOLOREFFECT()
TRANSFORM_BLACK.transform[4][4] = 1.0
TRANSFORM_DEFAULT = winMagnification.MAGCOLOREFFECT()
TRANSFORM_DEFAULT.transform[0][0] = 1.0
TRANSFORM_DEFAULT.transform[1][1] = 1.0
TRANSFORM_DEFAULT.transform[2][2] = 1.0
TRANSFORM_DEFAULT.transform[3][3] = 1.0
TRANSFORM_DEFAULT.transform[4][4] = 1.0

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if (winVersion.winVersion.major, winVersion.winVersion.minor) < (6, 2):
			raise RuntimeError("This add-on is only supported on Windows 8 and above")
		winMagnification.Initialize()
		winMagnification.SetFullscreenColorEffect(byref(TRANSFORM_BLACK))

	def terminate(self):
		winMagnification.SetFullscreenColorEffect(byref(TRANSFORM_BLACK))
		winMagnification.Uninitialize()
