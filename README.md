# Central Command

One small tray panel for the whole PC: black the screens and lights out, run the fans from the water temperature, and hold the GPU overclock with no tuning app running.

<p>
<img src="docs/panel-main.png" width="280" alt="Central Command panel">
<img src="docs/panel-settings.png" width="280" alt="Fan curve settings">
</p>
<p>
<img src="docs/panel-wake.png" width="280" alt="Wake settings">
<img src="docs/panel-system.png" width="280" alt="System and status">
<img src="docs/panel-gpu.png" width="280" alt="GPU tab: profile and XBAR offset">
</p>

## Who it is for

Someone with a water-cooled, overclocked Windows desktop who wants one quiet tool in the tray instead of a fan app, an RGB app and a GPU tuning app left running. It is built for one such PC and is run there every day. It is published as it is: every part is optional and skips itself when its hardware is missing, but only the hardware in [Supported hardware](#supported-hardware) marked verified has been run.

## Central Command and Blackout

Central Command grew out of [Blackout](https://github.com/Xipzer/blackout-tray), a small tray tool that turns every screen off with one click. Blackout kept growing (fans, GPU) until it was no longer small, so it was split:

- **Blackout** is the small public tool again. It only blacks a PC out. If that is all you want, use it.
- **Central Command** is everything Blackout could do before the split, under its own name: screens and lights off, the wake rules, the fan curve with its device definitions, and the GPU profiles.

Run one or the other, not both: each would switch the screens and the lighting. Moving over from Blackout is described under [Coming from Blackout](#coming-from-blackout).

## What it does

**Screens and lights.** Left-click the tray icon and every screen turns off. Lighting, fans, monitor power and window positions follow the screens, for a click and for Windows' own display timeout:

| Screens off | Screens on |
|---|---|
| RGB off | RGB back on |
| Fans to the "screens off" speed | Fans to the "screens on" speed |
| Listed monitors powered off over DDC/CI | Those monitors powered on |
| Window positions saved | Windows put back where they were |

**Cooling.** One temperature, usually the water, drives up to 7 fans along a curve you draw in the panel ([Fan curve](#fan-curve)).

**GPU.** Overclock profiles for an NVIDIA card are written straight to the driver, and sent again after a restart or a driver reset ([GPU profiles](#gpu-profiles-optional)).

**Right-click** the tray icon for the panel. It sits flush against the taskbar and the screen edge like the system tray menus, and takes its colour from your taskbar.

- **Main:** Screens off, RGB lighting, RGB off with the screens. With a fan curve: the temperature, fan speed, a 15 minute graph, RPM per fan, the switch that makes the fans follow the temperature and the override at a fixed speed. With GPU profiles: the profile on the card, a dot that is green when the driver took it, and the XBAR offset.
- **Settings > Fans:** the fan curve (drag a point, double-click to add one, right-click to remove one), max fan speed, how much cooler it must get before the fans slow down, reset.
- **Settings > Wake:** which inputs may wake the screens, and what woke them last, with the device behind it.
- **Settings > GPU:** overclock profiles for an NVIDIA card: the clock curve as a chart, power limit, memory offset, XBAR offset.
- **Settings > System:** Start with Windows, Exit, and what Central Command found on this PC, with its version.

Esc goes back or closes the panel, the arrow keys change tabs. If Direct2D is unavailable, a plain menu appears instead. Hover the tray icon for the temperature, the fan speed and the GPU profile.

RGB set to off stays off: waking the screens only brings the lighting back if the RGB switch is on.

## Supported hardware

| Feature | Hardware | Needs |
|---|---|---|
| RGB | Anything [OpenRGB](https://openrgb.org) supports | OpenRGB portable |
| Pump/fan RGB | Corsair iCUE LINK System Hub (XD5, QX, LX...) | Nothing |
| RAM RGB | Kingston FURY DDR5 | FURY module + Kingston FURY CTRL |
| Fan speed | Corsair Commander Pro | Nothing |
| Fan curve | Motherboard fan headers and USB fan controllers, from the files in [`devices`](devices) | For motherboard headers: PawnIO, `LpcIO.bin`, run as admin |
| GPU profiles | NVIDIA cards (tested on an RTX 5090 FE) | NVIDIA driver, run as admin |
| Monitor power | Any monitor with DDC/CI | Nothing |

Every feature is optional. Missing hardware is skipped.

## Setup

1. Get `central-command.exe` from [Releases](https://github.com/Xipzer/central-command/releases) or build it (see [Build](#build)), and put it in a folder, for example `%LOCALAPPDATA%\CentralCommand`. Keep the `devices` folder beside it if you use the fan curve.
2. Copy `central-command.example.ini` there as `central-command.ini` and edit it. No ini means screens off and fans only.
3. Run `central-command.exe`. Right-click the icon, open Settings > System and switch on **Start with Windows**.

For RGB, also unzip [OpenRGB](https://openrgb.org/releases.html) portable to the path in `central-command.ini`.
For the fan curve and the GPU profiles, run it as admin: see the two sections below.

### Coming from Blackout

1. In Blackout, switch **Start with Windows** off, then exit it.
2. Copy `blackout.ini` into the Central Command folder as `central-command.ini`. The sections and keys are the same, so the fan setup and the GPU profiles come along. Copy `LpcIO.bin`, `furyled.exe` and the `devices` folder too if you use them.
3. Start `central-command.exe` (as admin if it drives fans or the GPU) and switch **Start with Windows** on.

The first time it starts, Central Command copies Blackout's settings from `HKCU\Software\Blackout` to its own `HKCU\Software\CentralCommand`, once: the edited fan curve, the override, the active GPU profile, the XBAR offset and the wake rules are all as you left them. After that the two keys are separate.

## Fan curve

One temperature drives up to 7 fans along a curve you draw in the panel. The usual setup is a water loop: the coolant sensor on an iCUE LINK hub sets the speed of radiator fans on motherboard headers.

1. For motherboard headers, install [PawnIO](https://pawnio.eu) and put `LpcIO.bin` (from PawnIO.Modules or OpenRGB) beside `central-command.exe`.
2. Run `central-command.exe --devices` as admin. It lists the fans and temperatures it can see.
3. Add `[fans]` to `central-command.ini` with `outputs=` and, unless you use the iCUE LINK coolant sensor, `source=`.
4. Run Central Command as admin and switch **Start with Windows** on. As admin this creates a logon task, so there is no UAC prompt at login.

Edit the curve in the panel (Settings > Fans): drag a point, double-click the chart to add one, right-click a point to remove it, and set **Max fan speed** and **Slow down once cooler by**. Changes apply at once and are kept in `HKCU\Software\CentralCommand` (`Curve`, `FanMax`, `Hysteresis`), which override the ini. **Reset to central-command.ini** drops them.

**Override at a fixed speed** (panel main view, or the tray menu) runs the fans at one fixed speed, 20 to 100%, instead of the curve. **Fixed speed** under it sets that speed, also before the override is switched on. It pauses while the temperature is above the point where the curve reaches its top, and comes back once it is 2 C below that.

Fans go up straight away and come down after the hysteresis. Motherboard fans go back to the BIOS curve when the temperature reading is lost for 20 s, on exit, sleep and shutdown, and when the curve is switched off. Set a sensible fixed speed or curve in the BIOS: it is what runs whenever Central Command does not.

### Hardware

Each fan chip or controller is described by a text file in [`devices`](devices). [docs/devices.md](docs/devices.md) explains the format and how to add one.

| Hardware | Files | Fan control |
|---|---|---|
| Nuvoton NCT6779D, NCT6791D to NCT6799D | 10 | Yes. NCT6796D-R is verified, the rest are untested |
| ITE IT8603E to IT8698E, IT8728F, IT8792E, IT87952E | 15 | Yes, untested |
| ITE IT8790E, Fintek F718xx and F818xx, Nuvoton NCT6683D to NCT6687D | 20 | Speeds and temperatures only |
| Corsair Commander Pro | 1 | Yes, untested |
| NZXT Kraken X42 to X72, Aquacomputer D5 Next, Quadro, Octo, Farbwerk | 6 | Speeds and temperatures only |

Untested means the file was written from other open source drivers and has not been run on that hardware. Central Command will not control fans through it until you set `untested=1`. If it works for you, a pull request that marks it verified helps the next person.

An older ini with `channels=1,3,4` keeps working: it means `outputs=sio/2,sio/4,sio/5`.

## Choosing what wakes the screens

A bumped mouse or a vibrating desk can wake the screens in the middle of the night. With **Wake the screens only with** switched on (panel > Settings > Wake), only the chosen inputs wake them while they are off:

- **Left-click** and/or **Esc** (at least one stays on)
- Mouse movement, other buttons and other keys are ignored, and don't reach any app
- **Ctrl+Alt+Del** always works

It applies whenever the screens go off, from Central Command or from Windows' own display timeout. Nothing runs for it while the screens are on.

The same tab lists the last few wakes and the device behind each one (for example a mouse icon and `PRO X SUPERLIGHT`), whether that switch is on or not. A device that got past it is marked `not blocked`. Use the list to find a device that keeps waking the screens.

## Configuration

`central-command.ini` sits beside `central-command.exe`. See [central-command.example.ini](central-command.example.ini).

| Section | Key | Meaning |
|---|---|---|
| `[rgb]` | `openrgb` | Path to `OpenRGB.exe`. Empty skips OpenRGB. |
| | `off`, `on` | OpenRGB arguments for each state |
| | `off2`..`off4`, `on2`..`on4` | Extra steps. Use for devices that are sometimes missing (wireless, speakers). |
| | `color` | Hex colour for the iCUE LINK hub and RAM when on |
| `[link]` | `leds` | LED count on the iCUE LINK chain. 0 disables it. |
| `[ddc]` | `monitors` | Monitor hardware IDs to power off, comma separated (e.g. `BNQ7F2F`) |
| `[fans]` | `outputs` | Fans to drive, e.g. `sio/2,sio/4` (see [Fan curve](#fan-curve)) |
| | `source` | Temperature to follow: `link` (default) or e.g. `sio/AUXTIN2` |
| | `untested` | `1` allows control through a definition marked untested |
| | `max` | Cap on every duty in % (default 100) |
| | `names` | Panel labels for the fans, in the order of `outputs`, e.g. `Top,Side,Bottom` |
| | `curve` | `C:duty` points, e.g. `30:40,45:100` |
| | `hysteresis` | C the temperature must drop before fans slow down (default 2) |
| `[gpu]` | `cap_cold`, `cap_warm` | Optional NVIDIA clock cap in MHz that follows the coolant (see below). Both 0 (default) = off |
| | `cold_below`, `warm_above` | Coolant C: the cold cap applies below `cold_below` (default 30), the warm cap above `warm_above` (default 32) |
| | `xbar`, `xbar_default` | XBAR offsets in MHz for the GPU tab's stepper (e.g. `0,300,400,500`), and the one used until another is picked |
| `[gpu.1]` to `[gpu.5]` | `name`, `power`, `memory`, `curve` | GPU profiles applied natively, written by **Read from card** on the GPU tab (see [docs/gpu.md](docs/gpu.md)) |

Switches and fan speeds are kept in `HKCU\Software\CentralCommand`.

To find a monitor's hardware ID: Device Manager > Monitors > Properties > Details > Hardware Ids.

## GPU profiles (optional)

For an overclocked NVIDIA card. Central Command holds the overclock itself and writes it straight to the driver, so no tuning app has to run: a clock curve, a power limit and a memory offset per profile, plus the XBAR (crossbar clock) offset.
The driver forgets all of it when it resets or the PC restarts, so Central Command sends it again after startup and after a driver reset.

On a PC with an NVIDIA driver the panel's Settings have a **GPU** tab:

- **Profiles** along the top. Clicking one only shows it: its clock curve over the card's own curve (the grey line), the top of the curve with the lowest voltage that reaches it, the power limit in % and the memory offset in MHz. **Apply** sends it. Red marks the profile that is on the card.
- **Read from card** keeps what the card is running now as the profile on show, so an overclock you have tuned and tested in any app becomes a Central Command profile with one click. **+** is the next empty profile. A profile that exists asks before it is replaced.
- Click a profile's name to change it.
- **XBAR offset**: its minus and plus step through the `xbar` values from `central-command.ini`. Sent a moment after the last step. It is a row of its own because it belongs to the card, not to a profile.
- The line at the bottom says what the driver answered. On the Main view the dot beside the profile is green when it was applied, and the tray tooltip names the profile.

Nothing is read from the card while the panel is open; **Read from card** reads it once.
It uses private driver interfaces and is tested on one card (RTX 5090 FE, driver 621.24). Read [docs/gpu.md](docs/gpu.md) first: setup, limits, the layouts and their sources.

## GPU clock cap (optional)

For an overclocked NVIDIA card on the same water loop. A cold GPU core gets extra boost bins from the driver, and an overclocked curve may not survive them.
With `[gpu] cap_cold` and `cap_warm` set, Central Command sends `nvidia-smi -lgc 210,<cap>` when the coolant crosses the thresholds, and again every minute, because a driver reset drops the cap.
It needs Central Command to run as admin. Leave both at 0 if you do not need it.

## FURY module (optional)

For Kingston FURY DDR5 RGB only. OpenRGB can't detect some of these kits, so this talks to Kingston's own service instead.

1. Install Kingston FURY CTRL. Its background service does the hardware access.
2. Put `furyled.exe` beside `central-command.exe`. Delete it to turn the module off.

Test it: `furyled off` or `furyled FF0000`.

## For scripts

Other programs can read what Central Command knows and tell it what to do. Nothing here needs a helper to be running.

| What | Where |
|---|---|
| Water (or source) temperature | `HKCU\Software\CentralCommand`, DWORD `Coolant`, C x10, averaged over about 30 s. Written only when it changes |
| Fan speed being driven | Same key, DWORD `FanDuty`, %. 0 = the BIOS has the fans |
| Clock cap last sent | Same key, DWORD `GpuCap`, MHz (only with `[gpu] cap_cold`, `cap_warm`) |
| Override | Same key, DWORDs `Override` (0 or 1) and `OverrideDuty` (%), read at startup |
| Commands | Post `WM_COMMAND` to the window of class `CentralCommand`: 1 screens off, 2 RGB on/off, 5 exit, 9 write the device report, 10 override on/off, 11 send the GPU profile again |
| Start it elevated with no UAC prompt | `schtasks /Run /TN CentralCommand` (the task **Start with Windows** makes when run as admin) |

The value names, units and command numbers are the ones Blackout used; only the key, the window class and the task name changed.

## Resource use

Measured on Windows 11. The panel figures are from this build (`central-command.exe --panel-bench`, three runs); the others were measured on the same code while it was still called Blackout.

| Process | When | Memory | CPU |
|---|---|---|---|
| `central-command.exe` (195 KB) | Always | 0.2 to 0.4 MB | 0% idle |
| iCUE LINK keep-alive | Every 4 s, only with `[link]` | 5 small USB transfers | ~0% |
| Fan curve | Same 4 s tick, only with `[fans]` | One temperature read; fan write only when the duty changes. Only the definitions in use are kept, about 2 KB each | ~0% |
| Panel | Only while open | Opens in 10 to 20 ms, 17 to 22 MB while open, back to 0.6 MB when closed. Drawn on the CPU, so no graphics driver is loaded | Brief |
| `OpenRGB.exe` | 3 to 5 s per change, then exits | ~100 MB while running | Brief |
| `furyled.exe` | Under 1 s per change | ~10 MB while running | Brief |
| Kingston FURY CTRL service | Always, if installed | ~40 MB | Kingston's |

## Setup notes

- **OpenRGB with Corsair Commander Pro or Lighting Node Pro:** set each channel's LED count once in OpenRGB (Zone Initialization). Static mode won't light a zone of size 0.
- **OpenRGB with an iCUE LINK hub:** disable OpenRGB's "Corsair iCUE Link System Hub" detector. Central Command drives the hub itself.
- **Screens off** briefly sets the Windows display timeout to 1 second, then restores your value.
- **Tray icon:** white on a dark taskbar, dark on a light one. It follows the Windows mode setting.

## Quirks and remedies

Things we hit running it every day on a water-cooled desktop (ASRock Z790 board with a Nuvoton NCT6796D, Corsair iCUE LINK hub, four monitors). Each one is either handled in the app or needs a setting from you.

| Quirk | What you see | Remedy |
|---|---|---|
| Fans go to the BIOS curve whenever Central Command is not driving them | A loud burst at exit, restart, sleep and shutdown | Set a sensible fixed speed or curve in the BIOS: it runs whenever Central Command does not |
| Restarting Central Command | Fans loud for a few seconds; the LINK hub shows its stored hardware colour until Central Command takes it over | Expected. Avoid restarting it while you want the room dark |
| HWiNFO (or another monitor) starts while Central Command drives the fans | Board fans at about 3,000 rpm for about 45 s while HWiNFO probes the Super I/O chip | Expected; Central Command shares the standard ISA bus mutex, and takes the fans back afterwards. Public reports of the same clash with other fan tools: [HWiNFO forum](https://www.hwinfo.com/forum/threads/hwinfo64-taking-over-fancontrol-sensor-settings.8390/), [r/FanControl](https://www.reddit.com/r/FanControl/comments/1goa24j/fan_control_borked_by_hwinfo/) |
| Another program (HWiNFO, iCUE) has the LINK hub open too | Coolant reading lost; the other program's replies were read | Fixed: Windows gives every open HID handle a copy of each input report ([Microsoft](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_flushqueue), [OSR](https://community.osr.com/t/theory-buffering-in-hid-class-driver/30591)), so Central Command flushes the queue before each exchange and reopens the handle on a reply that does not match |
| Three programs polling one LINK hub | The hub crashed once | Let one program own the hub. In OpenRGB, disable its iCUE LINK detector |
| Two fan chains on one 1 A header | A chain of three 120 mm fans draws about 0.9 to 1.3 A at 100% | Cap `max=` (we run 80%) until the fans have a powered hub |
| The legacy monitor-off broadcast | A monitor on the motherboard's iGPU came straight back; some iGPU DisplayPort outputs stayed half awake ("No Signal" flashes) | Central Command sets the display timeout to 1 s instead; list such monitors in `[ddc] monitors=` so they are powered off over DDC/CI. Best: run every monitor from the graphics card |
| Kingston FURY RGB not seen by OpenRGB | RAM stays lit | Use the FURY module. Keep Kingston FURY CTRL installed: it is also what blanks the DIMM lighting on sleep |
| A bumped mouse wakes the screens at night | | Settings > Wake: **Wake the screens only with** a left-click or Esc |
| Run key and logon task both present | Whichever starts first holds the single-instance lock. If that is the non-admin Run-key copy, there is no fan control | Use one: as admin, **Start with Windows** makes the logon task |
| Blackout and Central Command both running | Screens and lighting are switched twice | Run one of them |
| A GPU driver reset | The profile, the XBAR offset and a clock cap set with `nvidia-smi -lgc` are gone | The profile and XBAR are sent again 15 s after the reset; the `[gpu]` cap is re-sent every minute |

## Build

Needs [zig](https://ziglang.org) and Python 3 with Pillow.

```sh
./build.sh            # checks devices/ on simulated hardware, then builds build/central-command.exe
```

FURY module, on Windows: `modules\fury\build.cmd`.

## License

[PolyForm Noncommercial 1.0.0](LICENSE.md). Free to use, change and share. Not for sale.

## Credits

Protocol details from [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB) (iCUE LINK) and [liquidctl](https://github.com/liquidctl/liquidctl) (Commander Pro). Device definitions are written from the Linux hwmon drivers, [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) and liquidctl. Port access is through [PawnIO](https://pawnio.eu). Central Command grew out of [Blackout](https://github.com/Xipzer/blackout-tray).
