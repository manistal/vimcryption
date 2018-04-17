
" Python2 or Python3 Support Required
if has('python3')
    command! -nargs=1 Python python3 <args>
elseif has('python')
    command! -nargs=1 Python python <args>
else
    echo "Error: Requires Vim compiled with +python or +python3"
    finish
endif

" Load the Python Libraries
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))
python sys.path.append(vim.eval('expand("<sfile>:h")') + "/..")
python import vimcryption

" Enable Vimcryption Crypto Functionality 
function LoadVimcryption()

    " Disable writing plaintext SWAP/backup/undo files 
    setl noswapfile
    setl noundofile
    setl nobackup

    " make sure nothing is written to ~/.viminfo while editing
    " let g:vc_original_viminfo = &viminfo
    set viminfo=

    " Load the python libraries, construct VCFileHandler 
    python VCF = vimcryption.VCFileHandler()

    " Overload the File Access 
    augroup Vimcryption
        au! 
        au BufReadCmd    *    py VCF.BufRead()
        au FileReadCmd   *    py VCF.FileRead()
        au BufWriteCmd   *    py VCF.BufWrite()
        au FileWriteCmd  *    py VCF.FileWrite()
        au FileAppendCmd *    py VCF.FileAppend()
    augroup END 

endfunction

" Disable vimcryption and unload hooks
function UnloadVimcryption()
    augroup Vimcryption
        au! 
    augroup END 

    setl swapfile
    setl undofile
    setl backup
    " set viminfo= &vc_origin_viminfo
endfunction

" User API 
command! Vimcrypt call LoadVimcryption() | echo "Vimcryption Enabled!"
command! NoVimcrypt call UnloadVimcryption() | echo "Vimcryption Disabled!"

call LoadVimcryption()
