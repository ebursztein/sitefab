import datetime
import json
import pytz

from sitefab.Plugins import PostProcessor
from sitefab.SiteFab import SiteFab


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
            json_ld_person = None

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

            if post.meta.microdata_type == "AboutPage" or post.meta.microdata_type == "WebSite":
                json_ld_person = {
                    "@context": "http://schema.org",
                    "@type": "Person",
                    "image":  str("%s/%s" % (site.config.url, site.config.logo_url)),
                    "jobTitle": "Anti-abuse Research Lead",
                    "name": "Elie Bursztein",
                    "alumniOf": "Stanford University",
                    "birthPlace": "Paris, France",
                    "gender": "male",
                    "nationality": "French",
                    "url": "http://www.elie.net.com",
                    "sameAs": ["https://www.facebook.com/elieblog",
                               "https://www.linkedin.com/in/bursztein/",
                               "http://twitter.com/elie",
                               "https://www.youtube.com/eliebursztein",
                               "http://instagram.com/eliebursztein",
                               "https://plus.google.com/+eliebursztein"]
                }

            # banner image for include_images types
            if post.meta.microdata_type in Jsonld.common:
                # create correct category name
                correct_category = post.meta.category.replace(" ", "_")
                # banner
                if post.meta.banner:
                    jsonld_data["image"] = str("%s%s" % (site.config.url,
                                                         post.meta.banner))

                # about
                url = str("%s/%s%s" % (site.config.url,
                                       site.config.collections.output_dir,
                                       correct_category))
                jsonld_data["about"] = [{
                                            "name": str(post.meta.category),
                                            "url": url
                                        }]

                # microdata specific to PublicationEvent (talk)
                if post.meta.microdata_type == "PublicationEvent":
                    # organizer = conference
                    jsonld_data['organizer'] = {
                        "@type": "Organization",
                        "name": str(post.meta.conference_name),
                    }
                    if location:
                        jsonld_data['location'] = location

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
                    jsonld_data['articleSection'] = str("%s/%s%s" % (
                        site.config.url, site.config.collections.output_dir, correct_category))
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

                    if post.meta.tags:
                        for tag in post.meta.tags:
                            tag_correct = tag.replace(" ", "_")
                            meta_tag = {"name": str(tag),
                                        "url": str("%s/%s%s" % (site.config.url, site.config.collections.output_dir, tag_correct))}
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

                        jsonld_data['publisher'] = {
                            "@type": "Organization",
                            "name": str(site.config.name),
                            "logo": {
                                "@type": "ImageObject",
                                "url": str("%s/%s" % (site.config.url, site.config.logo.url)),
                                "width":  site.config.logo.width,
                                "height": site.config.logo.height
                            }
                        }

            jsonld_text = "%s%s%s" % (pre_txt, json.dumps(jsonld_data), post_txt)
            if json_ld_person:
                jsonld_text = "%s%s%s%s" % (jsonld_text, pre_txt, json.dumps(json_ld_person), post_txt)
            post.meta.jsonld = jsonld_text

            return SiteFab.OK, post.meta.title, jsonld_data
        else:
            return SiteFab.SKIPPED, post.meta.title, ""
