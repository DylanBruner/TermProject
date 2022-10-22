import os, sys, msvcrt            

class Input(object):
    def __init__(self):
        self.entries = []
        self.added_suggestions = []

    def get_tab_complete(self, input: str) -> str or None:
        filesOld = [file for file in os.listdir(os.getcwd())]
        filesOld.extend(self.added_suggestions)
         
        files = [file for file in filesOld if file.startswith(input)]
        if len(files) > 0:
            return files[0]
        return None

    def reprint_with_cursor(self, input: str, cursor_pos: int):
        sys.stdout.write('\r' + ' ' * (len(input) + 2) + '\r')
        sys.stdout.flush()
        sys.stdout.write('\r')
        sys.stdout.write(input)
        sys.stdout.write(' ' * (len(input) - cursor_pos))
        sys.stdout.write('\r')
        sys.stdout.write(input[:cursor_pos])
        sys.stdout.flush()
    
    def get_input(self, prompt: str) -> str:
        notDone = True

        sys.stdout.write(prompt)
        sys.stdout.flush()

        historyIndex = 0

        input_data = ""
        cursor_pos = len(prompt)

        while notDone:
            char = msvcrt.getch()
            if char == b'\r':
                notDone = False
            elif char == b'\b':
                if cursor_pos > len(prompt):
                    input_data = input_data[:cursor_pos-(len(prompt)+1)] + input_data[cursor_pos-len(prompt):]
                    cursor_pos -= 1
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            elif char == b'\t':
                #Add file tab complete just like bash self.get_tab_complete(input_data) returns the closest file
                file = self.get_tab_complete(input_data.split(' ')[-1])
                if file is not None:
                    #Remove the last ' ' seperated word from input_data
                    input_data = (' '.join(input_data.split(' ')[:-1]) + ' ' + file)
                    cursor_pos = len(input_data) + len(prompt)
                    sys.stdout.write(file)
                    sys.stdout.flush()
                    self.reprint_with_cursor(input_data, cursor_pos)
            elif char == b'\xe0':
                #Only need left and right arrow keys for cursor movement
                #Take in to account the prompt length
                char = msvcrt.getch()
                if char == b'K':
                    if cursor_pos > len(prompt):
                        cursor_pos -= 1
                        sys.stdout.write('\b')
                        sys.stdout.flush()
                elif char == b'M':
                    if cursor_pos < len(input_data):
                        cursor_pos += 1
                        sys.stdout.write(input_data[cursor_pos-1])
                        sys.stdout.flush()

                #Up and down arrow keys for history
                elif char == b'H':
                    if historyIndex < len(self.entries):
                        historyIndex += 1
                        input_data = self.entries[-historyIndex]
                        cursor_pos = len(input_data) + len(prompt)
                        self.reprint_with_cursor(input_data, cursor_pos)
                elif char == b'P':
                    if historyIndex > 0:
                        historyIndex -= 1
                        input_data = self.entries[-historyIndex]
                        cursor_pos = len(input_data) + len(prompt)
                        self.reprint_with_cursor(input_data, cursor_pos)
            else:
                input_data = input_data[:cursor_pos] + char.decode('utf-8') + input_data[cursor_pos:]
                cursor_pos += 1
                sys.stdout.write(char.decode('utf-8'))
                sys.stdout.flush()

            self.reprint_with_cursor(f"{prompt}{input_data}", cursor_pos)
        
        sys.stdout.write('\n'); sys.stdout.flush()

        self.entries.append(input_data)
        return input_data