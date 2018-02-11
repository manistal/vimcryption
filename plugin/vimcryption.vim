
" Get current plugin path
let g:plugin_path = expand('<sfile>:p:h')

" Always check to make sure dependancies are satisified 	
if !has('python')
    echo "Vim has to be compiled with +python to run this!" 
    finish
endif

" It seems like Python3 is hard to come by in vim
" if !has('py3')
"     echo "Python 3 is required to run vimcryption!"
"     finish
" endif


" This is just one way to invoke python
" you can also call 'pyfile' or 'python << EOF' 
function! Vimcrypt()

" Found a good importing example here:
" https://robertbasic.com/blog/import-custom-python-modules-in-vim-plugins/
python << endpython

import os
import sys
import vim

# Get the Vim variable to Python
plugin_path = vim.eval("g:plugin_path")
# Append it to the system paths
sys.path.append(plugin_path)

# And import!
import vimcryption
vimcryption.hello()
endpython

endfunc

" *Note* All user defined commands and functions
"        must start with an upper case letter
command! Vimcrypt call Vimcrypt()
