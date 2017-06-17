# Search Plugin

Plugin that generate the data and javascript needed to search the post locally in pure javascript

## Usage

Here is a simple search page that allows to search  via an inputbox and via the query parameter **q**:

```html

<html>
    <head>
        <script src="static/js/js_posts.js"></script>
        <script src="/static/js/search.js"></script>
    </head>
    <body>
        <input id="searchbox" type="search" value="" placeholder="search" size="30">
        <div id="search_results"></div>


        <script>

            var search_results = document.getElementById('search_results');

            function search_callback(docs, query) {
                /* Function called with search results
                @param docs: the list of doc that matches the query
                @param query: the query string
                */
                var html = "<ul>"
                for (var i = 0; docs[i]; i++) {
                    var doc = docs[i];
                    var info = window.posts[doc.id];
                    html += '<li><a href="' + info.permanent_url + '"> [' + doc.score + "]" + info.title + "</a></li>";
                }
                html += "</ul>";
                search_results.innerHTML = html;
            }

            function getURLParameter(name) {
                return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
            }

            //This can be optimized by doing it server side
            search_init(['title', 'authors', 'conference', 'terms'])
            
            // Attach the search to the search input
            var searchBox = document.getElementById('searchtop')
            search_attach_to(searchBox, search_callback) 
            
            //do the search based of url parameters if needed
            var query = getURLParameter('q');
            if (query) {
                console.log(query);
                var results = search(query);
                search_callback(results, query);
            }
        </script>
    </body>
</html>

```

Note you most likely  want to load the search.js after the page is loaded as it can be pretty big

FIXME add a more complex example here with aync load.

## Dependencies
This plugin requires the following plugins:

- nlp: core nlp part of sitefab that do all the terms extraction
- js_posts: Provide a javascript representation of the posts used for display

## See also
if you wish to add aucomplete to your search then look at the `autocomplete` plugin.

## Changelog
- 06/01/17
    - Refactored to use the nlp and js_posts plugins making the search more modular, lighter and faster.
    - Reworked the doc and examples to simplify it.

- 12/29/16
    - Added search via parameter
    -  Added TFIDF top keywords which can be parameterized via the config
    - Added a fully working example in the documentation

- 12/27/16 
    - intial version

## Credits

**Author**: Elie Bursztein

Leverage ElasticLunr: https://github.com/weixsong/elasticlunr.js
