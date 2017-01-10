from SiteFab.Plugins import SiteProcessor
from SiteFab.SiteFab import SiteFab
from collections import defaultdict

import gensim
from gensim import corpora, models, similarities
from SiteFab.utils import section

class RelatedPosts(SiteProcessor):
    def process(self, unused, site):
        
        try:
            num_related_posts = site.config.plugins.related_posts.num_related_posts
            # Tokenize
            docs = []
            for post in site.posts:
                txt = post.md
                docs.append(gensim.utils.simple_preprocess(txt, deacc=True, min_len=3, max_len=15))
                # Fixme stemming
            
            # build model
            dictionary = corpora.Dictionary(docs)
            corpus = [dictionary.doc2bow(doc) for doc in docs]
            tfidf = models.tfidfmodel.TfidfModel(corpus=corpus)
            num_topics = len(site.collections) + 1  # use collections as a proxy for the number of topics
            topic_model = models.LsiModel(tfidf[corpus], id2word=dictionary, num_topics=num_topics)
            index = similarities.MatrixSimilarity(topic_model[tfidf[corpus]], num_best=num_related_posts + 1) #+1 because the best one is itself
            
            # find simlar posts and store them
            log_details = ""
            for post, sims in zip(site.posts, index):
                post.meta.related_posts = []
                log_details += '<div class="subsection"><h3>%s</h3>Related posts:<ol>' % (post.meta.title)
                for idx, score in sims[1:]: #1: > first one is the article itself
                    post.meta.related_posts.append((site.posts[idx], score))
                    log_details += '<li>%s (%s)</li>' % (site.posts[idx].meta.title, round(score,2))
                log_details += '<ol></div>'
            return (SiteFab.OK, "Related posts via LSI", log_details)
        except Exception as e:
            return (SiteFab.ERROR, "Related posts via LSI", e)

