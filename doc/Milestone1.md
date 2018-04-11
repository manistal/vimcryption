# Outline

## Abstract
The prospect of writing a cryptographic application started out simply; code something up capable of encrypting and decrypting content.  The idea of encrypting messages quickly expanded into encryption of notes, or entire files.  This generalization of target content led us to the idea of a platform-independent editor plugin that could handle encryption of arbitrary data.  The choice of editor was clear: VIM. It runs on many platforms and can execute Python through it's vimconfig and plugin interfaces.  This plugin registers file io handling functions with VIM which replace the default ones.  All disk access from the editor is thus routed through this plugin, ensuring that all externally observable data is put through an encryption engine, including temporary files.

## Introduction
Any encryption plugin needs to be flexibly architected so that it can keep up with the cryptographic arms race.  To support this, we identified two main areas of development.  The first is the VIM interface, which describes to the editor what our library will be responsible for.  The second is an extensible encryption library that can handle file IO.

- VIM's existing encryption functionality is limited in configuration options.

The encryption library is based on Encryption Engines, which implement the header processing and encryption/decryption APIs.  Once a file is loaded and the header is processed, if that file requires vimcryption, the necessary Engine is loaded.  That engine is then handed the file handle to scan for any additional meta-data it requires.  Any sybsequent disk reads are done through EncryptionEngine.decrypt(file_descriptor, buffer) and disk writes through EncryptionEngine.encrypt(buffer, file_descriptor).

## Background 

Vim provides some builtin encryption functionality that can be used with the `-x` argument on the commandline and `:X` command in Vim, which both will prompt you for a key with which to encrypt the file. Vim supports 3 ciphers (`Pkzip`, `blowfish`, and `blowfish2`) and by default will use `Pkzip` which the `:help encryption` documentation in vim describes as "The algorithm used is breakable. A 4 character key in about one hour, a 6 character key in one day (on a Pentium 133 PC).". Blowfish is also compromised but fixed in blowfish2. Blowfish2 provides strong encryption but is vunerable to undetected modification. [4] 

Vim's script repository has also published a plugin which passes through file reads and rights to the Gnu Privacy Guard suite, known as `gnupg.vim`. The plugin implements encryption by attaching commandline GPG calls to Vim's "cmd-event" triggers which allow plugins to overload filesystem operations. The dependancy on Gnu Privacy Guard being installed greatly reduces the value of the plugin compared to a stand-alone solution. [5]

We also searched `https://vimawesome.com/`, the largest directory of vim plugins on the web, for any plugins which implement encryption. The only plugin related to cryptography available at this time is for cryptographic checksums. Vim appears to lack cross platform, configurable, and secure encryption functionality. Vimcryption attempts to address this need as a self-contained python based plugin. 


## Methodology
- Setup VIM disk access hooks
    - File Read
    - Buffer Read
    - File Write
    - Buffer Write
    - File Append
- Define Encrypt and Decrypt API
    - EncryptionEngine
        - encrypt(buffer, file)
        - decrypt(file, buffer)
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

[5] Markus Braun, James McCoy. "gnupg.vim" (2012) GitHub Repository.
https://github.com/vim-scripts/gnupg.vim
