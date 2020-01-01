class TemplateFilter():
    "Plugins that define jinja2 filters to be used in templates"

    @staticmethod
    def myfilter(filter_input, filter_arg):
        """Act as a jinja2 template

        Args:
            filter_input (str): the input passed to the filter
            filter_arg(str): optional arg to the filter
        Return:
            str: modified input
        """
