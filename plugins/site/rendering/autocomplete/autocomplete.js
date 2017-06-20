
var Octopi = function(words) {
  this.uid = 0;
  this.tree = {$$: []};
  this.table = {};
  words = (words || []);
  for (var i = 0; i < words.length; i++)
    this.add(words[i]);
};

/**
* Take serialized Octopi data as string and initialize the Octopi object
* @param json String The serialized Octopi trie
*/
Octopi.load = function(json){
    var oct = new Octopi();
    var o = JSON.parse(json);
    oct.uid = o.uid;
    oct.tree = o.tree;
    oct.table = o.table;
    return oct;
  }

Octopi.prototype = {
  constructor: Octopi,
  /**
     * Add a new element to the trie
     * @param key String prefix to look up
     * @param data Object returned by trie
     */
  add: function(key, data) {
    var id = ++this.uid;
    var sub = this.tree;

    this.table[id] = data || key;
    sub.$$.push(id);

    for (var i = 0; i < key.length; i++) {
      var c = key[i];
      sub = sub[c] || (sub[c] = {$$:[]});
      sub.$$.push(id);
    }
  },

  /**
     * Return the list of elements in the trie for a given query
     * @param key String The prefix to lookup
     */
  get: function(key) {
    var sub = this.tree;
    var tbl = this.table;
    for (var i = 0; i < key.length; i++)
      if (!(sub = sub[key[i]]))
        return [];

    return sub.$$.map(function(id) {
      return tbl[id];
    });
  },
  /**
     * Serialize the Octopi trie as string
     *
     * @return String
     */
  serialize: function(){
    var o = { uid: this.uid, 
              tree: this.tree,
              table: this.table
            }
    return JSON.stringify(o);

  }
};

//Search core code
var trie_data = AUTOCOMPLETE_PLUGIN_REPLACE;

var Autocomplete = function() {
  this.oct = new Octopi();
};

Autocomplete.prototype = {
  load_data: function(data) {
    for (var i = 0; data[i]; i++) {
      var info = {
        'w': data[i][0],
        'd': data[i][1],
        's': data[i][2]
      }
      this.oct.add(data[i][0], info)
    }
  },

  get: function(str) {
    // Fixme: cleanup malicious input
    var candidates = this.oct.get(str);
    return candidates.sort(function(a,b){
        return (a.s < b.s) ? 1: -1;
     }
    );
  }
};

// Export needed functions/data to the global context
window.Autocomplete = Autocomplete;
window.trie_data = trie_data;
