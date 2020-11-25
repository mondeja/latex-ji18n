# latex-ji18n (LaTeX + Jinja2 + YAML = i18n)

Set of tools to render LaTeX documents in multiple languages using
 [Jinja2][jinja2-link] Python library and some conventions inspired by
 [jekyll-multiple-languages-plugin][jekyll-multiple-languages-plugin-link].

So you have a LaTeX document that you want to internationalize. The first step
 is convert your project in a template. Using `latex-ji18n` command line tool,
 you can render YAML files into LaTeX Jinja2 templates.

## Install

You need a `pdflatex` binary available at your system PATH. Then run:

```bash
pip install latex-ji18n
```

## Separation of data, style and layout

Next structure of directories is the workflow that imposes this utility
 working with it:

```tree
 ├── _config
 │   ├── data.yml
 │   ├── layout.yml
 │   ├── style.yml
 │   └── _private    (optional)
 │       ├── data.yml
 │       └── layout.yml
 ├── dist
 │   ├── en.pdf
 │   ├── es.pdf
 │   └── fr.pdf
 ├── _i18n
 │   ├── _private    (optional)
 │   │   └── es.yml
 │   ├── en.yml
 │   ├── es.yml
 │   └── fr.yml
 └── src
     ├── template.tex
     ├── assets.jpg
     └── references.bib
```

The process is simple, you write your replacements in `src/template.tex`
 Jinja2 template file with `\BLOCK{}` and `\VAR{}` syntax, write your
 data or options inside `_i18n/` and `_config/` folders YAML files,
 run `latex-ji18n` to compile the PDFs and you will see each one for each
 language in `dist/` folder.

### Convention for separate data files

- `_private/`: Directories that stores all the sensitive data that you don't
 want to include, for example, sharing your repositorie with GIT. This folders
 are totally optional. Inside each one, you must keep the same files structure
 that in `_i18n/` and `_config/` directories.
- `data.yml`: Data that you want to include in the context, at the root
 of the dictionary, common to all languages. All the fields stored here are
 included at the root of the context. You can't include the fields `layout`
 nor `style` in the root of the context for data files.
- `layout.yml`: Designed to store some layout options for the template. Fields
 stored here are available for the context in the `layout` dictionary.
- `style.yml`: Designed to store style options for the template. Fields
 stored here are available for the context in the `style` dictionary.
- `_i18n/{language}.yml`: Overrides data for the context. Designed to localize
 your data output. An output file will be created for every `{language}.yml`
 file, with the name of `{language}.pdf`.

### Context creation

The contexts are created updating a dictionary iterating over files in next
 order:

- `config/data.yml`
- `config/layout.yml`
- `config/style.yml`
- `config/_private/data.yml`
- `config/_private/layout.yml`
- `config/_private/style.yml`
- `_i18n/{language}.yml`
- `_i18n/_private/{language}.yml`

Context data is dumped following next rules:

- All the data located in `data.yml` files is dumped at the root of the
 context.
- Data located in `layout.yml` files are dumped into a `layout` variable
 at the root of the context.
- Data located in `style.yml` files are dumped into a `style` variable
 at the root of the context.
- If `src/` directory contains `.bib` files, database entries located at this
 files will be available ordered by entry type at `_bibdb` variable at the root
 of the context.

[jinja2-link]: https://jinja.palletsprojects.com
[jekyll-multiple-languages-plugin-link]: https://github.com/kurtsson/jekyll-multiple-languages-plugin
