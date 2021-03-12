"""
Prog:   input_files.py
Auth:   Oleksii Krutko, IO-z91
Desc:   Optimization and experiments planning. 2021
"""


class InputError(Exception):
    """
    Common exception for input_files class
    """
    pass


class Input(object):
    """
    Base input class
    """
    def __init__(self):
        pass

    def read_var(self, var_name, var_type, var_min, var_max):
        """
        Reads variable from a source
        :param var_name: variable name
        :param var_type: expected variable type
        :param var_min: min value
        :param var_max: max value
        :return: value
        """
        pass


class KeyboardInput(Input):
    """
    input_files from keyboard
    """
    def __init__(self):
        super(KeyboardInput, self).__init__()

    def read_var(self, var_name, var_type, var_min, var_max):
        while True:
            try:
                var_new = var_type(input("Enter {}:".format(var_name)))
                if not var_min <= var_new <= var_max:
                    print("Value '{}' must be in range [{}:{}]".format(var_name, var_min, var_max))
                    continue
            except ValueError:
                print("Type '{}' expected.".format(var_type))
            else:
                break

        return var_new


class FileInput(Input):
    """
    input_files from file
    """
    def __init__(self, file_path):
        """
        Constructor
        :param file_path: file to read data from
        """
        super(FileInput, self).__init__()
        self._file_path = file_path
        self._var_list = dict()
        self._read_all_data()

    def _read_all_data(self):
        """
        Reads all variables from file
        :return:
        """
        try:
            with open(self._file_path) as reader:
                line = reader.readline()

                while line != '':
                    try:
                        var_name_file, var_value_file = line.rstrip('\n').split(' ')

                        self._var_list[var_name_file] = var_value_file
                    except ValueError:
                        print("Error in line '{}'".format(line))

                    line = reader.readline()
        except IOError:
            print("File '{}' not found or could not be read".format(self._file_path))

    def read_var(self, var_name, var_type, var_min, var_max):
        if not self._var_list.__contains__(var_name):
            raise InputError("Variable '{}' is missing in file '{}'".format(var_name, self._file_path))

        try:
            var_new = var_type(self._var_list[var_name])
            if not var_min <= var_new <= var_max:
                raise InputError("Value '{}' must be in range [{}:{}]".format(var_name, var_min, var_max))

            return var_new
        except ValueError:
            raise InputError("Variable '{}' type '{}' expected.".format(var_name, var_type))


def get_input_source(task_name):
    """
    input_files type selection
    :param task_name: prefix to look corresponding input file
    :return: input_files interface
    """
    keyboard_input = KeyboardInput()

    print("Select source type (1 - keyboard, 2 - {}_input.txt)".format(task_name))
    source_type = keyboard_input.read_var("source type", int, 1, 2)

    if source_type == 1:
        return KeyboardInput()
    elif source_type == 2:
        return FileInput("input_files/{}_input.txt".format(task_name))


def get_option(text, count):
    """
    Option selection
    :param text: test to show
    :param count: max number of options
    :return: selected option
    """
    keyboard_input = KeyboardInput()

    print(text)
    return keyboard_input.read_var("", int, 1, count)
