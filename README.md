# subset-gf-icons
Exploratory hacking around subsetting a Google-style icon font

# Sample usage

Assumes `https://github.com/google/material-design-icons` is cloned in a directory sibling to your
subset-gf-icons repo.

```shell
# Establish a virtual environment
$ pip install -e .
$ subset_gf_icons ../material-design-icons/font/MaterialIcons-Regular.ttf menu alarm_on
$ ttx -o - ../material-design-icons/font/MaterialIcons-Regular-subset.ttf

# Note that there is no ligature for "alarm", only alarm_on
# The original MaterialIcons-Regular.ttf is 279K, MaterialIcons-Regular-subset.ttf is 1.5K
```