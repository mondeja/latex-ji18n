import contextlib
import inspect
import os

from latex_ji18n.biber import get_db_entries_by_type_from_dir_bib_files
from latex_ji18n.config import Config
from latex_ji18n.io import read_yaml_file


class BaseContext(dict):
    def __init__(self, config=Config, metadata_dict="__config", **kwargs):
        super().__init__(**kwargs)

        self._metadata_dict = metadata_dict
        self[self._metadata_dict] = {}

        if inspect.isclass(config):
            config = config()
        self._config = config

        for key, value in self._config.__dict__().items():
            self._set_meta(key, value)

        self._prepared = False
        self._loaded = False

    def _get_meta(self, key, default=None):
        return self[self._metadata_dict].get(key, default)

    def _set_meta(self, key, value):
        self[self._metadata_dict][key] = value

    def _prepare_file(
        self,
        filepath,
        target_meta_prop_name,
        must_exists=False,
        not_exists_msg=None,
        not_exists_error=RuntimeError,
    ):
        """Check that file exists and appends its filepath to meta
        dictionary of the context."""
        if must_exists and not os.path.exists(filepath):
            raise not_exists_error(not_exists_msg)
        if os.path.exists(filepath):
            self._set_meta(target_meta_prop_name, filepath)

    def update(self, newdict, *args, **kwargs):
        if hasattr(newdict, "_metadata_dict"):
            # Preserve metadata merging contexts
            self[self._metadata_dict].update(newdict[newdict._metadata_dict])

            newdict_meta = newdict[newdict._metadata_dict]
            del newdict[newdict._metadata_dict]
            super().update(newdict, *args, **kwargs)
            newdict[newdict._metadata_dict] = newdict_meta
        else:
            super().update(newdict, *args, **kwargs)


class ProjectContext(BaseContext):
    """Common context shared by all language contexts of the project."""

    def __init__(self, project_path=None, **kwargs):
        super().__init__(**kwargs)
        if project_path is None:
            project_path = os.getcwd()
        self._set_meta("project_path", project_path)

    @property
    def project_path(self):
        return self._get_meta("project_path")

    @property
    def source_dirpath(self):
        return os.path.join(self.project_path, self._get_meta("source_dirname"))

    @property
    def dist_dirpath(self):
        return os.path.join(self.project_path, self._get_meta("dist_dirname"))

    @property
    def template_filepath(self):
        _tfp = self._get_meta("template_filepath")
        if _tfp:
            return _tfp
        self._prepare()
        return self._get_meta("template_filepath")

    def _prepare(self):
        """Prepare the context."""
        if self._prepared:
            return

        project_path = self._get_meta("project_path")

        # config/
        config_dirpath = os.path.join(project_path, self._get_meta("config_dirname"))
        self._prepare_file(config_dirpath, "config_dirpath")

        # config/_private/
        config_private_dirpath = os.path.join(
            config_dirpath, self._get_meta("private_dirname")
        )
        self._prepare_file(config_private_dirpath, "config_private_dirpath")

        # config/data.yml
        data_filename = self._get_meta("data_filename")
        self._prepare_file(os.path.join(config_dirpath, data_filename), "data_filepath")

        # config/_private/data.yml
        self._prepare_file(
            os.path.join(config_private_dirpath, data_filename), "data_private_filepath"
        )

        # config/layout.yml
        layout_filename = self._get_meta("layout_filename")
        self._prepare_file(
            os.path.join(config_dirpath, layout_filename), "layout_filepath"
        )

        # config/_private/layout.yml
        self._prepare_file(
            os.path.join(config_private_dirpath, layout_filename),
            "layout_private_filepath",
        )

        # config/style.yml
        style_filename = self._get_meta("style_filename")
        self._prepare_file(
            os.path.join(config_dirpath, style_filename), "style_filepath"
        )

        # config/_private/style.yml
        self._prepare_file(
            os.path.join(config_private_dirpath, style_filename),
            "style_private_filepath",
        )

        # src/
        source_dirpath = os.path.join(project_path, self._get_meta("source_dirname"))
        self._prepare_file(
            source_dirpath,
            "source_dirpath",
            must_exists=True,
            not_exists_msg=("Source directory '%s' does not exists.") % source_dirpath,
        )

        # src/main.template.tex
        template_filepath = os.path.join(
            source_dirpath, self._get_meta("template_filename")
        )
        self._prepare_file(
            template_filepath,
            "template_filepath",
            must_exists=True,
            not_exists_msg=("Template file '%s' does not exists.") % template_filepath,
        )

        # dist/
        dist_dirpath = os.path.join(project_path, self._get_meta("dist_dirname"))
        self._prepare_file(
            dist_dirpath,
            "dist_dirpath",
            must_exists=True,
            not_exists_msg=("Distribution directory '%s' does not exists.")
            % dist_dirpath,
        )

        # _i18n/
        i18n_dirpath = os.path.join(project_path, self._get_meta("i18n_dirname"))
        self._prepare_file(
            i18n_dirpath,
            "i18n_dirpath",
            must_exists=True,
            not_exists_msg=("i18n directory '%s' does not exists.") % i18n_dirpath,
        )

        # _i18n/
        i18n_private_dirpath = os.path.join(
            i18n_dirpath, self._get_meta("private_dirname")
        )
        self._prepare_file(i18n_private_dirpath, "i18n_private_dirpath")

        # Load bib databases
        self.update({self._get_meta("bibdb_variable_name"):
                     get_db_entries_by_type_from_dir_bib_files(source_dirpath)})

        self._prepared = True

    def load(self):
        if self._loaded:
            return

        data_file_meta_props = [
            "data_filepath",
            "layout_filepath",
            "style_filepath",
            "data_private_filepath",
            "layout_private_filepath",
            "style_private_filepath",
        ]

        for data_file_meta_prop in data_file_meta_props:
            # print(data_file_meta_prop, self[self._metadata_dict])
            if data_file_meta_prop in self[self._metadata_dict]:
                partial_context = read_yaml_file(self._get_meta(data_file_meta_prop))
                if data_file_meta_prop.startswith(("layout", "style")):
                    vars_group = data_file_meta_prop.split("_")[0]
                    if vars_group not in self:
                        self[vars_group] = {}
                    self[vars_group].update(partial_context)
                else:
                    self.update(partial_context)
        self._loaded = True

    def discover_languages(self):
        self._prepare()

        for filename in os.listdir(self._get_meta("i18n_dirpath")):
            lang, ext = os.path.splitext(filename)
            if ext != ".yml":
                continue
            yield lang

    @contextlib.contextmanager
    def sourcedir_as_cwd(self):
        """Change to source directory path as current working directory
        while the context is active.
        """
        _previous_cwd = os.getcwd()
        _source_dirpath = self._get_meta("source_dirpath")
        os.chdir(_source_dirpath)
        yield _source_dirpath
        os.chdir(_previous_cwd)


class LanguageContext(BaseContext):
    def __init__(self, language="en", project_context=ProjectContext, **kwargs):
        super().__init__(**kwargs)

        self.project_context = project_context
        if inspect.isclass(project_context):
            self.project_context = self.project_context()
        self._set_meta("language", language)

    @property
    def localized_tex_filename(self):
        schema = self.project_context._config.localized_template_name_schema()
        return schema % self._get_meta("language")

    @property
    def localized_tex_filepath(self):
        return os.path.join(
            self.project_context.source_dirpath, self.localized_tex_filename
        )

    @property
    def filepath(self):
        _fp = self._get_meta("i18n_filepath")
        if _fp:
            return _fp
        self._prepare()
        return self._get_meta("i18n_filepath")

    def _prepare(self):
        self.project_context._prepare()
        if self._prepared:
            return

        self[self._metadata_dict].update(
            self.project_context[self.project_context._metadata_dict]
        )

        i18n_filepath = os.path.join(
            self.project_context._get_meta("i18n_dirpath"),
            "%s.yml" % self._get_meta("language"),
        )
        self._prepare_file(
            i18n_filepath,
            "i18n_filepath",
            must_exists=True,
            not_exists_msg=("i18n file '%s' does not exists.") % i18n_filepath,
        )

        self._prepared = True

    def _check_forbidden_attrs(self, data):
        forbidden_attrs = self.project_context._config.get_forbidden_attrs()
        for forbidden_attr in forbidden_attrs:
            if forbidden_attr in data:
                msg = (
                    "The file '%s' can not contain an attribute"
                    " '%s', you must use the file '%s' instead."
                ) % (
                    self._get_meta("i18n_filepath"),
                    forbidden_attr,
                    self._get_meta(forbidden_attr + "_filepath"),
                )
                raise ValueError(msg)

    def load(self):
        """Load the data files to populate the context. The order of
        updating is the next.

        - config/data.yml
        - config/layout.yml
        - config/style.yml
        - config/_private/data.yml
        - config/_private/layout.yml
        - config/_private/style.yml
        - _i18n/{language}.yml
        - _i18n/_private/{language}.yml
        """
        self._prepare()

        self.project_context.load()
        if self._loaded:
            return

        data = read_yaml_file(self._get_meta("i18n_filepath"))
        self._check_forbidden_attrs(data)
        self.update(data)

        i18n_private_dirpath = self._get_meta("i18n_private_dirpath")
        if i18n_private_dirpath:
            i18n_private_filepath = os.path.join(
                i18n_private_dirpath, "%s.yml" % self._get_meta("language")
            )
            data = read_yaml_file(i18n_private_filepath)
            self._check_forbidden_attrs(data)
            self.update(data)

        self.update(self.project_context)

        self._loaded = True
