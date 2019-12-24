from pathlib import Path


def test_config_paths(sitefab):
    # path
    correct_path = Path('tests/data/config/generator_templates/logs')
    assert sitefab.logger.config.template_dir == correct_path

    # templates
    assert sitefab.logger.config.log_template == 'log.html'
    assert sitefab.logger.config.log_index_template == "log_index.html"
    assert sitefab.logger.config.stats_template == "stats.html"


def test_directory_exist(sitefab):
    output_dir = Path(sitefab.logger.config.output_dir)
    assert output_dir.exists()
    assert output_dir.is_dir()
