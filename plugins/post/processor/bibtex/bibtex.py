from datetime import date

from sitefab.Plugins import PostProcessor
from sitefab.SiteFab import SiteFab


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

            authors_okay = []
            first_author_lastname = None
            for author in post.meta.authors:
                author_details = []
                author_details = author.split(",")

                if len(author_details) == 1:
                    # need to split with space instead
                    author_details = author.split(" ")
                    if len(author_details) == 1:
                        # That means no space in the author name
                        author_details.append(author)
                        author_details.append(" ")

                author_okay = "%s, %s" % (author_details[1].strip(),
                                          author_details[0].strip())
                authors_okay.append(author_okay)

                if not first_author_lastname:
                    first_author_lastname = author_details[0].strip().upper()

            year = date.fromtimestamp(post.meta.conference_date_ts).year
            stub = post.meta.title[:10].replace(" ", "").upper()

            id_publication = "%s%s%s" % (first_author_lastname, year, stub)
            authors = (" and ").join(authors_okay)

            bibtex_data = "@inproceedings{%s, " \
                          "title={%s}," \
                          "author={%s}," \
                          "booktitle={%s}," \
                          "year={%s}," \
                          "organization={%s}}" % (id_publication,
                                                  post.meta.title, authors,
                                                  post.meta.conference_name,
                                                  year,
                                                  post.meta.conference_publisher  # noqa
                                                )

            post.meta.bibtex = bibtex_data

            return SiteFab.OK, post.meta.title, bibtex_data
        else:
            return SiteFab.SKIPPED, post.meta.title, ""
