
minimum effort bughunt in shellscripts included in portage tree

# Requirements

* click
* python-bugzilla
* shellcheck


# Usage

* set PORTDIR glob in shellbug.py (default: "/usr/portage/**")
* run

```
$ ./shellbug.py
```

output.json will contain shellcheck results
