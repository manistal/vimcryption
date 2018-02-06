
# Vim Plugin to Encrypt Files
#### Authors: Thomas Manner, Miguel Nistal 

For our final project we plan to implement a Vim plugin to apply encryption to working with files in the editor. In order for the project to have real-world value the plugin has to be aware of and encrypt both the file being editted when it's saved as well as any intermediate swap files created in the process of editing the file. This plugin will be a full service encryption application that allows you to encrypt new files, safely interact and edit already encrypted files, and save existing files as encrypted. The plugin will be broken down into several components in order to handle both the encryption code and the vim api. 

## Keys and Authentication 

Since most users of Vim already have SSH configured in their home directory, we can use SSH RSA keys to do the encryption. It also means we don't have to implement key generation code and directory protections like SSH already does for us. We can also add the ability to add other users public keys (similar to how GitHub keys work) to allow your friends to work on files that you share together. Added others public keys to Vim would probably be done via an extra buffer you can bring up via a vim command. 

## The Vimscript Plugin Interface

All Vim plugins require some vimscript to interact with the editor itself and load the backend code. This plugin will include the bare minimum vimscript code to be compliant with modern vim plugin managers (such as vundle), allow users to interact with the plugin and bind commands, take key input, and intercept buffers before they're flushed to disk. 

## The Python Encryption Backend

Since Vim natively supports Python based plugins, we'll be writing the heavy lifting code in Python. 
