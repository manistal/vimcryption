# Always recreate the gh-pages branch!
git checkout master
git checkout -B gh-pages master
DOCGEN=1 ./run-tests.sh $TRAVIS_PYTHON_VERSION
echo git add doc/
echo git commit -m "Travis CI updated python$TRAVIS_PYTHON_VERSION coverage report."
echo git push
