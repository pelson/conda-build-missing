conda-build-missing
-------------------
A tool for building a collection of conda recipes, without re-building those which already have matching built distribtuions.
Unlike conda build, which only has the abilty to build "build-time" dependencies, conda-build-missing will build all of the "build" and "run" dependencies in an appropriate order.

Installation
------------
From conda: ```conda install -c pelson conda-build-missing```

From source: ```python setup.py install```

Documentation
-------------

```
$ conda-build-missing --help

usage: Build all of the recipes (found recursively within the given directories)
       which are not already available in the build cache.

[-h] recipes_roots [recipes_roots ...]

positional arguments:
  recipes_roots  The root of where all recipes are found.

optional arguments:
  -h, --help     show this help message and exit
```

Example
-------

The following example produces a directory of 3 recipes, a|b|c, which have dependencies. 

```
$ mkdir -p example-recipes/a example-recipes/b example-recipes/c

$ cat <<EOF > example-recipes/a/meta.yaml
package: 
  name: a
requirements:
  run:
    - b
EOF

$ cat <<EOF > example-recipes/b/meta.yaml
package: 
  name: b
requirements:
  build:
    - c
EOF

$ cat <<EOF > example-recipes/c/meta.yaml
package: 
  name: c

EOF
```

Running conda-build-missing on the directory containing these recipes results the in the packages being built in a sensible order.

```
$ conda-build-missing ./example-recipes
------------------------------------------------------------
Packages which will be built (in order):
    c
    b
    a
------------------------------------------------------------
BUILD START: c
...
BUILD START: b
...
BUILD START: a
```

Re-running conda-build-missing results in no further building taking place, as their associated built distributions are available in the conda-build directory.

```
$ conda-build-missing ./example-recipes
------------------------------------------------------------
Packages which are already built:
    c
    b
    a
------------------------------------------------------------
```
