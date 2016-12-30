# Search Plugin

Create a search page that allows to search through the post locally in pure javascript

## Usage

Here is a simple search page that allows to search  via an inputbox and via the query parameter **q**:

```html

<html>
    <head>
        <script src="/static/js/search.js"></script>
    </head>
    <body>
        <input id="searchbox" type="search" value="" placeholder="search" size="30">
        <div id="search_results"></div>


        <script>

            var search_results = document.getElementById('search_results') 

            function search_callback(docs, query) {
                /* Function called with search results
                @param docs: the list of doc that matches the query
                @param query: the query string
                */
                html = "<ul>"
                for (var i = 0; docs[i]; i++) {
                    doc = docs[i];
                    html += '<li><a href="'+ doc.permanent_url + '"> [' + doc.score + "]" + doc.title + "</a></li>";
                }
                html += "</ul>" 
                search_results.innerHTML = html;
            }

            // to perform the search when the user an input box
            search_init("searchbox", search_callback);

            //to perform the search based of url parameters if needed
            query = getURLParameter('q');
            if (query) {
                results = search(query)
                search_callback(results, query);
            }
        </script>

    </body>
</html>

```

Note you most likely  want to load the search.js after the page is loaded as it can be pretty big

FIXME add a more complex example here with aync load.

## Changelog

- 12/29/16
    - Added search via parameter
    -  Added TFIDF top keywords which can be parameterized via the config
    - Added a fully working example in the documentation

- 12/27/16 
    - intial version

## Credits

**Author**: Elie Bursztein

List library here