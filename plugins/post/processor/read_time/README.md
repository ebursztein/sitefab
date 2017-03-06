# Reading Time Plugin

Compute how long the article will take to read for an average speed.

## Usage

Add the following snippet to your template to display the time it takes to read the post.

```html
{% if post.meta.read_time %}
{{ post.meta.read_time}} min read
{% endif %}
```

## Changelog

- 12/27/16 initial version

## Credits

**Author**: Elie Bursztein

Computation use [Medium formula](https://help.medium.com/hc/en-us/articles/214991667-Read-time):

>Read time is based on the average reading speed of an adult (roughly 275 WPM). We take the total word count of a post and translate it into minutes. Then, we add 12 seconds for each inline image.

>**Additional notes**: Our original read time calculation was geared toward “slow” images, like comics, where you would really want to sit down and invest in the image. This resulted in articles with crazy big read times. For instance, this article containing 140 images was clocking in at a whopping 87 minute read. So we amended our read time calculation to count 12 seconds for the first image, 11 for the second, and minus an additional second for each subsequent image. Any images after the tenth image are counted at three seconds.
