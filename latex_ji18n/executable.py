import abc
import inspect
import os
import shutil
import subprocess
import sys
import time


class LatexExecutable(object):
    """Base class for Latex executables."""

    def __init__(self):
        self.binary = shutil.which(self.name)

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def run(self):
        """Generates a PDF from LaTeX a source. If there are errors generating
        a :py:class:`latex_ji18n.exceptions.LatexError`` is raised.
        """
        pass

    def is_available(self):
        """Checks if builder is available.
        Builders that depend on external programs like ``latexmk`` can check
        if these are found on the path or make sure other prerequisites are
        met.

        Returns:
            Boolean indicating availability.
        """
        return bool(self.binary)

    def blocking_call(self, cmd):
        proc = subprocess.Popen(
            cmd, stderr=sys.stderr, stdout=sys.stdout, stdin=open(os.devnull))
        while proc.poll() is None:
            time.sleep(.001)
        return proc.returncode


class PdfLatexExecutable(LatexExecutable):
    name = "pdflatex"
    output_extension = ".pdf"

    def run(self, filepath):
        return self.blocking_call([self.binary, filepath])


class BiberExecutable(LatexExecutable):
    name = "biber"

    def run(self, filepath):
        return self.blocking_call([self.binary, filepath])


executables = {
    local.name: local for local in locals().values()
    if inspect.isclass(local) and issubclass(local, LatexExecutable)
    and local is not LatexExecutable
}
