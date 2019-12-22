from sitefab.Plugins import TemplateFilter


class format_ts(TemplateFilter):
    """format_ts custom filter"""

    @staticmethod
    def myfilter(filter_input, filter_arg="%d %B %Y"):
        """ ts to formated date

        Args:
            input (str): timestamp to format
            arg(str): date format in strftimne format
        Return:
            str: formated date
        """
        from datetime import datetime

        ts = int(filter_input)
        dt = datetime.fromtimestamp(ts)
        return dt.strftime(filter_arg)
