
" Python2 or Python3 Support Required
if has('python3')
    command! -nargs=1 Python python3 <args>
elseif has('python')
    command! -nargs=1 Python python <args>
else
    echo "Error: Requires Vim compiled with +python or +python3"
    finish
endif

" Default values for configs
if !exists("g:vimcryption_cipher")
  " Cipher to encrypt files with, default is nothing
  let g:vimcryption_cipher = "IOPASS"
endif

if !exists("g:vimcryption_start_onload")
  " Whether or not to enable the plugin when vim starts
  "  default is yes since we're working with security 
  let g:vimcryption_start_onload = 1
endif

" Load the Python Libraries
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))
python sys.path.append(vim.eval('expand("<sfile>:h")') + "/..")
python import vimcryption

" Enable Vimcryption Crypto Functionality 
function LoadVimcryption(...)

    " Disable writing plaintext SWAP/backup/undo files 
    setl noswapfile
    setl noundofile
    setl nobackup

    " make sure nothing is written to ~/.viminfo while editing
    " let g:vc_original_viminfo = &viminfo
    set viminfo=

    " Construct a new VCFileHandler when VC Loads
    python VCF = vimcryption.VCFileHandler()

    " If we're given a cipher type from the user, tell VCF to initialize it
    if a:0 > 0
        let b:vc_cipher_arg = a:1
        python VCF.setCipher(vim.eval('b:vc_cipher_arg'))
    endif

    " Overload the File Accessors with our VCF Callbacks
    augroup Vimcryption
        au! 
        au BufReadCmd    *    py VCF.BufRead()
        au FileReadCmd   *    py VCF.FileRead()
        au BufWriteCmd   *    py VCF.BufWrite()
        au FileWriteCmd  *    py VCF.FileWrite()
        au FileAppendCmd *    py VCF.FileAppend()
    augroup END 

    if !exists("b:vimcryption_loaded")
        let b:vimcryption_loaded = 1
    else
        redraw!
        echo "Vimcryption Enabled! " . b:vc_cipher_arg
    endif

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

    echo "Vimcryption Disabled!"
endfunction

" User API 
command! NoVimcrypt call UnloadVimcryption() 
command! -nargs=? Vimcrypt call LoadVimcryption(<f-args>) 

if g:vimcryption_start_onload
    call LoadVimcryption()
endif
