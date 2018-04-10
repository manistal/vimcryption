"""
"""

import vim
import os
import binascii
from base64 import b64decode, b64encode
from iobase import IOPassThrough


class VCFileHandler():
    _CIPHERS = {
        'IOPASS' : IOPassThrough, 
        'BASE64' : IOPassThrough, 
        'AES128' : IOPassThrough, 
        'AES256' : IOPassThrough
    }

    def __init__(self, config=None):
        self.cipher_type = vim.eval("get(g:, 'vimcryption_cipher_type', \"IOPASS\")")
        self.cipher_gen = self._CIPHERS.get(self.cipher_type, IOPassThrough) 

        if self.cipher_type not in self._CIPHERS:
            self.cipher_type = "IOPASS"


    def DisableVC(self, file_handle):
        file_handle.seek(0) 
        vim.command("call UnloadVimcryption()")
        self.cipher_gen = IOPassThrough

    def ProcessHeader(self, file_handle):
        """ Process vimcryption header
            @param file_handle expects file-like bytes object
            0:15 (16)  bytes - b64encode of "vimcryption" if the file is our type
            16:23 (8)  bytes - b64encode of cipher, always 6 chars (AES128, AES256, BASE64, IOPASS)
            24:88 (64) bytes - sha256 hash of key/password for file (optional)
        """
        try:
            # First check to see if we should be handling it 
            header_valid = b64decode(file_handle.read(16))
            if (header_valid != 'vimcrypted'):
                return self.DisableVC(file_handle)

            # Setup the cipher IO for encrypt/decrypt 
            header_cipher = b64decode(file_handle.read(8))
            self.cipher_gen = self._CIPHERS[header_cipher]
            self.cipher_type = header_cipher

        # Python2 Padding Error
        except TypeError as err:
            self.DisableVC(file_handle)

        # Python3 Padding Error 
        except binascii.Error as err:
            self.DisableVC(file_handle)

        # Unsupported Cipher
        except KeyError as err:
            print("Unsupported Cipher: " + header_cipher)
            self.DisableVC(file_handle)


    def WriteHeader(self, file_handle):
        file_handle.seek(0) # Always start at the begginning
        file_handle.write(b64encode('vimcrypted'))
        file_handle.write(b64encode(self.cipher_type))

    def BufRead(self):
        """
        BufReadCmd: Before starting to edit a new buffer.  
        Should read the file into the buffer. 
        """
        file_name = vim.current.buffer.name

        # Don't do anything if the file doesnt exist
        # Write functions will create file
        if not os.path.exists(file_name): return

        with open(file_name, 'rb+') as current_file:
            self.ProcessHeader(current_file)

            for line in self.cipher_gen().decrypt(current_file):
                vim.current.buffer.append(line)

        # Vim adds an extra line at the top of the buffer 
        # We need to remove it or files keep getting longer
        del vim.current.buffer[0]

    def FileRead(self):
        """
        FileReadCmd: Before reading a file with a ":read" command.
        Should do the reading of the file.
        """
        file_name = vim.current.buffer.name

        # Don't do anything if the file doesnt exist
        # Write functions will create file
        if not os.path.exists(file_name): return

        with open(file_name, 'rb+') as current_file:
            self.ProcessHeader(current_file)

            for line in self.cipher_gen().decrypt(current_file):
                vim.current.buffer.append(line)

        # Vim adds an extra line at the top of the buffer 
        # We need to remove it or files keep getting longer
        del vim.current.buffer[0]

    def BufWrite(self):
        """
        BufWriteCmd: Before writing the whole buffer to a file.
        Should do the writing of the file and reset 'modified' if successful, unless '+' is in
        'cpo' and writing to another file |cpo-+|. The buffer contents should not be changed.
        """
        file_name = vim.current.buffer.name

        with open(file_name, 'wb+') as current_file:
            self.WriteHeader(current_file)

            for line in self.cipher_gen().encrypt(vim.current.buffer):
                current_file.write(line + "\n")

        vim.command(':set nomodified')

    def FileWrite(self):
        """
        FileWriteCmd: Before writing to a file, when not writing the
        whole buffer.  Should do the writing to the file.  Should not change the buffer.  Use the
        '[ and '] marks for the range of lines.
        """
        file_name = vim.current.buffer.name
        buf_start_line, buf_start_col = vim.buffer.mark("'[")
        buf_end_line, buf_end_col = vim.buffer.mark("']") 
        current_range = vim.buffer.range(buf_start_line, buf_end_line)

        with open(file_name, 'wb+') as current_file:
            self.WriteHeader(current_file)

            for line in self.cipher_gen().encrypt(current_range):
                current_file.write(line + "\n")

        vim.command(':set nomodified')

    def FileAppend(self):
        """
        FileAppendCmd: Before appending to a file.  Should do the
        appending to the file.  Use the '[ and '] marks for the range of lines.
        """
        file_name = vim.current.buffer.name
        buf_start_line, buf_start_col = vim.buffer.mark("'[")
        buf_end_line, buf_end_col = vim.buffer.mark("']") 
        current_range = vim.buffer.range(buf_start_line, buf_end_line)

        with open(file_name, 'ab') as current_file:
            self.WriteHeader(current_file)

            for line in self.cipher_gen().encrypt(current_range):
                current_file.write(line + "\n")

        vim.command(':set nomodified')


