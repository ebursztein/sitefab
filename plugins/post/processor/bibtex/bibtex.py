from datetime import date

from SiteFab.Plugins import PostProcessor
from SiteFab.SiteFab import SiteFab


class Bibtex(PostProcessor):
    """
    Write bibtex data for each publication

    """
    def process(self, post, site, config):
        """

        :param post: post data
        :param site: site data
        :param config: plugin config
        :return:
        """
        bibtex_data = ""
        if post.meta.template == "publication":
            year = date.fromtimestamp(post.meta.conference_date_ts).year
            id_publication = "Bursztein%s%s" % (year, post.meta.title[:10].replace(" ", ""))
            authors_okay = []
            for author in post.meta.authors:
                author_details = author.split(",")
                author_okay = "%s, %s" % (author_details[1].strip(), author_details[0].strip())
                authors_okay.append(author_okay)
            authors = (" and ").join(authors_okay)

            bibtex_data = "@inproceedings{%s, " \
                          "title={%s}," \
                          "author={%s}," \
                          "booktitle={%s}," \
                          "year={%s}," \
                          "organization={%s}}" % (id_publication, post.meta.title, authors, post.meta.conference_name, year, post.meta.conference_publisher)
            post.meta.bibtex = bibtex_data

            return SiteFab.OK, post.meta.title, bibtex_data
        else:
            return SiteFab.SKIPPED, post.meta.title, ""
