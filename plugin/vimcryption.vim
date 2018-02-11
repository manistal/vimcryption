    
	
if !has('python')
    echo "Vim has to be compiled with +python to run this!" 
    finish
endif

" It seems like Python3 is hard to come by in vim
" if !has('py3')
"     echo "Python 3 is required to run vimcryption!"
"     finish
" endif

function! Vimcrypt()
    exec py "import vimcryption"
    exec py "vimcryption.hello()"
endfunc

command! vimcrypt call Vimcrypt()
