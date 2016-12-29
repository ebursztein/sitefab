# Search Plugin

Create a search page that allows to search through the post locally in pure javascript

## Usage

The simplest way to add search to a page is to add:

```html

        <input id="searchbox" type="search" value="" placeholder="search" size="30">
        <div id="search_results"></div>

        <script src="static/js/search.js"></script>
        <script>
            var search_results = document.getElementById('search_results');

            function search_callback(docs, query) {
                /* Function called with search results
                @param docs: the list of doc that matches the query
                @param query: the query string
                */
                html = "<ul>"
                for (var i = 0; docs[i]; i++) {
                    doc = docs[i];
                    html += "<li>[" + doc.score + "]" + doc.title + "</li>";
                }
                html += "</ul>" 
                search_results.innerHTML = html;
            }

            search_init("searchbox", search_callback);
        </script>

```

Note you most likely  want to load the search.js after the page is loaded as it can be pretty big

FIXME add a more complex example here with aync load.

## Changelog

- 12/27/16 intial version

## Credits

**Author**: Elie Bursztein

List library here