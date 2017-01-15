---
template: code
title: "Code highlighting demo"
creation_date: 29 jul 2001 00:00
update_date: 20 nov 2016 18:01
microdata_type: WebPage
lang: en


permanent_url: "code"

authors:
  - Elie, Bursztein

abstract: "Demo of the code highlighting"

---
# Python
with language specified:

```python
def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))
```


with the language guessed
```
def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))
```

# Ruby 

```ruby
def hammingDistance(s1, s2)
    raise "ERROR: Hamming: Non equal lengths" if s1.length != s2.length
    (s1.chars.zip(s2.chars)).count {|l, r| l != r}
end
```

