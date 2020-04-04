# coding=utf-8
from __future__ import absolute_import, division

import logging

import octoprint.plugin
from octoprint.events import Events
from octoprint.printer import PrinterCallback
from flask_babel import gettext


logger = logging.getLogger(__name__)


class ProgressMonitor(PrinterCallback):
    def __init__(self, *args, **kwargs):
        super(ProgressMonitor, self).__init__(*args, **kwargs)
        self.reset()

    def reset(self):
        self.completion = None
        self.time_elapsed_s = None
        self.time_left_s = None

    def on_printer_send_current_data(self, data):
        self.completion = data["progress"]["completion"]
        self.time_elapsed_s = data["progress"]["printTime"]
        self.time_left_s = data["progress"]["printTimeLeft"]


class M73progressPlugin(
    octoprint.plugin.ProgressPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.RestartNeedingPlugin
):
    def on_after_startup(self):
        self._progress = ProgressMonitor()
        self._printer.register_callback(self._progress)

        settings = self._settings
        self.output_time_left = settings.get_boolean(["output_time_left"])
        self.progress_from_time = settings.get_boolean(["progress_from_time"])

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED or event == Events.PRINT_DONE:
            # Firmware manages progress bar when printing from SD card
            if payload.get("origin", "") == "sdcard":
                return

        if event == Events.PRINT_STARTED:
            self._progress.reset()
            self._set_progress(0)
        elif event == Events.PRINT_DONE:
            self._set_progress(100, 0)

    def on_print_progress(self, storage, path, progress):
        if not self._printer.is_printing():
            return

        # Firmware manages progress bar when printing from SD card
        if storage == "sdcard":
            return

        progress = 0.0
        time_left = None

        if self.output_time_left and self._progress.time_left_s is not None:
            # M73 expects time left value in minutes, not seconds
            time_left = self._progress.time_left_s / 60

        if (
            self.progress_from_time and
            self._progress.time_left_s is not None and
            self._progress.time_elapsed_s is not None
        ):
            time_left_s = self._progress.time_left_s
            time_elapsed_s = self._progress.time_elapsed_s
            progress = time_elapsed_s / (time_left_s + time_elapsed_s)
            progress = progress * 100.0
        else:
            progress = self._progress.completion or 0.0

        self._set_progress(progress=progress, time_left=time_left)

    def _set_progress(self, progress, time_left=None):
        if time_left is None:
            gcode = "M73 P{:.0f}".format(progress)
        else:
            gcode = "M73 P{:.0f} R{:.0f}".format(progress, time_left)

        self._printer.commands(gcode)

    def get_settings_defaults(self):
        return dict(
            output_time_left=True,
            progress_from_time=False
        )

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        settings = self._settings
        self.output_time_left = settings.get_boolean(["output_time_left"])
        self.progress_from_time = settings.get_boolean(["progress_from_time"])

    def get_template_configs(self):
        return [
            dict(
                type="settings",
                name=gettext("M73 Progress"),
                custom_bindings=False
            )
        ]

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


__plugin_name__ = "M73 Progress Plugin"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = M73progressPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config":
            __plugin_implementation__.get_update_information
    }
