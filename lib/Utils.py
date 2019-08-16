if __name__ == "__main__":
    # MAJOR +1 represents an added function.
    __MAJOR = 1 + 1
    # MINOR +1 represents a change in existing function(s) within the current MAJOR.
    __MINOR = 0
    
    __info = """This file contains general-purpose functions for my labs and assignments. Included with every complex program.
To use functions contained herein in another project, include this file inside the project's directory."""
    
    print("========================================================")
    print("Utils.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")



#========================Imports========================

# Used by: CsvToMatrix(); WriteCsv()
import csv
# Used by: ModuleAvailability()
import imp
# Used by: CsvToMatrix(); WriteCsv()
import os
# Used by: (deprecated) CsvToMatrix(); (deprecated) WriteCsv()
import platform
# Used by WriteShell()
import sys



#========================Common functions========================

#Asks the user to enter a number. Validate if it is not an integer.
def enterInteger(CustomMessage="Please enter an integer: ",
                 CustomErrorMessage="The input is not an integer, please try again...",
                 min=None, max=None):
    """
    Repeatedly tries to convert user input to an integer until succeded.
    
    Args:
        CustomMessage: Define a custom user input prompt.
            Default: "Please enter an integer: "
        CustomErrorMessage: Define a custom message if the user has not typed an integer.
            Default: "The input is not an integer, please try again..."
        min: the inclusive minimum value the integer is permitted (None for no minimum value)
            Default: None
        max: the inclusive maximum value the integer is permitted (None for no minimum value)
            Default: None
    
    Returns:
        The inputted integer.
    """
    
    isInteger = False
    while not isInteger:
        try:
            number = int(input(CustomMessage))
            isInteger = True
        except ValueError:
            print(CustomErrorMessage)

    # range parameter
    if type(min) is int and type(max) is int:
        if min > max:
            raise ValueError("parameter 'min' is larger than 'max'")
        else:
            while min > number or number > max:
                number = enterInteger(CustomMessage="Please input a number within "+str(min)+" to "+str(max)+": ")
    elif type(min) is int:
        while min > number:
            number = enterInteger(CustomMessage="Please input a number larger than " + str(min) + ": ")
    elif type(max) is int:
        while number > max:
            number = enterInteger(CustomMessage="Please input a number smaller than " + str(max) + ": ")

    return number


def enterList(CustomMessage="Please enter a list: ", CustomErrorMessage="The input is not a valid list, please try again...", ExplicitType=type):
    """
    Repeatedly tries to convert user input to a list until succeded.
    
    Args:
        CustomMessage: Define a custom user input prompt. Default is: "Please enter a list: "
        CustomErrorMessage: Define a custom message if the user has not typed a valid list. Default is: "The input is not a valid list, please try again..."
        ExplicitType: Specify a data type which all items inside the list should be. Non-built-in types are not guaranteed to work. Default is: type
    
    Returns:
        The user-inputted list.
    """
    
    isList = False
    while isList == False:
        try:
            ls = []
            # we map 'ls' into 'ldict' to be used for exec()
            ldict = locals()

            print(CustomMessage)
            if ExplicitType != type:
                print("    Please note that every element inside the list needs to be of type '", TypeclassToString(ExplicitType), "'", sep="")

            # Using exec(), we can convert the user's string input to a list.
            # Note the use of ldict as an argument
            # Remark: This method is potentially dangerous, as any code can be executed with the proper syntax. Consider limiting the length of the input.
            exec("ls = list("+input()+")", globals(), ldict)
            # Value assignments inside exec() will map onto ldict, which we need to transfer back to the original variables (ls)
            ls = ldict["ls"]

            isList = True
            
            if ExplicitType == type:
                break

            # Convert to specified ExplicitType. A conversion error means that the user input is invalid.
            for i in range(0, len(ls)):
                ldict = locals()

                # Type constructors' names for built-in types are the same as the type's name.
                # e.g. constructor for type int is int())
                exec("ls[i] = " + TypeclassToString(ExplicitType) + "(ls[i])", globals(), ldict)
            # We transfer 'ls's value from ldict back to the original list.
            ls = ldict["ls"]
        except Exception:
            # If isList == True, but an exception is neverthless thrown, this means that an item inside the list does not have the correct type.
            # This is why we need to reset isList to false every time an exception is thrown.
            isList = False
            print(CustomErrorMessage)
    return ls


def isiter(obj):
    """
    Checks if an object is an iterable.
    Strings also do return True.
    
    Args:
        object: An object of any type.
    
    Returns:
        A boolean indicating whether 'object' is an iterable.
    
    Raises:
        Any exception not pertaining to TypeError is passed onto the stack.
    """
    
    try:
        iter(obj)
        return True
    except TypeError:
        pass
    return False


def LongestFromList(ls: list):
    """
    Determines the object with the longest length inside a list.

    Args:
        ls: A list containing an array of objects.

    Returns:
        The object with the longest length from the list.
        None if not applicable.
    """
    try:
        current = ls[0]
        for obj in ls:
            if len(obj) > len(current):
                current = obj
        return current
    except:
        # There could be many reasons for which above code fails:
        # ls of length 0, obj of a type without support for len(), or ls is not an iterable.
        return None


def ModuleAvailability(module_name):
    """
    Checks if a module is installed/available on the current system.

    Args:
        module_name: [str] name of the module to check for availability.

    Returns:
        A boolean indicating whether the module is available.
    """

    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False

    
def TypeclassToString(_type):
    """
    Returns a string representation of a Python data type.
    
    Args:
        _type: Any data type or an instance of that type.
    
    Returns:
        The type of the parameter, in string, without the <class '*'> (asterisk is the data type) formatting.
    """

    typestring = str(type(_type))

    if typestring == "<class 'type'>":
        # This means that _type is a Python data type, and not an instance of that type.
        typestring = str(_type)

    # Formatting typestring to remove "<class '" and "'>" parts
    typestring = typestring.replace("<class '", "")
    typestring = typestring.replace("'>", "")

    return typestring


def WriteShell(*text, sep=' ', end='\n', Color='default', stderr=False, flush=False):
    """
    An alternative to Python's built-in print() function, without the 'file' parameter.
    Writes objects' string representation to the shell's stdout.
    Note: If not running inside IDLE, shells must have extended ANSI support to display color.
    
    Args:
        *text: A set of objects to be outputted to the shell's stdout.
        sep: The separator string to use for in-between objects from '*text'
        end: A string to print at the end of the output.
            Default: '\n' as newline character
        Color: The foreground color of the printed text.
            Available colors are:
                'default' - the default color of the shell.
                'black'
                'red' - dark red
                'orange'
                'green'
                'blue' - used for IDLE's stdout
                'purple'
                'brown' - cyan outside IDLE
                'error' - used for printing stderr, a bright red
            Note:
                Colors may vary depending on the shell used and/or IDLE's color configuration.
        stderr: Whether to optput into stderr instead of stdout.
            Note:
                Printing to stderr will not automatically change the text color. Best to use Color='error'
                Consider flushing stderr (param flush=True) to allow error messages to be outputted before any other code is executed.
        flush: Whether to flush the output (True) or let it remain buffered (False).
    """

    try:
        # 'IDLEshell' assignement will throw an error when the line is run outside IDLE.
        if stderr:
            IDLEshell = sys.stderr.shell
        else:
            IDLEshell = sys.stdout.shell

        # Dictionary to translate 'Color' parameter to IDLE's coloring options.
        colormap = {'default': 'stdout',
                    'black': 'SYNC',
                    'red': 'COMMENT',
                    'orange': 'KEYWORD',
                    'green': 'STRING',
                    'blue': 'DEFINITION',
                    'purple': 'BUILTIN',
                    'brown': 'console',
                    'error': 'stderr'}
        
        # If 'Color' parameter does not pass a valid value, use default 'stdout'
        try:
            coloring = colormap[Color]
        except:
            coloring = 'stdout'
        
        # The string to be written to IDLEshell:
        out = ""

        for i in range(0, len(text)-1):
            out += str(text[i])
            out += str(sep)
        if len(text) != 0:
            # We don't want to write yet another separator character to the end of the line.
            # Thus, we append the last item out of the for loop.
            out += str(text[-1])
        
        out += end

        # Write to IDLEshell.
        # 'outlen' is used to store the length of the string written, in integer. 
        # Without this assignment, the length will get outputted to stdout at the end of the line.
        outlen = IDLEshell.write(out, coloring)

        if flush:
            # Flushes the output.
            IDLEshell.flush()
        
    # => Not in IDLE's shell.
    # We will employ a general shell coloring method.
    # This only works in general shells with extended ANSI support.
    except AttributeError:
        # Dictionary to translate 'Color' parameter to ANSI escape characters.
        # if color mapping is 'default', no ANSI formatting will be used. Safe for shells without extended ANSI support.
        # Since ANSI excape character set does not include brown, it is substituted for cyan. Also, error red replaced with red.
        colormap = {'default': 'default',
                    'black': '\033[30m',
                    'red': '\033[31m',
                    'orange': '\033[33m',
                    'green': '\033[32m',
                    'blue': '\033[34m',
                    'purple': '\033[35m',
                    'brown': '\033[36m',
                    'error': '\033[31m'}
        
        # If 'Color' parameter does not pass a valid value, use default 'default'
        try:
            coloring = colormap[Color]
        except:
            coloring = 'default'

        # The string to be written to output:
        out = ""

        for i in range(0, len(text)-1):
            out += str(text[i])
            out += str(sep)
        if len(text) != 0:
            # We don't want to write yet another separator character to the end of the line.
            # Thus, we append the last item out of the for loop.
            out += str(text[-1])

        out += end

        if stderr:
            if coloring == "default":
                outlen = sys.stderr.write(out)
            else:
                outlen = sys.stderr.write(coloring + out + '\033[0m')

            if flush:
                sys.stderr.flush()
        else:
            if coloring == "default":
                outlen = sys.stdout.write(out)
            else:
                outlen = sys.stdout.write(coloring + out + '\033[0m')

            if flush:
                sys.stdout.flush()



#========================CSV========================

def __parseCsvRow(row):
    """
    THIS IS AN INTERNAL FUNCTION!
    Convert every integer and float string literals into their respective types
    
    Args:
        row: Provide a string literal of a matrix's row
    
    Returns:
        The matrix row with string literals of float and integers converted to their respective types.
    """
    
    resultRow = []
    for item in row:
        if type(item) is str:
            if "." in item:
                try:
                    f = float(item)
                    resultRow.append(f)
                except ValueError:
                    resultRow.append(item)
            else:
                try:
                    i = int(item)
                    resultRow.append(i)
                except ValueError:
                    resultRow.append(item)
        else:
            resultRow.append(item)
    return resultRow


def CsvToMatrix(csvFileName, csvDelimiter=','):
    """
    Converts from a CSV formatted file into a two-dimensional list.
    
    Args:
        csvFileName: The absolute path to a CSV-formatted file
            Hint: Use (os.getcwd() + "\\FILENAME.csv") to acquire the current directory file.
    
    Returns:
        A matrix extracted from the specified CSV file.
    """
    if os.path.isfile(csvFileName):
        dataMatrix = []         # dimensions a list to store CSV data lists

        filePermission = "r"    # Platform-specific file reading privileges
        #if platform.system() == "Windows":
        #    filePermission = "rb"
        
        with open(csvFileName, filePermission) as csvfile:
            reader = csv.reader(csvfile, delimiter=csvDelimiter, quotechar='|')
            for row in reader:
                if row != []:
                    dataMatrix.append(__parseCsvRow(row))
            csvfile.close()
        return dataMatrix
    else:
        return []           # returns am empty list


def WriteToCsv(matrix, csvFileName, csvDelimiter=','):
    """
    Converts a two-dimensional list to a CSV file and writes it to a specified file.
    If the provided file path refers to an existing file, it will be overwritten.
    
    Args:
        matrix: A two-dimensional matrix (list of lists or tuple of tuples)
        csvFileName: The absolute path to save the CSV file
            Hint: Use (os.getcwd() + "\\FILENAME.csv") to specify the current directory.
    
    Returns:
        A matrix extracted from the specified CSV file.
    """
    
    if os.path.isfile(csvFileName) == True:
        os.remove(csvFileName)  # Deletes the CSV file

    filePermission = "w"    # Platform-specific file reading privileges
    #if platform.system() == "Windows":
    #    filePermission = "wb"
    
    with open(csvFileName, filePermission) as csvfile:
        writer = csv.writer(csvfile, delimiter=csvDelimiter, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in matrix:
            if row != []:
                writer.writerow(row)
        csvfile.close()



#========================Version History========================

# 1.0
"""
    Initial Release
    Imported functions from Assignment 2 that are general-purpose

    Additions
    ---------
        Functions adapted from Assignment 2:
        -enterInteger(CustomMessage = "Please enter an integer: ", CustomErrorMessage = "The input is not an integer, please try again...")
        -enterList(CustomMessage = "Please enter a list: ", CustomErrorMessage = "The input is not a valid list, please try again...", ExplicitType = type)
        -__parseCsvRow(row)
        -CsvToMatrix(csvFileName)
        -WriteToCsv(matrix, csvFileName)
        New functions:
        -isiter(object)
        -ModuleAvailability(module_name)
        -TypeclassToString(_type)
        -WriteShell(*text, sep = ' ', end = '\n', Color = 'default', stderr = False, flush = False)
"""

# 1.1
"""
    Minor changes and polishing

    Additions
    ---------
        -When executing this file as a standalone Python executable (instead of importing it), an information message will be printed.
        -Added parameter 'csvDelimiter' to CsvToMatrix() and WritetoCsv() to specify how to separate data in CSV file.
            -Default value is ','
            -Signatures for these functions have been changed:
                -From CsvToMatrix(csvFileName) to CsvToMatrix(csvFileName, csvDelimiter=',')
                -From WriteToCsv(matrix, csvFileName) to WriteToCsv(matrix, csvFileName, csvDelimiter=',')
    
    Changes
    -------
        -Changed signature of isiter() from isiter(object) to isiter(obj).
            ->Since 'object' is a reserved type keyword, that original parameter name will override it.
        -Visual change: for every optional parameter, removed spaces surrounding assignment operator
            -e.g. WriteShell(*text, sep = ' ', end = '\n', Color = 'default', stderr = False, flush = False) changed to WriteShell(*text, sep=' ', end='\n', Color='default', stderr=False, flush=False)
"""

# 2.0
"""
    Released with Assignment 4
    Includes new function

    Additions
    ---------
        -LongestFromList(ls: list)

    Changes
    -------
        -Fixed a small typo in one comment
    
    Bug Fixes
    ---------
        -
"""

# 2.1
"""
    Released with Topics Final Project
    Modified enterInteger's behavior to include a range parameter

    Additions
    ---------
        -

    Changes
    -------
        -Added parameters min and max to enterInteger
    
    Bug Fixes
    ---------
        -
"""
