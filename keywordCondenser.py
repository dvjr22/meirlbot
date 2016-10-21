############################################################
#                     Keyword Condenser                    #
# Creator: Tyler Moon                                      #
# Contributors:                                            #
# Purpose: This is a simple script to take the long list   #
# of keywords from the keywords.txt file and find the top  #
# two most common lines out of it and write those to the   #
# file keywordsCondensed.txt                               #
############################################################


import sys

# Array to hold all the keywords as they are read
keywordArray = []

# Open the keywords.txt file and put each line into the keywordArray
with open('keywords.txt') as my_file:
    for line in my_file:
        keywordArray.append(line)

# Write the most common and second most common from the keywordArray
# to the keywordsCondensed.txt file
with open('keywordsCondensed.txt', 'w') as file:
    # Pulls out the most common keyword
    mostCommon = max(set(keywordArray), key=keywordArray.count)
    file.write('FIRSTCOMMON=' + mostCommon)

    # Remove all the instances of the most common keyword
    for index, item in enumerate(keywordArray):
        if(item == mostCommon):
            keywordArray.pop(index)
    # Find the most common keyword remaining which is the second most
    # common overall
    secondCommon = max(set(keywordArray), key=keywordArray.count)
    file.write('SECONDCOMMON=' + secondCommon)
