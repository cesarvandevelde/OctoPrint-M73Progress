# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from octoprint.events import Events


class M73progressPlugin(octoprint.plugin.ProgressPlugin,
                        octoprint.plugin.EventHandlerPlugin):

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED or event == Events.PRINT_DONE:
            # Firmware manages progress bar when printing from SD card
            if payload.get("origin", "") == "sdcard":
                return

        if event == Events.PRINT_STARTED:
            self._set_progress(0,0)
        elif event == Events.PRINT_DONE:
            self._set_progress(100)

    def on_print_progress(self, storage, path, progress):
        if not self._printer.is_printing():
            return

        # Firmware manages progress bar when printing from SD card
        if storage == "sdcard":
            return

	time = -1
	try:
		currentData = self._printer.get_current_data()
		time = currentData["progress"]["printTime"]
	except Exception as e:
		self._logger.info("Caught an exception {0}\nTraceback:{1}".format(e,traceback.format_exc()))
		
        self._set_progress(progress, time)

    def _set_progress(self, progress, time=-1):
		if time == -1:
			self._printer.commands("M73 P{}".format(progress))
		else:
			self._printer.commands("M73 P{0} T{1}".format(progress, time))

    def get_update_information(self):
        return dict(
            m73progress=dict(
                displayName="M73 Progress Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="cesarvandevelde",
                repo="OctoPrint-M73Progress",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/cesarvandevelde/OctoPrint-M73Progress/archive/{target_version}.zip"
            )
        )


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = M73progressPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config":
            __plugin_implementation__.get_update_information
    }
