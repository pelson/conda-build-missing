conda-build-missing
-------------------
A tool for building a collection of conda recipes, without re-building those which already have matching built distribtuions.
Unlike conda build, which only has the abilty to build "build-time" dependencies, conda-build-missing will build all of the "build" and "run" dependencies in an appropriate order.

Docs
----

```
$> conda-build-missing --help

usage: Build all of the recipes (found recursively within the given directories)
       which are not already available in the build cache.

[-h] recipes_roots [recipes_roots ...]

positional arguments:
  recipes_roots  The root of where all recipes are found.

optional arguments:
  -h, --help     show this help message and exit
```
