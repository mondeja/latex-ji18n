import os
import re


DEFAULT_CONFIG_DIRNAME = "_config"
DEFAULT_DATA_FILENAME = "data.yml"
DEFAULT_LAYOUT_FILENAME = "layout.yml"
DEFAULT_STYLE_FILENAME = "style.yml"
DEFAULT_I18N_DIRNAME = "_i18n"
DEFAULT_PRIVATE_DIRNAME = "_private"
DEFAULT_SOURCE_DIRNAME = "src"
DEFAULT_DIST_DIRNAME = "dist"
DEFAULT_TEMPLATE_FILENAME = "template.tex"
DEFAULT_BIBDB_VARIABLE_NAME = "_bibdb"


class BaseConfig:
    def __dict__(self):
        return {
            "config_dirname": self.config_dirname,
            "i18n_dirname": self.i18n_dirname,
            "private_dirname": self.private_dirname,
            "source_dirname": self.source_dirname,
            "dist_dirname": self.dist_dirname,
            "data_filename": self.data_filename,
            "layout_filename": self.layout_filename,
            "style_filename": self.style_filename,
            "template_filename": self.template_filename,
            "bibdb_variable_name": self.bibdb_variable_name,
        }

    def get_forbidden_attrs(self):
        return [
            os.path.splitext(self.layout_filename)[0],
            os.path.splitext(self.style_filename)[0],
            self.bibdb_variable_name,
        ]

    def localized_template_name_schema(self):
        if re.match(r"^template\.", self.template_filename):
            return re.sub(r"^template", "%s", self.template_filename)
        return "%s." + self.template_filename


class Config(BaseConfig):
    def __init__(
        self,
        config_dirname=DEFAULT_CONFIG_DIRNAME,
        i18n_dirname=DEFAULT_I18N_DIRNAME,
        private_dirname=DEFAULT_PRIVATE_DIRNAME,
        source_dirname=DEFAULT_SOURCE_DIRNAME,
        dist_dirname=DEFAULT_DIST_DIRNAME,
        data_filename=DEFAULT_DATA_FILENAME,
        layout_filename=DEFAULT_LAYOUT_FILENAME,
        style_filename=DEFAULT_STYLE_FILENAME,
        template_filename=DEFAULT_TEMPLATE_FILENAME,
        bibdb_variable_name=DEFAULT_BIBDB_VARIABLE_NAME,
    ):
        self.config_dirname = config_dirname
        self.i18n_dirname = i18n_dirname
        self.private_dirname = private_dirname
        self.source_dirname = source_dirname
        self.dist_dirname = dist_dirname
        self.data_filename = data_filename
        self.layout_filename = layout_filename
        self.style_filename = style_filename
        self.template_filename = template_filename
        self.bibdb_variable_name = bibdb_variable_name
