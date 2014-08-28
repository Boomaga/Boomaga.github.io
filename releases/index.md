---
layout: default
title: Boomaga - release notes
menuItem: Download
---

Boomaga release notes
=========
<br>

{% for post in site.categories.releases limit 5 %}
{{ post.content }}
<i style="font-weight: normal; font-size: 90%;">{{ post.date | date_to_string}}</i>
<br>
{% endfor %}
