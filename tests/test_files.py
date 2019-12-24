from pathlib import Path
from sitefab.files import read_file, write_file, clean_dir, get_files_list


def test_basic_file_flow(tmp_path):
    """testing all at once as it is hard to do in smaller chunk
       write -> read -> list -> clean -> list again
    """
    fname = 'a.txt'
    content = 'this is a test'
    path = Path(tmp_path) / fname

    # write
    write_file(tmp_path, fname, content)
    assert path.exists()

    # read
    read_back = read_file(path)
    assert read_back == content

    # list
    files_list = get_files_list(tmp_path, '*.txt')
    assert path in files_list

    # clean
    clean_dir(tmp_path)
    assert not path.exists()

    # filelist again
    files_list = get_files_list(path, '*.txt')
    assert not files_list  # must be empty


def test_unicode_support(tmp_path):

    fname = '😁.txt'
    content = 'this is a test 😁'
    path = Path(tmp_path) / fname

    # write
    write_file(tmp_path, fname, content)
    assert path.exists()

    # read
    read_back = read_file(path)
    assert read_back == content

    # cleanup
    clean_dir(tmp_path)


def test_writing_subdirectory(tmp_path):
    "make sure sub directory is created"

    fname = 'myfile.md'
    content = 'this is a test 😁'
    subdir = 'tobecreated'
    subdir_path = Path(tmp_path) / subdir
    path = subdir_path / fname

    # write
    write_file(subdir_path, fname, content)
    assert path.exists()
    assert subdir_path.is_dir()

    # read
    read_back = read_file(path)
    assert read_back == content

    # cleanup
    clean_dir(tmp_path)
    assert not path.exists()
    assert not subdir_path.exists()


def test_non_existing_read_file():
    assert read_file('asjkajlkajlksal32312ewdas3') == ""


def test_filelist_filter(tmp_path):
    "making sure we get all the files which have a givem suffix"
    fnames = ['😁.md', 'a.m', 'a.txt', 'b.md', 'a.md.md']
    content = 'this is a test'

    clean_dir(tmp_path)
    for fname in fnames:
        write_file(tmp_path, fname, content)

    files_list = get_files_list(tmp_path, '*.md')
    assert len(files_list) == 3

    files_list = get_files_list(tmp_path, '*.txt')
    assert len(files_list) == 1

    clean_dir(tmp_path)


def test_filelist_filter_empty(tmp_path):
    "ensure no matches return an empty array"
    clean_dir(tmp_path)
    assert get_files_list(tmp_path) == []
    assert get_files_list('thisisnotthedirectoryyoulookfor') == []


def test_filelist_recursive(tmp_path):
    clean_dir(tmp_path)
    sub_path = tmp_path / 'newdir'
    fname = 'test.md'

    txt = 'hello'
    write_file(sub_path, 'test.md', txt)

    # ensure we have a sub dir and the file in it
    assert sub_path.exists()
    assert sub_path.is_dir()
    read_text = read_file(sub_path / fname)
    assert read_text == txt

    # test we get a recursive listing
    assert len(get_files_list(tmp_path)) == 1

    # test that non recursive returns nothing
    assert get_files_list(tmp_path, recursive=False)  == []
