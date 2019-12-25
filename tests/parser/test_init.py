from sitefab.files import get_files_list


def test_parser_template_path(sitefab):
    "making sure we have the right templates in the parser"
    assert 'a' in sitefab.config.parser.templates
    assert 'img' in sitefab.config.parser.templates
    assert 'youtube' in sitefab.config.parser.templates


def test_parser_templates_loaded(sitefab):
    print(sitefab.config.parser.templates_path)
    assert len(get_files_list(sitefab.config.parser.templates_path, "*.html"))
