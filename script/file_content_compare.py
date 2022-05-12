# coding: utf-8
# file_content_compare.py detect some mismatch content between two files(based on reference file)
import os
import sys
import re # only for python3+

log_string_array = []

#  assume same:
    # strContent = strContent.replace('環', '鬟')
    # strContent = strContent.replace('嚐', '嘗')
    # strContent = strContent.replace('盡', '儘')
    
str_tongjia_l = '真值鎮填慎顛青清鐘裏為既眾讚清泄著諡跡敘教皂羡飲蹤概卻郎抬闊豔樑告丟唧嫻群鉤腳説託躲朵閑蔥姦兇鄉歎啟簷聼汙污階撐冤駡嫋屏氊舐昂研耽插遊喂丰筍妝夀墜韭迥冊輒垛拋妍髪荊煙笄喻鯗騭'

# in reference Tex:
str_tongjia_r = '眞値鎭塡愼顚靑淸鍾裡爲旣衆贊淸洩着謚蹟敍敎皀羨飮踪槪却郞擡濶艷梁吿丢喞嫺羣鈎脚說托躱朶閒葱奸凶鄕嘆啓檐聽汚汚堦撑寃罵嬝屛氈䑛昻硏躭揷游餵丯笋粧壽堕韮逈册輙垜抛姸髮荆烟筓喩鮝隲'

def preProcessMatchString(strContent):
    global str_tongjia_l, str_tongjia_r

    strContent = strContent.replace('　', '')
    for index in range(0, len(str_tongjia_l)):
        strContent = strContent.replace(str_tongjia_l[index], str_tongjia_r[index])

    return strContent

def tongjia_same(str1, str2):
    if (str1 == str2):
        return True

    global str_tongjia_l, str_tongjia_r

    for index in range(0, len(str_tongjia_l)):
        if (str1 == str_tongjia_l[index] and str2 == str_tongjia_r[index]):
            return True

        if (str1 == str_tongjia_r[index] and str2== str_tongjia_l[index]):
            return True

    return False

def evaluateSimilarity(str1, str2, line_index, print_out):
    global log_string_array

    if (len(str1) != len(str2)):
        if (line_index >= 0):
            log_string_array.append(('------------lengt hmismatch! line: %d; str1: %s; str2: %s' % (line_index + 1, str1, str2)))
        return len(str1)

    mismatchCnt = 0
    index = 0
    str_mis_match = ''
    while index < len(str1):
        str_l = str1[index:index + 1]
        str_r = str2[index:index + 1]
        if tongjia_same(str_l, str_r):
            index += 1
            continue

        if (len(str_mis_match) > 0):
            str_mis_match += ' '

        str_mis_match += str_l + '->' + str_r
        mismatchCnt += 1

        index += 1

    if ((mismatchCnt > 0) and (mismatchCnt <= len(str1) / 2) and print_out):
        log_string_array.append("partial matched? line: %d. content: %s; mismatch: (%d)%s; ref: %s" % (line_index + 1, str1, mismatchCnt, str_mis_match, str2))

    return mismatchCnt

def fuzzyMatchLine(strContent, lineBufRef, start_index_ref):
    mismatchCharactes = len(strContent)
    start_index = 1
    sub_str_ref = ''

    while True:
        # discard head part:
        sub_str = strContent[start_index : ]
        find_index = lineBufRef.find(sub_str, start_index_ref)
        if (find_index >= start_index):
            sub_str_ref = lineBufRef[find_index - start_index : find_index - start_index + len(strContent)]
            mismatchCharactes = evaluateSimilarity(strContent, sub_str_ref, -1, False)
            return (mismatchCharactes, find_index - start_index)

        # discard tail part:
        sub_str = strContent[0 : (len(strContent) - start_index)]
        find_index = lineBufRef.find(sub_str, start_index_ref)
        if (find_index >= start_index):
            sub_str_ref = lineBufRef[find_index : find_index + len(strContent)]
            mismatchCharactes = evaluateSimilarity(strContent, sub_str_ref, -1, False)
            return (mismatchCharactes, find_index)

        # discard bothhead & tail part:
        sub_str = strContent[start_index : (len(strContent) - start_index)]
        if (len(sub_str) >= 2):
            sub_str = strContent[start_index: len(strContent) - start_index]
            find_index = lineBufRef.find(sub_str, start_index_ref)
            if (find_index >= start_index):
                sub_str_ref = lineBufRef[find_index - start_index: find_index - start_index + len(strContent)]
                mismatchCharactes = evaluateSimilarity(strContent, sub_str_ref, -1, False)
                return (mismatchCharactes, find_index - start_index)

        if (start_index >= 2):
            sub_str = strContent[0 : start_index]
            find_index = lineBufRef.find(sub_str, start_index_ref)
            if (find_index >= 0):
                sub_str_ref = lineBufRef[find_index: find_index + len(strContent)]
                mismatchCharactes = evaluateSimilarity(strContent, sub_str_ref, -1, False)
                return (mismatchCharactes, find_index)

            start_index1 = (len(strContent) - 1 - start_index)
            sub_str = strContent[start_index1 :]
            find_index = lineBufRef.find(sub_str, start_index_ref)
            if (find_index >= start_index1):
                sub_str_ref = lineBufRef[find_index - start_index1: find_index - start_index1 + len(strContent)]
                mismatchCharactes = evaluateSimilarity(strContent, sub_str_ref, -1, False)
                return (mismatchCharactes, find_index - start_index1)

        start_index += 1
        if (start_index > len(strContent) / 2):
            break

    return (len(strContent), -1)

def fuzzyMatch(strContent, refLineBuf, line_index):
    original_content = '' + strContent # copy
    strContent = preProcessMatchString(strContent)

    for line_string in refLineBuf:
        if (line_string.find(strContent) >= 0):
            return 0 # happy!

    minMismatch = len(strContent)
    str_most_match = ''

    for line_string in refLineBuf:
        ref_start_index = 0
        while True:
            [mismatchCharactes, first_match_place] = fuzzyMatchLine(strContent, line_string, ref_start_index)
            if ((mismatchCharactes >= len(strContent)) or (first_match_place < 0)):
                first_match_place = -5
                break   # give-up

            if (mismatchCharactes < minMismatch):
                str_most_match = line_string[first_match_place : first_match_place + len(strContent)]
                minMismatch = mismatchCharactes

            if (mismatchCharactes <= 2):
                # good!
                break

            ref_start_index = first_match_place + len(strContent)
            if ((ref_start_index + len(strContent) / 2) >= len(line_string)):
                break # give-up!

        if (minMismatch <= 1 and len(strContent) <= 6):
            evaluateSimilarity(original_content, str_most_match, line_index, True)
            return minMismatch
        elif (minMismatch <= 2):
            evaluateSimilarity(original_content, str_most_match, line_index, True)
            return minMismatch

    evaluateSimilarity(original_content, str_most_match, line_index, True)

    return len(strContent)

def doCompareLine(line_string, line_index, refLineBuf):
    global log_string_array

    if (line_string.find('<h') >= 0):
        index = line_string.find('　')  # 2-characters space
        if (index < 0):
            return

        index1 = line_string.find('</h', index)
        if (index1 > index):
            title_str = line_string[(index + 1) : index1]
            # print ("found title: %s in line %d" % (title_str, (line_index + 1)))
            fuzzyMatch(title_str, refLineBuf, line_index)

        return

    if (line_string.find('<p') < 0):
        # ignore non-paragraph lines
        return

    index = line_string.find('>')
    index += 1

    str_prev = ''
    index_end = line_string.find('</p>')
    while (index <= index_end):
        index1 = line_string.find('<', index)
        if (index1 > 0):
            str_content = line_string[index : index1]
            if (len(str_content) <= 3):
                str_prev = str_content
            else:
                str = str_prev + str_content
                str_prev = ''

                # ignore following characters:
                '''
                str = str.replace('「', '')
                str = str.replace('」', '')

                str = str.replace('『', '')
                str = str.replace('』', '')

                str = str.replace('（', '')
                str = str.replace('）', '')
                '''

                str = str.replace('《', '')
                str = str.replace('》', '')

                str = str.replace('、', '')

                split_str_array = re.split('。|，|？|！|：|「|」|『|』|；', str)

                str_prev = ''
                for str_item in split_str_array:
                    if (len(str_item) <= 0):
                        continue

                    str_merged = str_prev + str_item
                    str_prev = ''
                    if (len(str_merged) <= 2):
                        str_prev = str_merged
                    else:
                        misMatch = fuzzyMatch(str_merged, refLineBuf, line_index)
                        if ((misMatch >= 1) and (len(str_merged) <= 8)):
                            str_prev = str_merged
                            if (len(log_string_array) > 0):
                                # del log_string_array[-1]
                                log_string_array.pop(-1) # remove last

                # last part:
                if (len(str_prev) > 0):
                    misMatch = fuzzyMatch(str_merged, refLineBuf, line_index)
                    str_prev = ''

        if (index1 >= index_end):
            break

        index1 = line_string.find('>', index + 1)
        if (index1 < 0):
            break

        index = index1 + 1

    return

def processCompare(refFile, compareFile):
    global log_string_array

    refLineBuf = []
    with open(refFile, 'rt') as fileRef:
        for line_string in fileRef:
            if (len(line_string) <= 1):
                continue

            line_string = line_string.replace('。', '') # this because the reference content may too much brokened
            line_string = line_string.replace('：', '')
            line_string = line_string.replace('「', '')
            line_string = line_string.replace('」', '')
            line_string = line_string.replace('『', '')
            line_string = line_string.replace('』', '')

            line_string = line_string.replace('　', '') # 2characters space
            refLineBuf.append(line_string)

        fileRef.close()

    if (len(refLineBuf) == 0):
        print ("warning: nothing to do. empty referen file!")
        return

    with open(compareFile, 'rt') as fileCompare:
        line_index = 0
        for line_string in fileCompare:
            if (len(line_string) > 2):
                doCompareLine(line_string, line_index, refLineBuf)
            line_index += 1

        fileCompare.close()

    for log_str in log_string_array:
        print (log_str)

if __name__ == '__main__':
    ref_file = ''
    compare_file = ''
    num_argv = len(sys.argv)

    for index in range(1, num_argv):
        if ((index + 1) < num_argv):
            if (((sys.argv[index]).lower() == '-r') or ((sys.argv[index]).lower() == '-ref')):
                if (len(ref_file) == 0):
                    ref_file = sys.argv[index + 1]
            elif (((sys.argv[index]).lower() == '-t') or ((sys.argv[index]).lower() == '-target')):
                if (len(compare_file) == 0):
                    compare_file = sys.argv[index + 1]

    if ((len(ref_file) == 0) or (len(compare_file) == 0)):
        print (("usage: %s -r <specific reference file> -t <specific comparing file>") % (sys.argv[0]))
    else:
        print (('ref_file: %s; compare file: %s') % (ref_file, compare_file))
        # processCompare(ref_file, compare_file)

    processCompare('part_01_ref.tex', 'chapter_001.html')




