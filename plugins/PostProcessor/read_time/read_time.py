from SiteFab.Plugins import PostProcessor
from SiteFab.SiteFab import SiteFab

class ReadTime(PostProcessor):
    def process(self, post, site):
        wpm = site.config.plugins.read_time.wpm
        if post.md and len(post.md):
            
            # basic read time
            words = post.md.count(" ")
            wps = float(wpm) / 60
            num_sec = words / wps

            # accounting for images based of medium recommendation
            num_images = min(post.info.stats.num_images, 12)
            for n in range(num_images, 0, -1):
               num_sec += n
            
            post.meta.read_time = int(num_sec / 60)
            st = "%s min read - %s words - %s images<br>%s wps - %s sec read - %s num_images" % (
                post.meta.read_time, words, num_images, round(wps, 1), round(num_sec), num_images)
            return (SiteFab.OK, post.meta.title, st)
        else:
            return (SiteFab.SKIPPED, post.meta.title, "")