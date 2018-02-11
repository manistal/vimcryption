
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
    exec py "import vimcryption"
    exec py "vimcryption.hello()"
endfunc

" *Note* All user defined commands and functions
"        must start with an upper case letter
command! Vimcrypt call Vimcrypt()
