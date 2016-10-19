import sys
keywordArray = []
with open('keywords.txt') as my_file:
    for line in my_file:
        keywordArray.append(line)
#print('\n' + max(set(keywordArray), key=keywordArray.count))

with open('keywordsCondensed.txt', 'w') as file:
    mostCommon = max(set(keywordArray), key=keywordArray.count)
    file.write('FIRSTCOMMON=' + mostCommon)
    for index, item in enumerate(keywordArray):
        if(item == mostCommon):
            keywordArray.pop(index)
    secondCommon = max(set(keywordArray), key=keywordArray.count)
    file.write('SECONDCOMMON=' + secondCommon)
