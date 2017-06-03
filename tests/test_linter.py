# encoding: utf-8
import pytest

class TestLinter():
    "Base class for linter testing"

    def get_linter_errors_list(self, results):
        "Return the list of errors returned by the linter"
        lst = []
        for res in results.info:
            lst.append(res[0])
        return lst