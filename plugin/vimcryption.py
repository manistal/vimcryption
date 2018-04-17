"""
"""

import vim
import os
import binascii
from base64 import b64decode, b64encode

from encryptionengine import PassThrough, Base64Engine

class UnsupportedCipherException(Exception):
    pass


def VCPrompt(message):
    vim.command('call inputsave()')
    vim.command("let user_input = input('" + message + " ')")
    vim.command('call inputrestore()')
    return vim.eval('user_input')


def MakeCipher(cipher_type):
    CIPHERS = {
        'IOPASS' : PassThrough, 
        'BASE64' : Base64Engine, 
        'AES128' : PassThrough, 
        'AES256' : PassThrough
    }
    if cipher_type not in CIPHERS:
        raise UnsupportedCipherException("Tried to construct unsupported cipher: " + cipher_type)
    return CIPHERS[cipher_type](prompt=VCPrompt)


class VCFileHandler():
    def __init__(self):
        """
        Configurations:
        g:vimcryption_cipher   Entry in self._CIPHERS for Engine setting
        """
        self.cipher_type = vim.eval("get(g:, 'vimcryption_cipher', \"IOPASS\")")
        self.cipher_engine = MakeCipher(self.cipher_type)

    def DisableVC(self, file_handle):
        """ Disable Vimcryption Engine and Reset File Pointer """
        file_handle.seek(0) 
        vim.command("call UnloadVimcryption()")
        self.cipher_engine = MakeCipher("IOPASS")

    # Header Functions
    def ProcessHeader(self, file_handle):
        """ Process vimcryption header
            @param file_handle expects file-like bytes object
            0:15 (16)  bytes - b64encode of "vimcryption" if the file is our type
            16:23 (8)  bytes - b64encode of cipher, always 6 chars (AES128, AES256, BASE64, IOPASS)
            24:X  (X)  bytes - [optional]  - Engine may process additional metadata 
        """
        try:
            # First check to see if we should be handling it 
            header_valid = b64decode(file_handle.read(16))
            if (header_valid != b'vimcrypted'):
                return self.DisableVC(file_handle)

            # Setup the cipher IO for encrypt/decrypt 
            self.cipher_type = b64decode(file_handle.read(8)).decode('utf-8')
            self.cipher_engine = MakeCipher(self.cipher_type)

        # Python2 Padding Error
        except TypeError as err:
            self.DisableVC(file_handle)

        # Python3 Padding Error 
        except binascii.Error as err:
            self.DisableVC(file_handle)

        # Unsupported Cipher
        except UnsupportedCipherException as err:
            print("Unsupported Cipher: " + self.cipher_type)
            self.DisableVC(file_handle)

    def WriteHeader(self, file_handle):
        file_handle.seek(0) # Always start at the begginning
        file_handle.write(b64encode('vimcrypted'))
        file_handle.write(b64encode(self.cipher_type))

    # Reader Functions 
    def VimCryptionRead(self):
        """
        General `read` function for dealing with reads in Vim using 
        the encryption engine to append the decrypted lines
        """
        file_name = vim.eval('expand("<amatch>")') 
        modifiable = (vim.eval("&modifiable") != '0') 

        # Don't do anything if the file doesnt exist
        # Write functions will create file
        if not os.path.exists(file_name): return

        # Unlock read only buffers so we can update them
        if not modifiable: vim.command(":set ma")

        with open(file_name, 'rb') as current_file:
            self.ProcessHeader(current_file)
            self.cipher_engine.decrypt(current_file, vim.current.buffer)

        # Vim adds an extra line at the top of the NEW buffer 
        del vim.current.buffer[0]

        # Relock read-only buffers  before user gets it
        if not modifiable: vim.command(":set noma")

    def BufRead(self):
        """
        BufReadCmd: Before starting to edit a new buffer.  
        Should read the file into the buffer. 
        """
        self.VimCryptionRead()        

    def FileRead(self):
        """
        FileReadCmd: Before reading a file with a ":read" command.
        Should do the reading of the file.
        """
        self.VimCryptionRead()        

    # Writer Functions 
    def VimCryptionWrite(self, buffer):
        file_name = vim.eval('expand("<amatch>")') 
        new_file = not os.path.exists(file_name)

        with open(file_name, 'wb+') as current_file:
            self.WriteHeader(current_file)
            self.cipher_engine.encrypt(vim.current.buffer, current_file)

        # Writers must always reset the modified bit
        vim.command(':set nomodified')

        # On writes Vim echoes what it did so the user can tell 
        new_file_str = "[New]" if new_file else "" 
        print("\"{}\" {} {}L written".format(
              os.path.basename(file_name), new_file_str, len(vim.current.buffer)))

    def BufWrite(self):
        """
        BufWriteCmd: Before writing the whole buffer to a file.
        Should do the writing of the file and reset 'modified' if successful, unless '+' is in
        'cpo' and writing to another file |cpo-+|. The buffer contents should not be changed.
        """
        self.VimCryptionWrite(vim.current.buffer)

    def FileWrite(self):
        """
        FileWriteCmd: Before writing to a file, when not writing the
        whole buffer.  Should do the writing to the file.  Should not change the buffer.  Use the
        '[ and '] marks for the range of lines.
        """
        buf_start_line, buf_start_col = vim.buffer.mark("'[")
        buf_end_line, buf_end_col = vim.buffer.mark("']") 
        current_range = vim.buffer.range(buf_start_line, buf_end_line)

        self.VimCryptionWrite(current_range)

    # Append Function
    def FileAppend(self):
        """
        FileAppendCmd: Before appending to a file.  Should do the
        appending to the file.  Use the '[ and '] marks for the range of lines.
        """
        file_name = vim.eval('expand("<amatch>")') 

        buf_start_line, buf_start_col = vim.buffer.mark("'[")
        buf_end_line, buf_end_col = vim.buffer.mark("']") 
        current_range = vim.buffer.range(buf_start_line, buf_end_line)

        with open(file_name, 'ab') as current_file:
            self.WriteHeader(current_file)
            self.cipher_engine.encrypt(current_range, current_file)

        vim.command(':set nomodified')


