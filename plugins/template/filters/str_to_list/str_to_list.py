from sitefab.Plugins import TemplateFilter


class str_to_list(TemplateFilter):
    """Transform a string into a list of characters"""

    @staticmethod
    def myfilter(filter_input):
        """
        Args:
            input (str): input list
        Return:
            list: list of characters
        """
        return list(filter_input)
