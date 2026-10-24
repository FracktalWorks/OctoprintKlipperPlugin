# -*- coding: utf-8 -*-
# <Octoprint Klipper Plugin>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

plugin_identifier = "klipper"

plugin_package = "octoprint_klipper"

plugin_name = "OctoKlipper"

import subprocess


def _git_version_suffix():
    """Return a PEP 440 local version suffix from the current git state.

    Appends the short commit SHA (e.g. "+g1a2b3c4"). When the working tree
    has uncommitted changes, also appends ".dirty.g<sha>" where <sha> is the
    short SHA of the stash commit created by `git stash create` — a
    deterministic identifier of the dirty working-tree state.
    Returns "" when git is unavailable or the directory is not a git repo.
    """
    try:
        sha = (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
    except (subprocess.CalledProcessError, OSError):
        return ""

    suffix = "+g" + sha

    try:
        stash_sha = (
            subprocess.check_output(
                ["git", "stash", "create"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
    except (subprocess.CalledProcessError, OSError):
        stash_sha = ""

    if stash_sha:
        try:
            short_stash = (
                subprocess.check_output(
                    ["git", "rev-parse", "--short", stash_sha],
                    stderr=subprocess.DEVNULL,
                )
                .decode("utf-8")
                .strip()
            )
        except (subprocess.CalledProcessError, OSError):
            short_stash = stash_sha[:7]
        suffix += "-dirty.g" + short_stash

    return suffix


plugin_version = "0.4.1" + _git_version_suffix()

plugin_description = """A plugin for OctoPrint to configure,control and monitor the Klipper 3D printer software."""

plugin_author = "thelastWallE"

plugin_author_email = "thelastwalle.github@gmail.com"

plugin_url = "https://github.com/FracktalWorks/OctoprintKlipperPlugin"

plugin_license = "AGPLv3"

plugin_requires = ["psutil", "sarge"]

plugin_additional_data = []

plugin_additional_packages = []

plugin_ignored_packages = []

additional_setup_parameters = {}

########################################################################################################################

from setuptools import setup


def _plain_setuptools_parameters():
    """Same result as octoprint_setuptools.create_plugin_setup_parameters, without importing OctoPrint.

    pip builds in an isolated environment (PEP 517) where OctoPrint is not importable, so a hard
    dependency on octoprint_setuptools makes `pip install <this plugin>` -- and OctoPrint's own
    software update -- fail on modern pip (OctoPrint 1.11 / Python 3.13 printers).
    Same approach as FracktalWorks/ControlCenter and TwinDragonPrintRestore.
    """
    import os

    from setuptools import find_packages

    packages = set(
        [plugin_package]
        + [
            p
            for p in find_packages(exclude=plugin_ignored_packages)
            if p.startswith(plugin_package + ".")
        ]
        + list(plugin_additional_packages)
    )
    data = []
    for d in ["static", "templates", "translations"] + list(plugin_additional_data):
        base = os.path.join(plugin_package, d)
        for root, _, files in os.walk(base):
            data += [os.path.relpath(os.path.join(root, f), plugin_package) for f in files]
    requires = list(plugin_requires)
    if not any(r.lower().startswith("octoprint") for r in requires):
        requires = ["OctoPrint"] + requires
    return {
        "name": plugin_name,
        "version": plugin_version,
        "description": plugin_description,
        "author": plugin_author,
        "author_email": plugin_author_email,
        "url": plugin_url,
        "license": plugin_license,
        "packages": sorted(packages),
        "package_data": {plugin_package: data},
        "include_package_data": True,
        "zip_safe": False,
        "install_requires": requires,
        "entry_points": {
            "octoprint.plugin": ["%s = %s" % (plugin_identifier, plugin_package)]
        },
    }


try:
    import octoprint_setuptools
except ImportError:
    octoprint_setuptools = None

if octoprint_setuptools is None:
    setup_parameters = _plain_setuptools_parameters()
else:
    setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
        identifier=plugin_identifier,
        package=plugin_package,
        name=plugin_name,
        version=plugin_version,
        description=plugin_description,
        author=plugin_author,
        mail=plugin_author_email,
        url=plugin_url,
        license=plugin_license,
        requires=plugin_requires,
        additional_packages=plugin_additional_packages,
        ignored_packages=plugin_ignored_packages,
        additional_data=plugin_additional_data,
    )

if len(additional_setup_parameters):
    setup_parameters.update(additional_setup_parameters)

setup(**setup_parameters)
