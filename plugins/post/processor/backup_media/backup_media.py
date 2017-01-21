import tqdm
from multiprocessing import Pool
import requests

from SiteFab.Plugins import PostProcessor
from SiteFab.SiteFab import SiteFab

class BackupMedia(PostProcessor):
    def process(self, post, site, config):
        if post.md and len(post.md):
            p = Pool(5) # num thread
            imgs = post.elements.images
            print imgs
            return (SiteFab.OK, post.meta.title, "")
        else:
            return (SiteFab.SKIPPED, post.meta.title, "")