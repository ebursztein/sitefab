from sitefab.cmdline.cmdline import generate, version


def test_compile_and_check_generated_content(sitefab):
    generate(sitefab.config_filename, version)
