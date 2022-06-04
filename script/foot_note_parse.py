# coding: utf-8
# file_content_compare.py detect some mismatch content between two files(based on reference file)
import os
import sys

def parseLineFootNote(line_string, file_name, line_index):
    find_index = line_string.find('\\endnotetext')
    if (find_index >= 0):
        print (('file: %s; line: %d; foot_note: %s') % (file_name, line_index + 1, line_string))
        return
    
    find_index = 0
    while (find_index >= 0):
        find_index = line_string.find('\\endnotemark[', find_index)
        if (find_index >= 0):
            index = find_index - 10
            if (index < 0):
                index = 0
            sub_string = line_string[index: (find_index + 17)]
            print (('file: %s; line: %d; foot_note_mark: %s') % (file_name, line_index + 1, sub_string))
            find_index += 15

chapter_cnt = 0
prefix_cnt = 0
def dumpAndParseChapter(line_buff_array):
    global chapter_cnt
    global prefix_cnt

    line_string = line_buff_array[0]
    find_index = line_string.find('第')
    if (find_index >= 0):
        file_name =  ('./chapter_%02d.tex' % (chapter_cnt + 1))
        chapter_cnt += 1
    else:
        file_name =  ('./prefix_%02d.tex' % (prefix_cnt + 1))
        prefix_cnt += 1
            
    with open(file_name, 'wt') as fileDst:
        line_index = 0
        for line_string in line_buff_array:
            parseLineFootNote(line_string, file_name, line_index)
            line_index += 1
            fileDst.write(line_string)

        fileDst.close

def parseFootNote(texFile):
    with open(texFile, 'rt') as fileRef:
        outputLineBuff = []
        for line_string in fileRef:            
            if (len(line_string) <= 1):
                continue

            find_index = line_string.find('\\part*')
            if (find_index >= 0):
                if (len(outputLineBuff) > 0):
                    dumpAndParseChapter(outputLineBuff)
                    outputLineBuff.clear()

            outputLineBuff.append(line_string)

        if (len(outputLineBuff) > 0):
            dumpAndParseChapter(outputLineBuff)
            outputLineBuff.clear()

        fileRef.close()

if __name__ == '__main__':
    parseFootNote('./contents.tex')




