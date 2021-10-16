Pufo Twitter Bot 🛸
====================

|PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/pufo-twitter-bot.svg
   :target: https://pypi.org/project/pufo-twitter-bot/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pufo-twitter-bot
   :target: https://pypi.org/project/pufo-twitter-bot
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/pufo-twitter-bot
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/pufo-twitter-bot/latest.svg?label=Read%20the%20Docs
   :target: https://pufo-twitter-bot.readthedocs.io/
   :alt: Read the documentation at https://pufo-twitter-bot.readthedocs.io/
.. |Tests| image:: https://github.com/mjt91/pufo-twitter-bot/workflows/Tests/badge.svg
   :target: https://github.com/mjt91/pufo-twitter-bot/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/mjt91/pufo-twitter-bot/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/mjt91/pufo-twitter-bot
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features 🚀
-----------
This is an command-line app to create randomly created book titles to author combinations.
The interface provides the possibility to tweet the list on twitter.

* Creates a list of random book titels and author combinations
* Parameters to tune are
   * `count` for number of author/titles
   * `gender` for the gender of the authors

Book titles are in german for now. Multilanguage support maybe coming in the future.


Requirements 📋
---------------

* python>=3.7,<3.10
* twitter devloper account (to post to twitter)


Installation 🔨
----------------

You can install *Pufo Twitter Bot* via pip_ from PyPI_:

.. code:: console

   $ pip install pufo-twitter-bot


Usage
-----

Basic usage:

.. code:: console

   $ pufo-twitter-bot --count 2 --gender m
   >> 1. Der Büffel - Florentin Titze
   >> 2. Platte Tüte - Stefan Will

Please see the `Command-line Reference <Usage_>`_ for details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Pufo Twitter Bot* is free and open source software.


Issues 📌
---------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

Random book titles are taken from `buchtitelgenerator.de`_
This project would not be possible without the authors of this site for
letting me use their data. Herewith I express my deepest thanks.

Random author names generated from two origins:

* randomname.de_
* offenedaten-koeln_

The names data is distributed under the Creative Commons license (see: `cc licenses`_)


Support
-------

Get me a `coffee`_ ☕  or `beer`_ 🍺


This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _cc licenses: https://github.com/santisoler/cc-licenses
.. _buchtitelgenerator.de: https://www.buchtitelgenerator.de/
.. _randomname.de: https://randomname.de/
.. _offenedaten-koeln: https://offenedaten-koeln.de/
.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/mjt91/pufo-twitter-bot/issues
.. _pip: https://pip.pypa.io/
.. _beer: https://www.buymeacoffee.com/mjt91
.. _coffee: https://www.buymeacoffee.com/mjt91
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://pufo-twitter-bot.readthedocs.io/en/latest/usage.html
