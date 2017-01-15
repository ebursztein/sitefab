import json

import datetime

import pytz

from SiteFab.Plugins import PostProcessor
from SiteFab.SiteFab import SiteFab

from PIL import Image


class Jsonld(PostProcessor):
    """
    Write microdata jsonld_collection

    """
    lang_meta_to_jsonld = {
        'en': "English"
    }

    def process(self, post, site):
        jsonld_data = {}
        if post.meta.microdata_type:
            #
            pre_txt = '<script type="application/ld+json">'
            post_txt = '</script>'

            jsonld_data = {"@context": "http://schema.org",
                           "@type": post.meta.microdata_type,
                           "url": post.meta.full_url,
                           "name": post.meta.title,
                           "inLanguage": Jsonld.lang_meta_to_jsonld[post.meta.lang],
                           "description": post.meta.abstract
                           }

            if post.meta.microdata_type == "ScholarlyArticle" or post.meta.microdata_type == "BlogPosting":
                correct_category = post.meta.category.replace(" ", "_")
                keywords = []
                keywords.append(post.meta.category)
                jsonld_data['mainEntityOfPage'] = {
                    "@type": "WebPage",
                    "@id": post.meta.full_url
                }
                jsonld_data['headline'] = post.meta.title
                jsonld_data['articleSection'] = "%s%s%s" % (
                site.config.url, site.config.collections.output_dir, correct_category)

                # date "2016-10-18T08:00:00+00:00"
                published_date = datetime.datetime.fromtimestamp(post.meta.creation_date_ts, tz=pytz.UTC).isoformat()
                jsonld_data['datePublished'] = published_date

                if post.meta.update_date:
                    jsonld_data['dateModified'] = datetime.datetime.fromtimestamp(post.meta.update_date_ts, tz=pytz.UTC).isoformat()
                else:
                    jsonld_data['dateModified'] = published_date
                jsonld_data['description'] = post.meta.abstract

                if post.meta.microdata_type == "ScholarlyArticle":
                    jsonld_data['publication'] = {
                        "@type": "PublicationEvent",
                        "name": post.meta.conference_name
                    }
                    jsonld_data['publisher'] = {
                        "@type": "Organization",
                        "name": post.meta.conference_publisher
                    }
                if post.meta.microdata_type == "BlogPosting":
                    filename = "generated/%s" % site.config.logo_url
                    with Image.open(filename) as im:
                        width, height = im.size

                    jsonld_data['publisher'] = {
                        "@type": "Organization",
                        "name": site.config.name,
                        "@logo": {
                            "@type": "ImageObject",
                            "url": "%s%s" % (site.config.url, site.config.logo_url),
                            "width": width,
                            "height": height
                        }
                    }

                if post.meta.banner:
                    filename = "generated/%s" % post.meta.banner
                    with Image.open(filename) as im:
                        width, height = im.size

                    jsonld_data["image"] = {
                        "@type": "ImageObject",
                        "url": "%s%s" % (site.config.url, post.meta.banner),
                        "height": height,
                        "width": width
                    }

                jsonld_data["about"] = [{"name": post.meta.category, "url": "%s%s%s" % (
                site.config.url, site.config.collections.output_dir, correct_category)}]
                for tag in post.meta.tags:
                    tag_correct = tag.replace(" ", "_")
                    meta_tag = {"name": tag,
                                "url": "%s%s%s" % (site.config.url, site.config.collections.output_dir, tag_correct)}
                    jsonld_data['about'].append(meta_tag)
                    keywords.append(tag)

                for seo_keyword in post.meta.seo_keywords:
                    keywords.append(seo_keyword)
                # keywords
                jsonld_data["keywords"] = keywords

                # authors
                jsonld_data['author'] = []
                for author in post.meta.authors:
                    author = author.strip().replace(",", "")
                    info = {"@type": "Person", "name": author}
                    jsonld_data['author'].append(info)

            jsonld_text = "%s%s%s" % (pre_txt, json.dumps(jsonld_data), post_txt)
            post.meta.jsonld = jsonld_text

            return SiteFab.OK, post.meta.title, jsonld_data
        else:
            return SiteFab.SKIPPED, post.meta.title, ""
