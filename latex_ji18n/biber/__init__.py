
import os

import bibtexparser


def get_bib_files_from_directory(dirpath):
    for fn in os.listdir(dirpath):
        if os.path.splitext(fn)[-1] == '.bib':
            yield fn


def get_db_entries_by_type_from_dir_bib_files(dirpath):
    response = {}
    for fn in get_bib_files_from_directory(dirpath):
        filepath = os.path.join(dirpath, fn)
        with open(filepath) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)

        for entry in bib_database.entries:
            if entry['ENTRYTYPE'] not in response:
                response[entry['ENTRYTYPE']] = []

            response[entry['ENTRYTYPE']].append(entry)
    return response
