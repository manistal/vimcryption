
import vim
import os
import binascii
from base64 import b64decode, b64encode

def GhettoGenerator(text_sequence):
    """ To be replaced by our actual encryptor/decryptors
        recieves iteratble text sequence, expects lines returned
        no line break characters returned, only lines, line breaks inserted by VCF
    """
    for line in text_sequence:
        yield line

Decryptor = GhettoGenerator
Encryptor = GhettoGenerator
Plaintext = GhettoGenerator

class VCFileHandler():
    def __init__(self, config=None):
        if config:
            self.config = config

    def ProcessHeader(self, file_handle):
        # First check to see if we should be handling it 
        self.generator = Plaintext
        header_entry = file_handle.read(16)

        try:
            if (header_entry and (b64decode(header_entry) == 'vimcrypted')):
                self.generator = Decryptor

        except TypeError as e:
            file_handle.seek(0) # its not ours, reset

        except binascii.Error as e:
            file_handle.seek(0) # not ours, python3 support

    def WriteHeader(self, file_handle):
        file_handle.write(b64encode('vimcrypted'))

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
            for line in self.generator(current_file):
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
            for line in self.generator(current_file):
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
            for line in GhettoGenerator(vim.current.buffer):
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
            for line in GhettoGenerator(current_range):
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
            for line in GhettoGenerator(current_range):
                current_file.write(line + "\n")

        vim.command(':set nomodified')


