
import vim


class VCFileHandler():
    def __init__(self, config=None):
        if config:
            self.config = config

    def BufRead(self):
        file_name = vim.current.buffer.name
        with open(file_name, 'r+') as current_file:
            vim.current.buffer.append(current_file.readlines())

    def FileRead(self):
        file_name = vim.current.buffer.name
        with open(file_name, 'r+') as current_file:
            vim.current.buffer.append(current_file.readlines())

    def BufWrite(self):
        file_name = vim.current.buffer.name
        with open(file_name, 'w+') as current_file:
            current_file.writelines("\n".join(vim.current.buffer))

        vim.command(':set nomodified')

    def FileWrite(self):
        file_name = vim.current.buffer.name
        with open(file_name, 'w+') as current_file:
            current_file.writelines("\n".join(vim.current.buffer))

        vim.command(':set nomodified')

    def FileAppend(self):
        pass