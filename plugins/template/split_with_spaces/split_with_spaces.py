from SiteFab.Plugins import TemplateFilter

class split_with_spaces(TemplateFilter):
    """split_with_spaces custom filter"""

    @staticmethod
    def myfilter(filter_input):
        """
        Args:
            input (str): Any string
        Return:
            str: String splitted with spaces
        """
        return " ".join(filter_input)