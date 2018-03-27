
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
" Found a good importing example here:
" https://robertbasic.com/blog/import-custom-python-modules-in-vim-plugins/
" function! LoadVimcrypt()
" python << endpython
" 
" import os
" import sys
" import vim
" 
" # Get the Vim variable to Python
" plugin_path = vim.eval("g:plugin_path")
" # Append it to the system paths
" sys.path.append(plugin_path)
" 
" # And import!
" import vimcryption as vc
" 
" endpython
" endfunc
" 
" function! Vimcrypt()
" python << endpython
" 
" vim.current.buffer.append("LOL")
" print vc.FileRead()
" 
" endpython
" endfunc
" 
" " *Note* All user defined commands and functions
" "        must start with an upper case letter
" command! Vimcrypt call Vimcrypt()
" au BufEnter * call LoadVimcrypt()

python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))
python import vimcryption 
python VCF = vimcryption.VCFileHandler()


" https://www.ibm.com/developerworks/library/l-vim-script-5/index.html
" Overload Write/Read commands for vimcryption
augroup Vimcryption
  au! 
  au BufReadCmd    *    py VCF.BufRead()
  au FileReadCmd   *    py VCF.FileRead()
  au BufWriteCmd   *    py VCF.BufWrite()
  au FileWriteCmd  *    py VCF.FileWrite()
"  au FileAppendCmd *    py VCF.FileAppend()
augroup END 
 


