# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin


class M73progressPlugin(octoprint.plugin.StartupPlugin,
                        octoprint.plugin.ProgressPlugin,
                        octoprint.plugin.EventHandlerPlugin):

    def on_after_startup(self):
        self._logger.info("Hello World from M73 blah blah!")

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
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
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


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "M73 Progress Plugin"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = M73progressPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
