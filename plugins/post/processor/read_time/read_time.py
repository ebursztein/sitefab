from sitefab.Plugins import PostProcessor
from sitefab.SiteFab import SiteFab


class ReadTime(PostProcessor):
    def process(self, post, site, config):
        if post.md and len(post.md):
            wps = config.wpm / 60
            num_sec = post.nlp.stats.counts.words / wps

            # accounting for images based of medium recommendation
            num_images = min(post.meta.statistics.num_images, 12)
            for n in range(num_images):
                num_sec += n

            # reading time in minutes
            post.meta.read_time = max(1, num_sec // 60)
            st = "%s min read - %s words - %s images<br>%s wps - %s sec read\
                - %s num_images" % (post.meta.read_time, post.nlp.counts.words,
                                    num_images, round(wps, 1), round(num_sec),
                                    num_images)
            return (SiteFab.OK, post.meta.title, st)
        else:
            return (SiteFab.SKIPPED, post.meta.title, "")
