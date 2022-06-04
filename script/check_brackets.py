# coding: utf-8
# check_brackets: check brackets for each paragraph
import os
import sys

def list_folders_files(path, suffixes_filters = []):
    list_folders = []
    list_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_folders.append(file)
        else:
            file_ext = os.path.splitext(file)[-1]
            ignore_this_file = 0
            if (suffixes_filters is not None):
                ignore_this_file = 1
                for suffix in suffixes_filters:
                    if (file_ext.upper() == suffix.upper()):
                        ignore_this_file = 0
                        break
            if (ignore_this_file == 0):
                list_files.append(file)
    return (list_folders, list_files)


def checkBracketsForLine(fileName, input_line_buff, line_index):
    find_index = input_line_buff.find('<p', 0)
    if (find_index < 0):
        return # only check paragraphes
              
    bracket_content_array = []
    char_array = []
    for index in range(find_index + 2, len(input_line_buff)):
        char = input_line_buff[index : index + 1]
        if ((char == '『') or (char == '「')):
            char_array.append(char)
            bracket_content_array.append(input_line_buff[index : (index + 6)])
        elif ((char == '」') or (char == '』')):
            char_match = ' '
            if (len(char_array) > 0):
                char_match = char_array.pop()
                bracket_content_array.pop()
            
            if (((char == '」') and (char_match != '「')) or ((char == '』') and (char_match != '『'))):
                print ("bracket unbalance-middle. file: %s; line: %d; partial content: %s" % (fileName, line_index + 1, input_line_buff[index : (index + 6)]))
    
    if (len(char_array) > 0):
        str_last_push = bracket_content_array[0]
        print ("bracket unbalance-end. file: %s; line: %d; partial content: %s" % (fileName, line_index + 1, str_last_push))

    
def processFile(path_i, fileName):
    full_path = os.path.join(path_i, fileName)

    # print(full_path)
    print(fileName)

    line_index = 0
    with open(full_path, 'rt') as file:
        for line_string in file:
            if (len(line_string) <= 2):
                line_index += 1
                continue
                
            checkBracketsForLine(fileName, line_string, line_index)
            line_index += 1

if __name__ == '__main__':
    suffixes_filters = []
    suffixes_filters.append(".html")
    
    src_folder = './text'
    (list_folders, list_files) = list_folders_files(src_folder, suffixes_filters)
    print("files: %d" % len(list_files))

    for item in sorted(list_files):
        processFile(src_folder, item)
