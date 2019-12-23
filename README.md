# OctoPrint-M73Progress

Most 3D printers offer a progress bar or percentage indicator on
their display. However, by default, this percentage is only updated when
printing from SD card. When printing directly through OctoPrint, the progress bar
remains empty. This small plugin remedies the situation by injecting
`M73 (set build percentage)` commands into the print stream.

**Note:** Not all printers support this feature. In order for this to work, your
firmware needs to understand the `M73` command. See below for instructions for
[Marlin](https://github.com/MarlinFirmware/Marlin).

![](pic.jpg)

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/cesarvandevelde/OctoPrint-M73Progress/archive/master.zip

### Marlin Firmware

You will need a recent version of Marlin, **1.1.7** or later. The `M73` feature is
not enabled by default. You can enable it by uncommenting line 576 in
`Configuration_adv.h`:

```C
// Add an 'M73' G-code to set the current percentage
#define LCD_SET_PROGRESS_MANUALLY
```

**Note:** The older Marlin versions (1.1.7 and 1.1.8) require that `SDSUPPORT` be enabled in order for
`LCD_SET_PROGRESS_MANUALLY` to work. See
[MarlinFirmware/Marlin#9178](https://github.com/MarlinFirmware/Marlin/issues/9178).

## Configuration

The plugin should work as-is. Once enabled, the plugin will automatically inject
M73 commands in the printer's serial stream. There are two options to fine-tune
the plugin's behavior, available through the `M73 Progress` tab in OctoPrint
settings.

* `Output time left`: Sends the estimated time remaining using the R parameter.
  This is only supported by certain firmwares (e.g. Marlin 2.0 and Prusa
  firmware). This option is enabled by default; most firmwares will just ignore
  this extra parameter if not supported.

* `Use time estimate`: By default, the plugin uses OctoPrint's built-in progress
  estimate, which is based on the progress inside a G-code file. In some cases,
  a better progress estimate can be calculated from the time elapsed and the
  time remaining: `P = elapsed / (elapsed + remaining)`. This option is
  particularly useful for
  [PrintTimeGenius](https://github.com/eyal0/OctoPrint-PrintTimeGenius) users.
