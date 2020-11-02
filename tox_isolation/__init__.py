#!/usr/bin/env python3
#
#  __init__.py
"""
Runs pytest in isolation.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import os
import pathlib
import shutil
import sqlite3
from tempfile import TemporaryDirectory

# 3rd party
import pluggy  # type: ignore
import py.path
from consolekit.terminal_colours import Style
from domdf_python_tools.typing import PathLike
from tox.config import Parser, TestenvConfig  # type: ignore
from tox.venv import VirtualEnv  # type: ignore

__all__ = ["tox_addoption", "tox_runtest", "fixup_coverage"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_addoption(parser: Parser):  # noqa: D103
	parser.add_testenv_attribute(
			name="isolate_dirs",
			type="line-list",
			help="List of files and directories to copy to the isolated environment.",
			default=None,
			postprocess=None,
			)


@hookimpl(tryfirst=True)
def tox_runtest(venv: VirtualEnv, redirect):
	"""
	Create a temporary directory, symlink the test directory into it, and chdir into that directory.
	"""

	envconfig: TestenvConfig = venv.envconfig

	if envconfig.isolate_dirs:

		# venv.envconfig.setenv["COVERAGE_HOME"] = str(venv.path / "lib")
		# venv.envconfig.setenv["COVERAGE_HOME"] = envconfig.get_envsitepackagesdir()

		print(Style.BRIGHT(f"{envconfig.envname} run-test-pre: isolating test environment"))

		source_dir = pathlib.Path.cwd()

		with TemporaryDirectory() as tmpdir:
			for directory in envconfig.isolate_dirs:
				if os.path.isabs(directory):
					os.symlink(directory, pathlib.Path(tmpdir) / os.path.relpath(directory, source_dir))
				else:
					os.symlink(source_dir / directory, pathlib.Path(tmpdir) / directory)

			venv.envconfig.changedir = py.path.local(tmpdir)
			venv.test(redirect=redirect)

			# copy .coverage from tmp dir back into root
			if (pathlib.Path(tmpdir) / ".coverage").is_file():
				shutil.copy2(pathlib.Path(tmpdir) / ".coverage", source_dir / ".coverage")
				fixup_coverage(
						old_base=envconfig.get_envsitepackagesdir(),
						new_base=source_dir,
						coverage_filename=source_dir / ".coverage"
						)

		return True  # Return non-None to indicate plugin has completed

	return None


def fixup_coverage(
		old_base: PathLike,
		new_base: PathLike,
		coverage_filename: PathLike = ".coverage",
		):
	"""
	Replaces the start of filenames in .coverage files.

	:param old_base:
	:param new_base:
	:param coverage_filename:
	"""

	conn = sqlite3.connect(str(coverage_filename))
	c = conn.cursor()

	old_base = pathlib.Path(old_base)
	new_base = pathlib.Path(new_base)

	for (idx, filename) in c.execute("SELECT * FROM file").fetchall():

		if not filename.startswith(str(old_base)):
			continue

		new_filename = str(new_base / pathlib.Path(filename).relative_to(old_base))
		c.execute("UPDATE file SET path=? WHERE id=?", (new_filename, idx))

	conn.commit()
	conn.close()
