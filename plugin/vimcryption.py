"""
The Vimcryption Plugin!
"""
# Standard Library
import os
# site-packages
import vim
# Vimcryption
from encryptionengine.engine import PassThrough
from encryptionengine.ciphers import CipherFactory, UnsupportedCipherException, NotVimcryptedException
from encryptionengine.aesutil import IncorrectPasswordException


def vc_prompt(message):
    """ Prompts the `vim` user for input.
    """
    vim.command('call inputsave()')
    vim.command("let user_input = inputsecret('" + message + " ')")
    vim.command('call inputrestore()')
    return vim.eval('user_input')


class VCFileHandler(object):
    """ The Vimcryption File Handler.
        Responsible for implementing all file access.  `vimcryption.vim` redirects all file and buffer
        operations to an instance of this class.
    """
    def __init__(self):
        """ Configurations:
            g:vimcryption_cipher   Default cipher type to use
        """
        self.cipher_factory = CipherFactory()
        self.cipher_type = vim.eval("get(g:, 'vimcryption_cipher', \"IOPASS\")")
        self.cipher_engine = None

    def set_cipher(self, cipher_type):
        """ Sets the current cipher type and constructs an `EncryptionEngine` of that type.
        """
        self.cipher_type = cipher_type
        self.cipher_engine = self.cipher_factory.get_engine_for_cipher(self.cipher_type, prompt=vc_prompt)

    def vimcryption_read(self):
        """ General `read` function for dealing with reads in Vim using
            the encryption engine to append the decrypted lines
        """
        file_name = vim.eval('expand("<amatch>")')
        modifiable = (vim.eval("&modifiable") != '0')

        # Don't do anything if the file doesnt exist
        # Write functions will create file
        if not os.path.exists(file_name):
            return

        # Unlock read only buffers so we can update them
        if not modifiable:
            vim.command(":set ma")

        with open(file_name, 'rb') as current_file:
            try:
                self.cipher_engine = self.cipher_factory.get_engine_for_file(current_file, prompt=vc_prompt)
                self.cipher_type = self.cipher_engine.cipher_type
            except NotVimcryptedException:
                self.cipher_engine = PassThrough()
                current_file.seek(0)

            retries = 0
            while True:
                try:
                    self.cipher_engine.decrypt_file(current_file, vim.current.buffer)
                    break

                except IncorrectPasswordException:
                    retries += 1
                    if retries >= 3:
                        print("Incorrect Password, Max Tries Reached, Showing Encrypted Content")
                        current_file.seek(0)
                        self.cipher_engine = PassThrough()
                        self.cipher_engine.decrypt_file(current_file, vim.current.buffer)
                        modifiable = False
                        break
                    else:
                        print("Incorrect Password")
                        self.cipher_engine.cipher_key = self.cipher_engine.get_cipher_key()


        # Vim adds an extra line at the top of the NEW buffer
        del vim.current.buffer[0]

        # Relock read-only buffers  before user gets it
        if not modifiable:
            vim.command(":set noma")

        # Redraw after we've loaded to clear out old stuff
        vim.command(":redraw!")

    def vimcryption_write(self, vim_buffer, mode):
        """ General `write` function for dealing with writes in Vim using
            the encryption engine to write encrypted lines.
        """
        file_name = vim.eval('expand("<amatch>")')
        new_file = (file_name != vim.current.buffer.name) or (not os.path.exists(file_name))

        # If we don't already know what cipher to use ask the Factory
        if (new_file and (self.cipher_engine is None)):
            try:
                self.cipher_engine = self.cipher_factory.get_engine_for_cipher(self.cipher_type, prompt=vc_prompt)
            except UnsupportedCipherException:
                self.cipher_engine = PassThrough()

        with open(file_name, mode) as current_file:
            self.cipher_engine.encrypt_file(vim.current.buffer, current_file)

        # Writers must always reset the modified bit
        vim.command(':set nomodified')

        # On writes Vim echoes what it did so the user can tell
        new_file_str = "[New]" if new_file else ""
        print("\"{}\" {} {}L written".format(os.path.basename(file_name), new_file_str, len(vim.current.buffer)))

    # Callbacks from Vim Cmd-Events
    def buf_read(self):
        """
        BufReadCmd: Before starting to edit a new buffer.
        Should read the file into the buffer.
        """
        vim.command('exe "silent doau BufReadPre ".fnameescape(expand("<amatch>"))')
        self.vimcryption_read()
        vim.command('exe "silent doau BufReadPost ".fnameescape(expand("<amatch>"))')

    def file_read(self):
        """
        FileReadCmd: Before reading a file with a ":read" command.
        Should do the reading of the file.
        """
        vim.command('exe "silent doau FileReadPre ".fnameescape(expand("<amatch>"))')
        self.vimcryption_read()
        vim.command('exe "silent doau FileReadPost ".fnameescape(expand("<amatch>"))')

    def buf_write(self):
        """
        BufWriteCmd: Before writing the whole buffer to a file.
        Should do the writing of the file and reset 'modified' if successful, unless '+' is in
        'cpo' and writing to another file |cpo-+|. The buffer contents should not be changed.
        """
        vim.command('exe "silent doau BufWritePre ".fnameescape(expand("<amatch>"))')
        self.vimcryption_write(vim.current.buffer, 'wb+')
        vim.command('exe "silent doau BufWritePost ".fnameescape(expand("<amatch>"))')

    def file_write(self):
        """
        FileWriteCmd: Before writing to a file, when not writing the
        whole buffer.  Should do the writing to the file.  Should not change the buffer.  Use the
        '[ and '] marks for the range of lines.
        """
        buf_start_line, buf_start_col = vim.buffer.mark("'[")
        buf_end_line, buf_end_col = vim.buffer.mark("']")
        current_range = vim.buffer.range(buf_start_line, buf_end_line)

        vim.command('exe "silent doau FileWritePre ".fnameescape(expand("<amatch>"))')
        self.vimcryption_write(current_range, 'wb+')
        vim.command('exe "silent doau FileWritePost ".fnameescape(expand("<amatch>"))')

    def file_append(self):
        """
        FileAppendCmd: Before appending to a file.  Should do the
        appending to the file.  Use the '[ and '] marks for the range of lines.
        """

        buf_start_line, buf_start_col = vim.buffer.mark("'[")
        buf_end_line, buf_end_col = vim.buffer.mark("']")
        current_range = vim.buffer.range(buf_start_line, buf_end_line)

        self.vimcryption_write(current_range, 'ab+')
