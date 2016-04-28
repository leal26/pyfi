# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 21:15:49 2016

@author: Pedro
"""
from datetime import datetime

def output_reader(filename, separator='\t', output=None, rows_to_skip=0,
                  header=0, type_data = None):
    """
    Function that opens files of any kind. Able to skip rows and
    read headers if necessary.

    Inputs:
        - filename: just the name of the file to read.

        - separator: Main kind of separator in file. The code will
          replace any variants of this separator for processing. Extra
          components such as end-line, kg m are all eliminated.

        - output: defines what the kind of file we are opening to
          ensure we can skip the right amount of lines. By default it
          is None so it can open any other file.

        - rows_to_skip: amount of rows to initialy skip in the file. If
          the output is different then None, for the different types of
          files it is defined as:
          - Polar files = 10
          - Dump files = 0
          - Cp files = 2
          - Coordinates = 1

        - header: The header list will act as the keys of the output
          dictionary. For the function to work, a header IS necessary.
          If not specified by the user, the function will assume that
          the header can be found in the file that it is opening.
          
        - type_data: if defined, has the same length of the number of 
          columns in the file and tells output_reader how to process
          the data. 'time' will return datetime objects, 'float' will
          return floats.

    Output:
        - Dictionary with all the header values as keys

    Created on Thu Mar 14 2014
    @author: Pedro Leal
    """

    # In case we are using an XFOIL file, we define the number of rows
    # skipped
    if output == 'Polar' or output == 'Alfa_L_0':
        rows_to_skip = 10
    elif output == 'Dump':
        rows_to_skip = 0
    elif output == 'Cp':
        rows_to_skip = 2
    elif output == 'Coordinates':
        rows_to_skip = 1
    # n is the amount of lines to skip
    Data = {}
    if header != 0:
        header_done = True
        for head in header:
            Data[head] = []
    else:
        header_done = False
    count_skip = 0

    with open (filename, "r") as myfile:
        # Jump first lines which are useless
        for line in myfile:
            if count_skip < rows_to_skip:
                count_skip += 1
                # Basically do nothing
            elif header_done == False:
                # If the user did not specify the header the code will
                # read the first line after the skipped rows as the
                # header
                if header == 0:
                    # Open line and replace anything we do not want (
                    # variants of the separator and units)
                    line = line.replace(separator + separator + separator +
                    separator + separator + separator, ' ').replace(separator
                    + separator + separator + separator + separator,
                    ' ').replace(separator + separator + separator +
                    separator, ' ').replace(separator + separator + separator,
                    ' ').replace(separator + separator, ' ').replace("\n",
                    "").replace("(kg)", "").replace("(m)", "").replace("(Pa)",
                    "").replace("(in)", "").replace("#", "").replace(separator,
                    ' ')

                    header = line.split(' ')
                    n_del = header.count('')
                    for n_del in range(0, n_del):
                        header.remove('')
                    for head in header:
                        Data[head] = []
                    # To avoid having two headers, we assign the False
                    # value to header which will not let it happen
                    header_done = True
                # If the user defines a list of values for the header,
                # the code reads it and creates libraries with it.
                elif type(header) == list:
                    for head in header:
                        Data[head] = []
                    header_done = True
            else:
                line = line.replace(separator + separator + separator,
                ' ').replace(separator + separator, ' ').replace(separator,
                ' ').replace("\n", "").replace('---------', '').replace(
                '--------', '').replace('-------', '').replace('------',
                '')

                line_components = line.split(' ')

                n_del = line_components.count('')
                for n in range(0, n_del):
                    line_components.remove('')

                if line_components != []:
                    if type_data == None:
                        for j in range(0, len(line_components)):
                            Data[header[j]].append(float(line_components[j]))
                    else:
                        for j in range(0, len(line_components)):
                            if type_data[j] == 'float':
                                Data[header[j]].append(float(line_components[j])) 
                            elif type_data[j] == 'time':
                                time_object = datetime.strptime(line_components[j],'%Y-%m-%d')
                                Data[header[j]].append(time_object)                        
                # else DO NOTHING!
    return Data

if __name__ == '__main__':
    data = output_reader('history_BOND.csv', separator = ',', type_data = ['time',
                         'float', 'float', 'float', 'float', 'float', 'float'])