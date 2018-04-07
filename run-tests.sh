# Python 2 testing
# Set up a Python 2 virtual environment.
echo "-BEGIN- Python 2 Testing."
echo "    Creating Python2 virtual envrionment in test/venv2..."
rm -rf test/venv2
virtualenv -p python test/venv2
echo "    done."
alias python="test/venv2/bin/python"
alias pip="test/venv2/bin/pip"
echo "    Installing vimcryption into venv2..."
pip install nose2
python testsetup.py install
echo "    done."
echo "--END-- Python 2 Testing."
echo
echo

# Python 3 testing
# Set up a Python 3 virtual environment.
echo "-BEGIN- Python 3 Testing."
echo "    Creating Python3 virtual envrionment in test/venv3..."
rm -rf test/venv3
virtualenv -p python3 test/venv3
echo "    done."
alias python="test/venv3/bin/python3"
alias pip="test/venv3/bin/pip"
echo "    Installing vimcryption into venv3..."
pip install nose2
python testsetup.py install
echo "    done."
echo "--END-- Python 3 Testing."
echo
echo
