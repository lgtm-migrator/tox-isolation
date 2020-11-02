# stdlib
import re
from subprocess import PIPE, Popen
from textwrap import dedent

# 3rd party
from domdf_python_tools.paths import in_directory


def test_isolation(tmp_pathplus):

	repo = tmp_pathplus / "demo_repo"
	repo.mkdir()

	(repo / "project").mkdir()
	(repo / "project" / "__init__.py").touch()

	(repo / "tests").mkdir()
	(repo / "tests" / "test_something.py").write_lines([
			"def test_something():",
			"    pass",
			])

	(repo / "tox.ini").write_clean(
			dedent(
					"""\
[tox]
envlist = py36, py37, py38
skip_missing_interpreters = True
requires = pip>=20.2.1

[testenv]
deps = pytest
commands = python -m pytest tests/
isolate_dirs = tests
"""
					)
			)

	(repo / "setup.py").write_lines([
			"from setuptools import setup",
			"setup(name='project', version=1)",
			])

	with in_directory(repo):
		tox_process = Popen(["tox"], stdout=PIPE, stderr=PIPE)
		(output_, err) = tox_process.communicate()
		exit_code = tox_process.wait()

	assert not err

	output = output_.decode("UTF-8")

	print(output)

	if "py36: InterpreterNotFound: python3.6" not in output:
		assert "py36 run-test-pre: isolating test environment" in output
		assert "py36 run-test-pre: isolating test environment" in output.splitlines()

	if "py37: InterpreterNotFound: python3.7" not in output:
		assert "py37 run-test-pre: isolating test environment" in output
		assert "py37 run-test-pre: isolating test environment" in output.splitlines()

	if "py38: InterpreterNotFound: python3.8" not in output:
		assert "py38 run-test-pre: isolating test environment" in output
		assert "py38 run-test-pre: isolating test environment" in output.splitlines()

	assert f"rootdir: {repo!s}" not in output
	assert f"rootdir: {repo!s}" not in output.splitlines()

	assert exit_code == 0
