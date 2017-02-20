# plugins list
List of available plugins

|Name | Description | dependencies|
|-----|:------------|:------------|
| [Post linter](/plugins/post/processor/post_linter/README.md) | Check posts for errors |  |
| [Read time](/plugins/post/processor/read_time/README.md) | Compute how long it will take to read a given post |  |
| [Directory copier](/plugins/site/preparsing/copy_dir/README.md) | Copy directories |  |
| [Backup Media](/plugins/post/processor/backup_media/README.md) | Backup all the files listed in .md in a backup directory (images,pdf) |  |
| [Related Posts]() | Use LSI to compute related posts. |  |
| [Sort collections](/plugins/collection/processor/sort_collection/README.md) | Sort collections by publication time to allow easy chronological display from templates. |  |
| [Jsonld Collection](/plugins/collection/processor/jsonld_collection/README.md) | Compute Jsonld object for each collection based on meta | compute_full_collection_url |
| [Post full url](/plugins/post/processor/compute_full_post_url/README.md) | Compute the full qualified url for each post and store in the post.meta under full_url |  |
| [Jsonld](/plugins/post/processor/jsonld/README.md) | Compute Jsonld object for each page based on meta | compute_full_post_url |
| [Search page](/plugins/site/rendering/search/README.md) | Generate a search page that run locally |  |
| [RSS](/plugins/site/rendering/rss/README.md) | RSS | compute_full_post_url |
| [Responsive Images](/plugins/site/preparsing/reponsive_images/README.md) | Create responsive images by using the picture element and creating multiple resolutions images | copy_dir |
| [Collection full url](/plugins/collection/processor/compute_full_collection_url/README.md) | Compute the full qualified url for collection |  |
| [Sitemap](/plugins/site/rendering/sitemap/README.md) | Generate Sitemap | compute_full_post_url, compute_full_collection_url |
