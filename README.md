# OctoPrint-M73Progress

Most 3D printers offer a progress bar or percentage indicator on
their display. However, by default, this percentage is only updated when
printing from SD card. When printing directly through OctoPrint, the progress bar
remains empty. This small plugin remedies the situation by injecting
`M73 (set build percentage)` commands into the print stream.

**Note:** Not all printers support this feature. In order for this to work, your
firmware needs to understand the `M73` command. See below for instructions for
[Marlin](https://github.com/MarlinFirmware/Marlin).

**TODO:** Picture

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

## Configuration

This plugin has no configurable options. Once enabled, it will automatically
inject M73 commands in the printer's serial stream.
