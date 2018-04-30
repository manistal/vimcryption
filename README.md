# Vimcryption

[![Build Status](https://travis-ci.org/Vipyr/vimcryption.svg?branch=master)](https://travis-ci.org/Vipyr/vimcryption)
[![Maintainability](https://api.codeclimate.com/v1/badges/c04c09507b66dc7fa5ad/maintainability)](https://codeclimate.com/github/Vipyr/vimcryption/maintainability)
[![codecov](https://codecov.io/gh/Vipyr/vimcryption/branch/master/graph/badge.svg)](https://codecov.io/gh/Vipyr/vimcryption)

Vimcryption is an extensible cross-platform Python based plugin to do encryption in Vim. Inspired by previous Vim
Encryption efforts (http://vim.wikia.com/wiki/Encryption), that lack up-to-date algorithms, or portability, this plugin
is designed to give users the flexibility to survive the cryptographic arms race.

## Installation

If using [Vundle](https://github.com/VundleVim/Vundle.vim) to install, add the following to your `.vimrc`:

```
Plugin `Vipyr/vimcryption`
```

If you're using [Pathogen](https://github.com/tpope/vim-pathogen) :

```
git clone https://github.com/Vipyr/vimcryption.git ~/.vim/bundle/vimcryption
```

## Configuration

You can configure Vimcryption defaults in your `.vimrc`:

```
" Default Cipher to Use When Encrypting
let g:vimcryption_cipher_type = "AES128"

" You can disable automatic loading of Vimcryption and only load on demand
let g:vimcryption_start_onload = 0
```

## Usage

To enable Vimcryption with a specific cipher and write the encrypted file:

```
:Vimcrypt AES128
:write
```

To enable Vimcryption with your default cipher:

```
:Vimcrypt
```

To disable Vimcryption and unload the plugin:
```
:NoVimcrypt
```

## Contributing

To contribute to Vimcryption, fork from https://github.com/Vipyr/vimcryption and clone to your local computer. Unit
tests require a Python3 and Python2 installation with nose2. To run unit tests:

```
cd vimcryption
./run_tests.sh
```
