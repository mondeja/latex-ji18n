# Contributing

## Setup your environment

1. Go to [TexLive download page][texlive-download-link] and download the
 package for your distribution.
2. Go to [quick installation instructions page][texlive-download-link] and
 follow the steps.
3. Initialize the virtualenv `python -m virtualenv venv && . venv/bin/activate`
4. Install in edit mode with development extras: `pip install -e .[dev]`
5. Run `pre-commit install`