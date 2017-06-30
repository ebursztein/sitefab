from SiteFab.Plugins import SiteProcessor
from SiteFab.SiteFab import SiteFab
from SiteFab import utils
import gensim
from gensim import corpora, models, similarities


class RelatedPosts(SiteProcessor):
    def process(self, unused, site, config):
        
        try:
            num_related_posts = config.num_related_posts
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
            # Fixme: get correct number of topics
            num_topics = site.posts_by_tag.get_num_collections() + 1  # use collections as a proxy for the number of topics
            topic_model = models.LsiModel(tfidf[corpus], id2word=dictionary, num_topics=num_topics)
            index = similarities.MatrixSimilarity(topic_model[tfidf[corpus]], num_best=num_related_posts + 1) #+1 because the best one is itself
            
            # find simlar posts and store them
            log_details = ""
            for post, sims in zip(site.posts, index):
                post.meta.related_posts = []
                log_details += '<div class="subsection"><h3>%s</h3>Related posts:<ol>' % (post.meta.title)
                for idx, score in sims[1:]: #1: > first one is the article itself
                    p = site.posts[idx]
                    o = utils.create_objdict()
                    o.meta = p.meta
                    o.score = score
                    o.html = p.score
                    post.meta.related_posts.append(o)
                    log_details += '<li>%s (%s)</li>' % (o.meta.title, round(score,2))
                log_details += '<ol></div>'
            return (SiteFab.OK, "Related posts via LSI", log_details)
        except Exception as e:
            return (SiteFab.ERROR, "Related posts via LSI", e)

