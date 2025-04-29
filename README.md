# Pufo Twitter Bot 🛸

[![PyPI](https://img.shields.io/pypi/v/pufo-twitter-bot.svg)](https://pypi.org/project/pufo-twitter-bot/)
[![Python Version](https://img.shields.io/pypi/pyversions/pufo-twitter-bot)](https://pypi.org/project/pufo-twitter-bot)
[![License](https://img.shields.io/pypi/l/pufo-twitter-bot)](https://opensource.org/licenses/MIT)
[![Read the Docs](https://img.shields.io/readthedocs/pufo-twitter-bot/latest.svg?label=Read%20the%20Docs)](https://pufo-twitter-bot.readthedocs.io/)
[![Tests](https://github.com/mjt91/pufo-twitter-bot/workflows/Tests/badge.svg)](https://github.com/mjt91/pufo-twitter-bot/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/mjt91/pufo-twitter-bot/branch/main/graph/badge.svg)](https://codecov.io/gh/mjt91/pufo-twitter-bot)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Important Note: As of August 2024 the source site buchtitelgenerator.de is down. Thus the project is on hold till I find time to build a solution. Looking into LLM integration as well.**

## Features 🚀

This is an command-line app to create randomly created book titles to author combinations.
The interface provides the possibility to tweet the list on twitter.

- Creates a list of random book titels and author combinations
- Parameters to tune are
  - `count` for number of author/titles
  - `gender` for the gender of the authors

Book titles are in german for now. Multilanguage support maybe coming in the future.

## Requirements 📋

- python>=3.7,<3.10
- twitter devloper account (to post to twitter)

## Installation 🔨

You can install _Pufo Twitter Bot_ via pip from PyPI:

```console
$ pip install pufo-twitter-bot
```

If you want to install inside a docker container:

```console
$ docker build -t pufo-bot .
$ docker run --env-file .env pufo-bot
```

I installed it as a cronjob, see `cronjob` file.

## Usage

Basic usage:

```console
$ pufo-twitter-bot --count 2 --gender m
>> 1. Der Büffel - Florentin Titze
>> 2. Platte Tüte - Stefan Will
```

Please see the [Command-line Reference](https://pufo-twitter-bot.readthedocs.io/en/latest/usage.html) for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide](CONTRIBUTING.rst).

## License

Distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT),
_Pufo Twitter Bot_ is free and open source software.

## Issues 📌

If you encounter any problems,
please [file an issue](https://github.com/mjt91/pufo-twitter-bot/issues) along with a detailed description.

## Credits

Random book titles are taken from [buchtitelgenerator.de](https://www.buchtitelgenerator.de/)
This project would not be possible without the authors of this site for
letting me use their data. Herewith I express my deepest thanks.

Random author names generated from two origins:

- [randomname.de](https://randomname.de/)
- [offenedaten-koeln](https://offenedaten-koeln.de/)

The names data is distributed under the Creative Commons license (see: [cc licenses](https://github.com/santisoler/cc-licenses))

## Support

Get me a [coffee](https://www.buymeacoffee.com/mjt91) ☕ or [beer](https://www.buymeacoffee.com/mjt91) 🍺

This project was generated from [@cjolowicz](https://github.com/cjolowicz)'s [Hypermodern Python Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python) template.
