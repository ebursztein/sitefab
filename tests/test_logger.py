from pathlib import Path


def test_config_paths(sitefab):
    # path
    partial_correct_path = Path('config/templates/logs')
    assert str(partial_correct_path) in str(sitefab.logger.config.template_dir)

    # templates
    assert sitefab.logger.config.log_template == 'log.html'
    assert sitefab.logger.config.log_index_template == "log_index.html"
    assert sitefab.logger.config.stats_template == "stats.html"


def test_directory_exist(sitefab):
    output_dir = Path(sitefab.logger.config.output_dir)
    assert output_dir.exists()
    assert output_dir.is_dir()
