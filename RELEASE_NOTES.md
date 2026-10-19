# OctoKlipper 0.5.0 rc1

This release candidate collects everything since **0.4** into one release: the
**0.4 foundation** (OctoPrint 2.0 compatibility while staying backward compatible
with 1.11.x, the Monaco config editor with syntax linter, the live klippy.log
tail, reworked backup/restore, sudo handling and the settings UI) plus the new
**printer.cfg macros with groups**, the **Setup Wizard**, **Save Variables**, and
the editor tooling.

## ✨ New

- **Parsed printer.cfg macros** — gcode macros are parsed out of `printer.cfg` and its `[include]`d files (recursively, with cycle protection) and shown as clickable buttons.
- **Macro groups** — create, rename, reorder and delete groups; control display order (empty = alphabetical); groups are collapsible and the state is remembered across reloads.
- **Dedicated macro panels** — "Macros" and "Klipper Macros" sidebar panels below the connection panel, plus a "Klipper Macros" settings tab to assign each macro to a group and choose where it is shown. Each panel can be shown or hidden independently.
- **Macro runtime parameters** — macros using `{params.X}`, `{rawparams.X}` or `{input.X}` open a parameter dialog and are sent as `MACRONAME X=value` arguments. Macro buttons also work while disconnected (the command is logged and a hint is shown).
- **Setup Wizard** — a step-by-step diagnostic dialog (**Settings → OctoKlipper → Basic → Run Setup Wizard**) that checks the Klipper install path and service, the config tree and required sections, the virtual serial port, and OctoPrint's error-handling setting, with one-click fixes where safe. See [docs/setup-wizard.md](docs/setup-wizard.md).
- **Save Variables** — a dialog (**Klipper tab → Tools**) that reads the `[save_variables]` file, shows the current values, highlights which parsed macros use each variable, and updates values via `SAVE_VARIABLE` gcode.
- **Create file** — a **Create file…** button in the config editor creates an empty config file in the open folder; a missing extension gets `.cfg` appended.
- **Config path checks** — **Check path** buttons and resolved-path hints for the **Klipper Config Directory** and **Klipper Base Config Filename** settings.
- **Klipper documentation links** — a **Klipper Documentation** link in the config editor (`Config_Reference`) and `save_variables` / `SAVE_VARIABLE` links in the Save Variables dialog.
- **Editor integration** — `[include ...]` path autocomplete, squiggle markers under missing include targets, and macros re-parsed after saving in the editor.
- **Full Klipper language support** — the Monaco language definition now covers the full set of Klipper config sections from `Config_Reference` (eddy current probes, smart effector, fans, LEDs, TMC drivers, load cells, thermal adjustment, axis twist compensation, accelerometer chips, displays, carriage, angle, and more).
- **Monaco editor** — the config editor has been migrated from Ace to Monaco: better rendering, smoother scrolling, and a proper Monokai theme.
- **Syntax linter (squiggle lines)** — errors are underlined directly in the editor:
  - Squiggles appear automatically as you type (debounced, no popups).
  - The check also runs when the editor opens.
  - The manual **Check Syntax** button still shows the full error message.
- **Live klippy.log tail** — a new _Klippy Log_ tab on the main OctoKlipper tab tails `klippy.log` in real time, so you can watch for print stalls, retransmits, and other diagnostics without opening an SSH session. It auto-scrolls, has a Pause/Start toggle, and shows which file the backend is loading.
- **Log path check in settings** — the _Klipper Log File_ setting now has a **Check path** button that resolves the entered directory on the server and shows whether `klippy.log` exists there, so a wrong path is immediately obvious.
- **Better config backups** — backups are now kept in an `archive/` folder (previous versions) plus a `current/` duplicate, so OctoPrint's own backup always holds the latest config state.
- **Backup all configs** — a button that copies every config file into the plugin data folder so OctoPrint's own backup holds all of them, not only the ones saved through the plugin. This also runs automatically right before a backup is created.
- **Restore servicefile backups** — servicefile backups can be restored and deployed to the real path (`/etc/default/klipper`) via sudo. If passwordless sudo isn't configured, you'll be asked for the sudo password.
- **Backup type tags** — the backup list now shows whether an entry is a `Config` or a `Servicefile`, and restore handles each type correctly.
- **Sudo password safety check** — before a sudo password is sent, the plugin checks the connection: HTTPS and localhost are fine, anything else asks for your confirmation first.
- **Klipper updater** — the plugin now fetches the installed and available Klipper versions and gives clear user feedback during update checks, with improved button state management.
- **Service restart command** — a command to restart the Klipper service directly from the plugin.
- **Open last config in editor** — an option to open the last edited config directly in the editor.
- **Colored short status** — the sidebar short status now uses colors for better readability.
- **Config versioning plan** — a design document for keeping the last 5 versions of every config plus a revert button (coming in a follow-up).

## 🎨 UI improvements

- **Macro button polish** — improved styling/colors, bordered group containers, and a grid layout for the parsed macro buttons.
- **Wider Group column** — the macro Group column in the settings table is now wider and dynamic.
- **Group backgrounds** — macro groups get a subtle background to separate them visually.
- **Macros settings reworked** — the macro list is now a proper table with an _Add Macro_ footer row, a live button preview that shows the macro name as you type, and a style selector that clears the custom color. The example command box is pinned to the bottom of the tab.
- **Save Variables table** — long variable names and "Used by" macro lists wrap instead of being cut off.
- **Small dialogs fixed** — the assisted bed leveling, coordinate offset, macro parameter, and PID tuning dialogs no longer clip text over button/input borders.
- **Fixes** — pressing Enter in an input no longer triggers unrelated buttons, the Klipper Tab / Sidebar checkboxes are aligned with their labels, and the copy-to-clipboard icon no longer overlaps the example command text.
- **Syntax highlighting** — improved highlighting for multiple pins on one line, more Jinja syntax, and a fix for config lines containing `=`.
- **Console messages colorized** — log output in the console is now colorized for easier reading.
- **Font size preference** — the editor font size is now remembered in `localStorage`.
- **Copy button** — the copy-to-clipboard button is hidden on plain HTTP connections for safety.

## 🐛 Fixes

- **Config editor fixes** — "Reload from file" and backup preview now load the actual content correctly.
- **Empty config files** — saving or checking an empty file returned HTTP 500 because the client sent `[]` instead of an empty string; empty content is kept as text and list/`None` payloads are coerced backend-side.
- **Create file dialog** — the submit button was dead because the dialog element was missing from the view model's `elements` list.
- **Macro parameter dialog** — crashed when a placeholder had no `default:`; every parameter now always gets a `value` observable.
- **Setup Wizard path check** — a Klipper path using `~` or an environment variable was reported as missing because the raw setting was checked with `isdir()`; the path is now expanded first.
- **Backups list** — directories returned by the recursive glob are excluded, long backup names wrap instead of being cut off, and the live `current/` duplicates are shown in a dedicated **Current Configs** section.
- **Toast/popup fixes** — error notifications now display their message properly.
- **Backup/restore** — saving and restoring backups no longer fail on paths with trailing separators.
- **Additional SAVE_CONFIG check** — an extra check before saving the config to avoid accidental overwrites.

## 🔧 Compatibility & platform fixes

This release reworks the plugin for the **newer OctoPrint versions** (while staying backward compatible with 1.11.x) and fixes several **Windows-specific** issues that surfaced in that process:

- **OctoPrint compatibility** — updated blueprint protection, permissions, and internal APIs for the newer OctoPrint versions.
- **Klipper serial port on OctoPrint 2.0** — OctoPrint 2.0 moved the serial settings to `plugins.serial_connector.*` and silently drops writes to the legacy `serial.*` paths, so the virtual serial port is now written to the correct path for the running version. Without this, the Klipper port never appeared in OctoPrint's port list on 2.0.
- **Connector options in the connection panel** — with "Replace Connection Panel" enabled, OctoPrint 2.0 could no longer render connector options because the plugin replaced the core template. OctoKlipper's panel now renders the `#connection_options_<connector>` / `data-connection-parameter` block itself, and the serial connector's own port and baudrate dropdowns are rendered too.
- **Setup Wizard error handling on 1.11** — OctoPrint 1.11 has no `serial.errorHandling` setting, so the wizard now translates between the 2.0 enum and the 1.11 `disconnectOnErrors` / `ignoreErrorsFromFirmware` booleans in both directions.
- **Non-Linux hosts** — the Setup Wizard's Klipper service check no longer reports a healthy install on platforms where Klipper's host software cannot run; it warns instead.
- **Windows path handling** — fixed path-separator handling when saving configs in subfolders or the baseconfig, and when restoring backups.
- **Moonraker Connector (experimental)** — the Setup Wizard detects it read-only and clearly labels it as experimental: version 0.1.0, no published release, requires OctoPrint 2.0, and OctoKlipper's serial-oriented features are unverified against it. It is never auto-selected, and the `status` verification step is skipped for it.
- **API documentation** — `docs/api.md` rewritten to document the current routes, methods, request/response formats, and the new backup paths.

## 🌍 Translations

- **Spanish and French are now fully translated** — the plugin is completely available in both languages.
- **German is complete again** — every string added since the last release is now translated as well.
- **Gettext catalog refreshed** — the template now carries 397 strings (was 311, with 113 in-use strings missing and 24 dead ones); the previously hardcoded macro button styles, restart types, log filter tooltips, editor dialog title, probes table headers and Refresh file list tooltip are now translatable. `babel.cfg` was fixed for Jinja2 3.x.

## 🛠 Developer tooling

- **Deploy script** — a PowerShell script (`deploy/deployOctoKlipper.ps1`) that builds the zip, uploads it to the Raspberry Pi via SCP, installs it into the OctoPrint venv, and optionally restarts OctoPrint. Supports OpenSSH and PuTTY. It falls back to a non-editable zip install for OctoPrint 1.11.x (editable installs crash there with modern setuptools/pip).
- **Zip script rewritten** — the packaging script was rewritten from VBScript to PowerShell (`.NET` `System.IO.Compression`), fixing unreliable COM-based zipping.
- **Tests** — a pytest suite covering the config tools, log analyzer, migration, extra utilities, and servicefile modules.

## 📝 Notes

- Compatible with OctoPrint 1.11.x and OctoPrint 2.0 (verified against 2.0.0rc6).
- Python 3.10+.
- Ships translations for German, Spanish and French.
- The connection-panel and serial-port fixes are OctoPrint 2.0 only; 1.11 has no `connection_options` templates, so its panel is unchanged.
- This note combines the earlier `0.4.1 rc` and `0.4.2 rc` notes; every change made after the `0.4` tag is part of `0.5.0`.
