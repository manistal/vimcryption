"""
"""

import vim
import os
import binascii
from base64 import b64decode, b64encode
from iobase import IOPassThrough

"""
TODO:
When using an external program, be certain to turn off options like 
    persistent undo (:help 'undofile'), 
    backup files (:help 'backup'), 
    swap files (:help 'swapfile'), and 
    .viminfo file (:help 'viminfo'),i
"""

class VCFileHandler():
    _CIPHER_GEN_MAP_ = {
        'IOPASS' : IOPassThrough, 
        'BASE64' : IOPassThrough, 
        'AES128' : IOPassThrough, 
        'AES256' : IOPassThrough
    }

    def __init__(self, config=None):
        self.io_generator = IOPassThrough

        if config:
            self.config = config

    def DisableVC(self):
        file_handle.seek(0) # its not ours, reset
        self.io_generator = IOPassThrough
        # TODO: might want to run a vim command to unregister us if its not our file
        #       can then have a different command hook to reregister for enables
        # vim.command("unloadVimcryption")

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


            # Which cipher
            header_cipher = b64decode(file_handle.read(8))
            self.io_generator = self._CIPHER_GEN_MAP_[header_cipher]


        except TypeError as err:
            self.DisableVC()

        except binascii.Error as err:
            self.DisableVC()

        except KeyError as err:
            self.DisableVC()
            file_handle.seek(0) # not ours, python3 support
            file_handle.seek(0) # nonexistant cipher requested

    def WriteHeader(self, file_handle):
        file_handle.write(b64encode('vimcrypted'))
        file_handle.write(b64encode('IOPASS'))

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

            for line in self.io_generator().decrypt(current_file):
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

            for line in self.io_generator().decrypt(current_file):
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

            for line in self.io_generator().encrypt(vim.current.buffer):
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

            for line in self.io_generator().encrypt(current_range):
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

            for line in self.io_generator().encrypt(current_range):
                current_file.write(line + "\n")

        vim.command(':set nomodified')


