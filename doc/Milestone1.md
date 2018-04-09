# Outline

## Abstract
- Encryption plugin for VIM.

## Introduction
- VIM's existing encryption functionality is limited in configuration options.

## Background and/or Related Work

Vim provides some builtin encryption functionality that can be used with the `-x` argument on the commandline and `:X` command in Vim, which both will prompt you for a key with which to encrypt the file. Vim supports 3 ciphers (`Pkzip`, `blowfish`, and `blowfish2`) and by default will use `Pkzip` which the `:help encryption` documentation in vim describes as "The algorithm used is breakable. A 4 character key in about one hour, a 6 character key in one day (on a Pentium 133 PC).". Blowfish is also compromised but fixed in blowfish2. Blowfish2 provides strong encryption but is vunerable to undetected modification. [4] 


## Methodology
- Setup VIM disk access hooks
    - File Read
    - Buffer Read
    - File Write
    - Buffer Write
    - File Append
- Define Encrypt and Decrypt API
    - EncryptionEngine
        - encrypt(buffer)
        - decrypt(file)
- Add Password or Key support

## Resources

[1] Losh, Steve. "Learn Vimscript the Hard Way." Learn Vimscript the Hard Way. Accessed March 08, 2018.
http://learnvimscriptthehardway.stevelosh.com/.

[2] "Vim Documentation: Autocmd" vimdoc. Accessed March 08, 2018. 
http://vimdoc.sourceforge.net/htmldoc/autocmd.htm 

[3] "Vim Documentation: Python Module" vimdoc. Accessed March 08, 2018. 
http://vimdoc.sourceforge.net/htmldoc/if_pyth.htm 

[4] "Encryption" Vim Tips Wiki. Accessed March 08, 2018.
http://vim.wikia.com/wiki/Encryption
