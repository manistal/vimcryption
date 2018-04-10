# Outline

## Abstract
- Encryption plugin for VIM.

## Introduction
- VIM's existing encryption functionality is limited in configuration options.

## Background 

Vim provides some builtin encryption functionality that can be used with the `-x` argument on the commandline and `:X` command in Vim, which both will prompt you for a key with which to encrypt the file. Vim supports 3 ciphers (`Pkzip`, `blowfish`, and `blowfish2`) and by default will use `Pkzip` which the `:help encryption` documentation in vim describes as "The algorithm used is breakable. A 4 character key in about one hour, a 6 character key in one day (on a Pentium 133 PC).". Blowfish is also compromised but fixed in blowfish2. Blowfish2 provides strong encryption but is vunerable to undetected modification. [4] 

Vim's script repository has also published a plugin which passes through file reads and rights to the Gnu Privacy Guard suite, known as `gnupg.vim`. The plugin implements encryption by attaching commandline GPG calls to Vim's "cmd-event" triggers which allow plugins to overload filesystem operations. The dependancy on Gnu Privacy Guard being installed greatly reduces the value of the plugin compared to a stand-alone solution. [5]

We also searched `https://vimawesome.com/`, the largest directory of vim plugins on the web, for any plugins which implement encryption. The only plugin related to cryptography available at this time is for cryptographic checksums. Vim appears to lack cross platform, configurable, and secure encryption functionality. Vimcryption attempts to address this need as a self-contained python based plugin. 


## Methodology

In it's role as a text editor, Vim is directly responsible for all the file operations a user need in order to interact with the filesystem. Additionally, Vim provides quality of life features to the user such as swap and backup files in case the session is interrupted or corrupted, undo files so the user can have a persistant undo stack, and logs command history so the user can repeat commands used earlier. To implement a secure encryption extension to Vim, we need to take into account the entire dataflow to ensure that plaintext is not visible outside of the active memory of the editor's process. 

Securing the unintential leak of plaintext data via temporary files is relatively simple in Vim. As discussed in the Vim Tips Wiki, we can disable the creation of temporary files by using vim-script in our plugin load [4]:  

```
    setl noswapfile
    setl noundofile
    setl nobackup
    set viminfo=
```

It's important to note that the above commands use the `setl` syntax which means "set local to the buffer". Since we want users to be able to work on encrypted and unencryted files simultaneously, we need to ensure that any plugin configurations don't effect other active files. 

Intercepting the actual reading and writing of the buffer is directly supported by Vim through through the use of Command-Events, which are specialized Auto-Commands that specifically allow the overloading of filesystem triggers. [2] We can then tie these file system triggers to event handlers in Python and write/read the file system and buffer directly through a file handler there. 

```
    au BufReadCmd    *    py VCF.BufRead()
    au FileReadCmd   *    py VCF.FileRead()
    au BufWriteCmd   *    py VCF.BufWrite()
    au FileWriteCmd  *    py VCF.FileWrite()
    au FileAppendCmd *    py VCF.FileAppend()
```

The Python based file handler is connstructed at the same time the auto-commands are registered and loads user settings from pre-defined user variables that can be set in the configurations file (`.vimrc`) or via the command prompt inside of vim. When the FileHandler is constructed it instantiates a Read/Write Engine using the strategy design pattern based on the encyrption method the user would like to use (or that the file metadata specifies). 


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

[5] Markus Braun, James McCoy. "gnupg.vim" (2012) GitHub Repository.   
https://github.com/vim-scripts/gnupg.vim
