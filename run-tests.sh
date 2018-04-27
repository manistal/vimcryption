#!/usr/bin/env bash
# run-tests.sh
#
# Sets up and runs unittests in each python environment it detects in the build files.


# Wrapper function that squashes stdout
__quiet() {
  "$@" > /dev/null
}


# Wrapper function that squashes both stdout and stderr
__silence() {
  (2>&1 > /dev/null "$@")
}


# Wrpper function that routes stdout to stderr
__stderr() {
  "$@" >&2
}


# Figure out the full interpreter path for a python version
__get_python_interpreter_path() {
  __python=python$1
  (> /dev/null which $__python 2>&1)
  if [ "$?" != "0" ] ; then
    if [ "$1" = "2" ] ; then
      __python=python
    fi
  fi
  (> /dev/null which $__python 2>&1)
  if [ "$?" = "0" ] ; then
    which $__python 
  else
    echo "NONE"
  fi
}


# Create a new virtual environment for a particular python version
__create_venv() {
  local __python
  __python=$(__get_python_interpreter_path $1)
  if [ "$__python" = "NONE" ] ; then
    __stderr echo "    python$1 not found!"
    exit 1
  else
    __virtualenv=$(dirname $__python)/virtualenv
    __silence $__virtualenv -v -p $__python .venv$1
    if [ "$?" != "0" ] ; then
      __virtualenv=$(which virtualenv)
      __silence $__virtualenv -v -p $__python .venv$1
      if [ "$?" != "0" ] ; then
        __stderr echo "    virtualenv executable not found for $__python!"
        exit 1
      fi
    fi
    . .venv$1/bin/activate
    __setup_venv $1
    __stderr echo "    python$1 ($__python) -> .venv$1"
  fi
}

__setup_venv() {
  pip install anybadge
  pip install coverage-badge
  pip install nose2
  pip install numpy
  pip install pylint
}


# Run PyLint
__do_pylint() {
  LOG_DIR=doc/coverage/python$1
  PYLINT_LOG=$LOG_DIR/pylint.report
  PYLINT_BADGE=$LOG_DIR/pylint.svg
  echo "PyLint: start ($PYLINT_LOG)"
  echo "Python $1" > $PYLINT_LOG
  echo "" >> $PYLINT_LOG
  __pylint_out=$(2>&1 pylint encryptionengine test plugin/vimcryption.py)
  __pylint_E=$(echo "$__pylint_out" | grep -c "E:")
  __pylint_W=$(echo "$__pylint_out" | grep -c "W:")
  __pylint_C=$(echo "$__pylint_out" | grep -c "C:")
  __pylint_R=$(echo "$__pylint_out" | grep -c "R:")
  __pylint_F=$(echo "$__pylint_out" | grep -c "F:")
  echo "$__pylint_out" >> $PYLINT_LOG
  __summary="PyLint: done  ($__pylint_E errors, $__pylint_W warnings, $__pylint_C conventions, $__pylint_R refactors, $__pylint_F fatals)"
  echo "$__summary" >> $PYLINT_LOG
  echo "" >> $PYLINT_LOG
  echo "" >> $PYLINT_LOG
  echo "$__summary"
  __rating_line=$(echo "$__pylint_out" | grep "Your code has been rated at ")
  __rating=$(echo "$__rating_line" | cut -d ' ' -f7 | cut -d '/' -f1)
  echo "  $__rating_line"
  echo
  rm -f $PYLINT_BADGE
  anybadge -l pylint -v $__rating -f $PYLINT_BADGE 2=red 4=orange 8=yellow 10=green
}


# Run unit tests
__do_tests() {
  echo "--Running Python$1 Tests--"
  python setup.py -q install --force
  nose2 --coverage encryptionengine/ -s test
  coverage html -d doc/coverage/python$1
  coverage-badge -o doc/coverage/python$1/coverage.svg
  coverage report
  coverage erase
  echo
  echo "---------Complete---------"
  echo
  echo
}


# Go through a simple yaml file and grab all python versions from it
__parse_yaml() {
  local yaml=($(cat $1))
  local token
  local capturing=0
  local capture_next=0
  declare -a versions
  for token in "${yaml[@]}" ; do
    if [ "$token" = "python:" ] ; then
      capturing=1
    elif [ $capturing -eq 1 ] ; then
      if [ $capture_next -eq 1 ] ; then
        echo "$token" | cut -c 2- | rev | cut -c 2- | rev
        capture_next=0
      elif [ "$token" = "-" ] ; then
        capture_next=1
      else
        capturing=0
      fi
    fi
  done
}


#
# Main body
#

__prefix="__quiet"
if [ "$1" = "-v" ] ; then
  __prefix=""
  shift 1
elif [ "$1" = "-s" ] ; then
  __prefix="__silence"
  shift 1
fi

# If we're just doing document generation, only do the unit tests for the given python version ($1)
if [ "$DOCGEN" != "" ] ; then
  # If we see a virtual env for this python version, activate it.
  if [ -e .venv$1 ] ; then
    . .venv$1/bin/activate
  fi
  $__prefix __setup_venv $1
  __do_pylint $1
  __do_tests $1
  exit 0
fi

# Enable dot glob so we will see any "hidden" yml files
shopt -s dotglob
__versions=($(__parse_yaml *.yml))
# Disable dot glob
shopt -u dotglob
# Get the array of version numbers
__versions=($(echo "${__versions[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ' | uniq))

echo "Setting up Python virtual environments"

declare -a __pids
declare -a __rcs
for __i in "${!__versions[@]}" ; do
  $__prefix __create_venv ${__versions[$__i]} &
  __pids[$__i]=$!
done


for __i in "${!__pids[@]}" ; do
  wait ${__pids[$__i]}
  __rcs[$__i]=$?
done

echo "done."
echo

for __i in "${!__rcs[@]}" ; do
  if [ "${__rcs[$__i]}" = "0" ] ; then
    __version="${__versions[$__i]}"
    . .venv$__version/bin/activate
    __do_pylint $__version
    __do_tests $__version
  fi
done
