__do_tests() {
  echo "-BEGIN- Python $1 Testing."
  echo "    Creating Python$1 virtual envrionment in venv$1..."
  rm -rf venv$1
  virtualenv -p python venv$1
  echo "    done."
  PATH=venv$1/bin:$PATH
  echo "    Installing vimcryption into venv$1..."
  pip install nose2
  python testsetup.py install
  echo "    done."
  echo "--Running Tests--"
  nose2 -s plugin/
  echo "----Complete-----"
  echo "--END-- Python $1 Testing."
  echo
  echo
}

# Python 2 testing
# Set up a Python 2 virtual environment.
__do_tests 2
__do_tests 3

# Python 3 testing
# Set up a Python 3 virtual environment.
