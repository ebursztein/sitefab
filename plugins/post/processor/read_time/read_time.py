from sitefab.Plugins import PostProcessor
from sitefab.SiteFab import SiteFab
from tabulate import tabulate


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
            info = [
                ['word per minute', wps],
                ['words', post.nlp.stats.counts.words],
                ['num images', num_images],
                ['read time', post.meta.read_time]
            ]

            return (SiteFab.OK, post.meta.title, tabulate(info,
                                                          tablefmt='html'))
        else:
            return (SiteFab.SKIPPED, post.meta.title, "")
