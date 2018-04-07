# Outline

##Abstract
- Encryption plugin for VIM.

##Introduction
- VIM's existing encryption functionality is limited in configuration options.

##Background and/or Related Work
- VIM -x

##Methodology
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

##Resources

- Learn VimScript the Hard Way `http://learnvimscriptthehardway.stevelosh.com/chapters/53.html`
- Vim Documentation: Autocmd `http://vimdoc.sourceforge.net/htmldoc/autocmd.html`
- Vim Documentation: Python `http://vimdoc.sourceforge.net/htmldoc/if_pyth.html`