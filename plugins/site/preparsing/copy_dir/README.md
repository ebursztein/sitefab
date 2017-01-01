# Copy directories

Allows to copy sub-directories from one place to another. 
Mostly used to copy assests to the release directory.

## Usage

Specify which directory to copy and its destination in the configuration file

### Configuration
For example
```yaml
copy_dir:
    - enable: True
    copy:
        - "assets/js > release/static/js"
```

will copy the content of the directory *assets/js* to  *release/static/js*


## Changlog

A simple list that list what changed. Something like:

- 12/23/16
 - Documentation updated to reflect how the plugin work

## Credit
Who wrote the plugin, which library it use, who got the idea etc.