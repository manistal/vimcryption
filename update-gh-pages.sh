#!/usr/bin/env bash
# Always recreate the gh-pages branch!
BRANCH=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match 2> /dev/null || git rev-parse --short HEAD)
git fetch origin gh-pages
git remote -v
git branch -a
git checkout gh-pages
git pull -X theirs --no-edit
git merge -X theirs --no-edit master
DOCGEN=1 ./run-tests.sh $TRAVIS_PYTHON_VERSION
git status
git add doc/
git commit -m "Travis CI updated python$TRAVIS_PYTHON_VERSION coverage report on $(date)"
git push -u origin gh-pages
git checkout $BRANCH
