
" Get current plugin path
let g:plugin_path = expand('<sfile>:p:h')

" Always check to make sure dependancies are satisified 	
" eventually we should also check if we're enabled
if has('python3')
    " command! VCPython python3
elseif has('python')
    " command! VCPython python
else 
    echo "Vim has to be compiled with +python to run this!" 
    finish
endif


" Load the python libraries when the plugin is loaded
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))
python import vimcryption 
python VCF = vimcryption.VCFileHandler()


" Overload Write/Read commands for vimcryption
augroup Vimcryption
  au! 
  au BufReadCmd    *    py VCF.BufRead()
  au FileReadCmd   *    py VCF.FileRead()
  au BufWriteCmd   *    py VCF.BufWrite()
  au FileWriteCmd  *    py VCF.FileWrite()
  au FileAppendCmd *    py VCF.FileAppend()
augroup END 
 

" " *Note* All user defined commands and functions
" "        must start with an upper case letter
" command! Vimcrypt call Vimcrypt()
" au BufEnter * call LoadVimcrypt()
