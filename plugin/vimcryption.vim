    
	
if !has('python')
    echo "Vim has to be compiled with +python to run this!" 
    finish
endif

if !has('python3')
    echo "Python 3 is required to run vimcryption!"
    finish
endif

function! Vimcrypt()
    exec py3 "import vimcryption"
    exec py3 "vimcryption.hello()"
endfunc

command! vimcrypt call Vimcrypt()
