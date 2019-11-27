import gensim
from gensim import corpora, models, similarities

from sitefab.Plugins import SiteProcessor
from sitefab.SiteFab import SiteFab
from sitefab import utils


class RelatedPosts(SiteProcessor):

    VALID_FORMAT = ['ScholarlyArticle', 'BlogPosting', 'PublicationEvent']

    def process(self, unused, site, config):

        try:
            num_related_posts = config.num_related_posts
            # Tokenize
            docs = []
            valid_posts = [] #exclude pages that are not posts
            for post in site.posts:
                if post.meta.microdata_type not in RelatedPosts.VALID_FORMAT:
                    continue
                txt = post.md
                docs.append(gensim.utils.simple_preprocess(txt, deacc=True, min_len=3, max_len=15))
                valid_posts.append(post)
                # Fixme stemming

            # build model
            dictionary = corpora.Dictionary(docs)
            corpus = [dictionary.doc2bow(doc) for doc in docs]
            tfidf = models.tfidfmodel.TfidfModel(corpus=corpus)
            # Fixme: get correct number of topics
            num_topics = len(site.posts) / 5  # use the number of post as proxy for number of topics
            topic_model = models.LsiModel(tfidf[corpus], id2word=dictionary, num_topics=num_topics)
            index = similarities.MatrixSimilarity(topic_model[tfidf[corpus]], num_best=num_related_posts + 1) #+1 because the best one is itself

            # find simlar posts and store them
            log_details = ""
            for post, sims in zip(valid_posts, index):
                if post.meta.microdata_type not in RelatedPosts.VALID_FORMAT:
                    continue
                post.meta.related_posts = []
                log_details += '<div class="subsection"><h3>%s</h3>Related posts:<ol>' % (post.meta.title)
                for idx, score in sims[1:]: #1: > first one is the article itself
                    p = valid_posts[idx]
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

