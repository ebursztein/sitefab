import datetime
import json

import pytz
from PIL import Image

from SiteFab.Plugins import PostProcessor
from SiteFab.SiteFab import SiteFab


class Jsonld(PostProcessor):
    """
    Write microdata jsonld_collection

    """
    lang_meta_to_jsonld = {
        'en': "English"
    }

    common = ['ScholarlyArticle', 'PublicationEvent', 'BlogPosting']

    def process(self, post, site, config):
        jsonld_data = {}
        if post.meta.microdata_type:
            #
            pre_txt = '<script type="application/ld+json">'
            post_txt = '</script>'

            jsonld_data = {
                "@context": "http://schema.org",
                "@type": str(post.meta.microdata_type),
                "url": str(post.meta.full_url),
                "name": str(post.meta.title),
                "inLanguage": Jsonld.lang_meta_to_jsonld[post.meta.lang],
                "description": str(post.meta.abstract),
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": str(post.meta.full_url)
                }
            }

            # location
            location = None
            if post.meta.conference_location:
                location_text = post.meta.conference_location
                location_array = location_text.split(",")
                if len(location_array) == 2:
                    city = location_array[0].strip()
                    country = location_array[1].strip()
                    location = {
                        "@type": "PostalAddress",
                        'addressLocality': str(city),
                        "addressCountry": str(country)
                    }

            # banner image for include_images types
            if post.meta.microdata_type in Jsonld.common:
                # create correct category name
                correct_category = post.meta.category.replace(" ", "_")
                # banner
                if post.meta.banner:
                    filename = "%s/%s" % (site.config.dir.output, post.meta.banner)

                    width, height = 0, 0
                    try:
                        with Image.open(filename) as im:
                            width, height = im.size
                    except IOError as e:
                        print "banner not found"

                    if width != 0 and height != 0:
                        jsonld_data["image"] = {
                            "@type": "ImageObject",
                            "url": str("%s%s" % (site.config.url, post.meta.banner)),
                            "height": height,
                            "width": width
                        }
                # about
                jsonld_data["about"] = [{"name": str(post.meta.category), "url": str("%s%s%s" % (
                    site.config.url, site.config.collections.category_output_dir, correct_category))}]

                # microdata specific to PublicationEvent (talk)
                if post.meta.microdata_type == "PublicationEvent":

                    jsonld_data['releasedEvent'] = {
                        "@type": "PublicationEvent",
                        "name": str(post.meta.conference_name),
                    }
                    if location:
                        jsonld_data['releasedEvent']['location'] = location

                    # performers
                    jsonld_data['performer'] = []
                    for author in post.meta.authors:
                        author = author.strip().replace(",", "")
                        info = {"@type": "Person", "name": str(author)}
                        jsonld_data['performer'].append(info)

                    #startDate
                    startDate = datetime.datetime.fromtimestamp(post.meta.creation_date_ts, tz=pytz.UTC).isoformat()
                    jsonld_data['startDate'] = str(startDate)

                elif post.meta.microdata_type == "ScholarlyArticle" or post.meta.microdata_type == "BlogPosting":
                    # award
                    jsonld_data['award'] = str(post.meta.award)

                    #headline ArticleSection
                    jsonld_data['headline'] = str(post.meta.title)
                    jsonld_data['articleSection'] = str("%s%s%s" % (
                        site.config.url, site.config.collections.category_output_dir, correct_category))
                    # Dates
                    # date "2016-10-18T08:00:00+00:00"
                    published_date = datetime.datetime.fromtimestamp(post.meta.creation_date_ts, tz=pytz.UTC).isoformat()
                    jsonld_data['datePublished'] = published_date
                    if post.meta.update_date:
                        jsonld_data['dateModified'] = datetime.datetime.fromtimestamp(post.meta.update_date_ts,
                                                                                      tz=pytz.UTC).isoformat()
                    else:
                        jsonld_data['dateModified'] = published_date

                    # authors
                    jsonld_data['author'] = []
                    for author in post.meta.authors:
                        author = author.strip().replace(",", "")
                        info = {"@type": "Person", "name": str(author)}
                        jsonld_data['author'].append(info)

                    # keywords
                    keywords = list()
                    keywords.append(str(post.meta.category))
                    for tag in post.meta.tags:
                        tag_correct = tag.replace(" ", "_")
                        meta_tag = {"name": str(tag),
                                    "url": str("%s%s%s" % (site.config.url, site.config.collections.category_output_dir, tag_correct))}
                        jsonld_data['about'].append(meta_tag)
                        keywords.append(str(tag))

                    if post.meta.seo_keywords:
                        for seo_keyword in post.meta.seo_keywords:
                            keywords.append(str(seo_keyword))
                    # keywords
                    jsonld_data["keywords"] = keywords

                    if post.meta.microdata_type == "ScholarlyArticle":
                        jsonld_data['publication'] = {
                            "@type": "PublicationEvent",
                            "name": str(post.meta.conference_name),
                            "location": location
                        }
                        jsonld_data['publisher'] = {
                            "@type": "Organization",
                            "name": str(post.meta.conference_publisher)
                        }
                    if post.meta.microdata_type == "BlogPosting":
                        filename = "%s%s" % (site.config.dir.output, site.config.logo_url)
                        with Image.open(filename) as im:
                            width, height = im.size

                        jsonld_data['publisher'] = {
                            "@type": "Organization",
                            "name": str(site.config.name),
                            "@logo": {
                                "@type": "ImageObject",
                                "url": str("%s%s" % (site.config.url, site.config.logo_url)),
                                "width": width,
                                "height": height
                            }
                        }

            jsonld_text = "%s%s%s" % (pre_txt, json.dumps(jsonld_data), post_txt)
            post.meta.jsonld = jsonld_text

            return SiteFab.OK, post.meta.title, jsonld_data
        else:
            return SiteFab.SKIPPED, post.meta.title, ""
