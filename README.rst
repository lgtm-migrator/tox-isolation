##############
tox-isolation
##############

.. start short_desc

**Runs pytest in isolation.**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|



.. |travis| image:: https://github.com/domdfcoding/tox-isolation/workflows/Linux%20Tests/badge.svg
	:target: https://github.com/domdfcoding/tox-isolation/actions?query=workflow%3A%22Linux+Tests%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/tox-isolation/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/tox-isolation/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/tox-isolation/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/tox-isolation/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Test Status

.. |requires| image:: https://requires.io/github/domdfcoding/tox-isolation/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/tox-isolation/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/tox-isolation/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/tox-isolation?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/tox-isolation?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/tox-isolation
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/tox-isolation
	:target: https://pypi.org/project/tox-isolation/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tox-isolation?logo=python&logoColor=white
	:target: https://pypi.org/project/tox-isolation/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tox-isolation
	:target: https://pypi.org/project/tox-isolation/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/tox-isolation
	:target: https://pypi.org/project/tox-isolation/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/tox-isolation
	:target: https://github.com/domdfcoding/tox-isolation/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/tox-isolation
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/tox-isolation/v0.0.0
	:target: https://github.com/domdfcoding/tox-isolation/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/tox-isolation
	:target: https://github.com/domdfcoding/tox-isolation/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/tox-isolation/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/tox-isolation/master
	:alt: pre-commit.ci status

.. end shields


Usage
----------

``tox-isolation`` runs pytest tests in isolation by copying the test directory into a temporary directory
and running the tests from there. This prevents pytest from trying to use the source files for the project,
instead forcing it to use the version installed in the virtualenv by tox.

The files copied into the temporary directory are controlled bu the ``isolate_dirs`` option in the
``testenv`` section of ``tox.ini``. This allows the files to be customised on a per-env basis.
If the option is undefined the isolation is disabled.
Relative paths are taken to be relative to the current working directory.

**Example:**

.. code-block:: ini

	# tox.ini

	[testenv]
	deps = -r{toxinidir}/tests/requirements.txt
	commands = python -m pytest tests/ {posargs}
	isolate_dirs = {toxinidir}/tests




Installation
--------------

.. start installation

``tox-isolation`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install tox-isolation

.. end installation
