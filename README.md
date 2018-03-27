# vimcryption

Encryption plugin for VIM.

## Links 

https://robertbasic.com/blog/import-custom-python-modules-in-vim-plugins/

https://www.ibm.com/developerworks/library/l-vim-script-5/index.html

### Intercept all File Reads and Writes

We're an encryption app, so we've gotta keep solid tabs on all data storage. We can do this in a vim plugin via special event callbacks known as *Cmd-Events*:

```
When using one of the "*Cmd" events, the matching autocommands are expected to
do the file reading, writing or sourcing.  This can be used when working with
a special kind of file, for example on a remote system.

CAREFUL: If you use these events in a wrong way, it may have the effect of
making it impossible to read or write the matching files!  Make sure you test
your autocommands properly.  Best is to use a pattern that will never match a
 normal file name, for example "ftp://*".

When defining a BufReadCmd it will be difficult for Vim to recover a crashed
editing session.  When recovering from the original file, Vim reads only those
parts of a file that are not found in the swap file.  Since that is not
possible with a BufReadCmd, use the |:preserve| command to make sure the
original file isn't needed for recovery.  You might want to do this only when
you expect the file to be modified.

For file read and write commands the |v:cmdarg| variable holds the "++enc="
and "++ff=" argument that are effective.  These should be used for the command
that reads/writes the file.  The |v:cmdbang| variable is one when "!" was
used, zero otherwise.

See the $VIMRUNTIME/plugin/netrwPlugin.vim for examples.
```

The ones we care about:
http://vimdoc.sourceforge.net/htmldoc/autocmd.html#BufWriteCmd
```
|BufWriteCmd|		before writing the whole buffer to a file |Cmd-event|
|FileWriteCmd|		before writing part of a buffer to a file |Cmd-event|
|FileAppendCmd|		before appending to a file |Cmd-event|

|BufReadCmd|		before starting to edit a new buffer |Cmd-event|
|FileReadCmd|		before reading a file with a ":read" command |Cmd-event|
```

### Tell Vimcryption what to do

We'll need the user to be able to add keys, remove keys, set file perms,  bind commands
