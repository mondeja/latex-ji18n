import abc
import os
import shutil
import subprocess
import sys

from latex_ji18n.exceptions import LatexBuildError


class LatexBuilder(object):
    """Base class for Latex builders."""

    def __init__(self):
        self.binary = shutil.which(self.binary_name)

    @property
    @abc.abstractmethod
    def binary_name(self):
        pass

    @abc.abstractmethod
    def build(self):
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

    def call(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise LatexBuildError(stderr)
        return (stdout, stderr)

    def live_stdout_call(self, cmd):
        proc = subprocess.Popen(
            cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=open(os.devnull)
        )
        line = ""
        for out in iter(lambda: proc.stdout.read(1), b""):
            ch = out.decode("latin1")
            line += ch
            if ch == "\n":
                yield line.strip("\n")
                line = ""
        proc.communicate()
        return proc.returncode


class PdfLatexBuilder(LatexBuilder):
    binary_name = "pdflatex"

    def build(self, filepath, n_runs=2):
        for i in range(n_runs):
            for line in self.live_stdout_call([self.binary, filepath]):
                sys.stdout.write("%s\n" % line)
