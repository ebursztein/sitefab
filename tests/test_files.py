from pathlib import Path
from sitefab.files import read_file, write_file, clean_dir


def test_read_write(tmp_path):
    fname = 'a.txt'
    content = 'this is a test'
    path = Path(tmp_path) / fname
    write_file(tmp_path, fname, content)
    assert path.exists()
    read_back = read_file(path)
    assert read_back == content
