# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin


class M73progressPlugin(octoprint.plugin.ProgressPlugin,
                        octoprint.plugin.EventHandlerPlugin):

    def on_event(self, event, payload):
        if event == octoprint.events.Events.PRINT_STARTED:
            self._set_progress(0)
        elif event == octoprint.events.Events.PRINT_DONE:
            self._set_progress(100)

    def on_print_progress(self, storage, path, progress):
        if not self._printer.is_printing():
            return
        self._set_progress(progress)

    def _set_progress(self, progress):
        # TODO: only for local prints, not SD!
        self._printer.commands("M73 P{}".format(progress))

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
