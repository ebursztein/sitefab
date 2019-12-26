import sys
from pathlib import Path
from sitefab.cmdline.cmdline import generate, version


def test_compile_and_check_generated_content():
    # needed to find conftest
    sys.path.append(str(Path(__file__).absolute().parents[1]))
    from conftest import TEMPLATE_DATA_CONFIG_FILE_PATH  # noqa
    generate(TEMPLATE_DATA_CONFIG_FILE_PATH, version)
