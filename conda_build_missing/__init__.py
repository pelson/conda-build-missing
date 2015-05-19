#!/usr/bin/env python
import os
import shutil
import sys

import conda.api
import conda.config
from conda.lock import Locked
from conda.utils import url_path
import conda_build.config
from conda_build.metadata import MetaData
import conda_build.build as build_module


docstr = """
Build all of the recipes (found recursively within the given directories)
which are not already available in the build cache.

""".strip()


def sort_dependency_order(metas):
    """Sort the metas into the order that they must be built."""
    meta_named_deps = {}
    buildable = [meta.name() for meta in metas]
    for meta in metas:
        all_deps = (meta.get_value('requirements/run', []) +
                    meta.get_value('requirements/build', []))
        # Remove version information from the name.
        all_deps = [dep.split(' ', 1)[0] for dep in all_deps]
        meta_named_deps[meta.name()] = [dep for dep in all_deps if dep in buildable]
    sorted_names = list(resolve_dependencies(meta_named_deps))
    return sorted(metas, key=lambda meta: sorted_names.index(meta.name()))


def resolve_dependencies(package_dependencies):
    """
    Given a dictionary mapping a package to its dependencies, return a
    generator of packages to install, sorted by the required install
    order.

    >>> deps = resolve_dependencies({'a': ['b', 'c'], 'b': ['c'],
                                     'c': ['d'], 'd': []})
    >>> list(deps)
    ['d', 'c', 'b', 'a']

    """
    remaining_dependencies = package_dependencies.copy()
    completed_packages = []

    # A maximum of 10000 iterations. Beyond that and there is probably a
    # problem.
    for failsafe in xrange(10000):
        for package, deps in sorted(remaining_dependencies.copy().items()):
            if all(dependency in completed_packages for dependency in deps):
                completed_packages.append(package)
                remaining_dependencies.pop(package)
                yield package
            else:
                # Put a check in to ensure that all the dependencies were
                # defined as packages, otherwise we will never succeed.
                for dependency in deps:
                    if dependency not in package_dependencies:
                        msg = ('The package {} depends on {}, but it was not '
                               'part of the package_dependencies dictionary.'
                               ''.format(package, dependency))
                        raise ValueError(msg)

        # Close off the loop if we've completed the dependencies.
        if not remaining_dependencies:
            break
    else:
        raise ValueError('Dependencies could not be resolved. '
                         'Remaining dependencies: {}'
                         ''.format(remaining_dependencies))


def build(meta, test=True):
    """Build (and optionally test) a recipe directory."""
    with Locked(conda_build.config.croot):
        meta.check_fields()
        if os.path.exists(conda_build.config.config.info_dir):
            shutil.rmtree(conda_build.config.config.info_dir)
        build_module.build(meta, verbose=False, post=None)
        if test:
            build_module.test(meta, verbose=False)
        return meta


def find_all_recipes(directories):
    possible_metas = set(['meta.yml', 'meta.yaml'])
    for directory in directories:
        for root, dirs, files in os.walk(os.path.expanduser(directory)):
            if set(files).intersection(possible_metas):
                yield MetaData(os.path.join(root))


def build_missing_metas(metas):
    metas = sort_dependency_order(metas)

    if os.path.exists(conda_build.config.config.bldpkgs_dir):
        # Get hold of just the built packages.
        index = conda.api.get_index([url_path(conda_build.config.config.croot)],
                                    prepend=False)
    else:
        # There are no built packages yet.
        index = {}

    already_builts = [meta for meta in metas
                      if '{}.tar.bz2'.format(meta.dist()) in index]
    needs_building = [meta for meta in metas
                      if '{}.tar.bz2'.format(meta.dist()) not in index]

    print('-' * 60)
    if already_builts:
        print('Packages which are already built:\n    ' +
              '\n    '.join(meta.name() for meta in already_builts))
    if needs_building:
        print('Packages which will be built (in order):\n    ' +
              '\n    '.join(meta.name() for meta in needs_building))
    print('-' * 60)
    for meta in needs_building:
        build(meta, test=True)


def main():
    import argparse
    parser = argparse.ArgumentParser(docstr)
    parser.add_argument("recipes_roots",
                        help="The root of where all recipes are found.",
                        nargs='+')
    args = parser.parse_args()
    metas = list(find_all_recipes(args.recipes_roots))
    build_missing_metas(metas)
