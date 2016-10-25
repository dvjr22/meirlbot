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

# Library for doing fuzzy searches on the results
import numpy as np
import Levenshtein as lv
import re
from collections import Counter

def main(_):
    # Array to hold all the keywords as they are read
    #temp = []
    # Open the keywords.txt file and put each line into the keywordArray
    temp = ""
    with open('keywords.txt') as my_file:
        #for line in my_file:
        temp = my_file.read()
        print temp
    #keywordArray = np.array(temp)
    #print temp
    print '\n\n'
    # Write the most common and second most common from the keywordArray
    # to the keywordsCondensed.txt file
    def levenshtein(dist, string):
        return map(lambda x: x<dist, map(lambda x: lv.distance(string, x),keywordArray))

    with open('keywordsCondensed.txt', 'w') as file:

        words = re.findall(r'\w+', temp)
        cap_words = [word.upper() for word in words]
        word_counts = Counter(cap_words)
        print word_counts

        # Pulls out the most common keyword
        #print levenshtein(95,"Me: I\'ll just have one drink, not gonna Bring revolutionary communism to the people of Latin America or anytning Two drinks later: FIDEL CASTRO")

        #print keywordArray[np.where(levenshtein(95,"Me: I\'ll just have one drink, not gonna Bring revolutionary communism to the people of Latin America or anytning Two drinks later: FIDEL CASTRO"))]



        #count = Counter(keywordArray)
        #print count.most_common()[1]
        #print count.most_common()[2]
        #file.write('FIRSTCOMMON=' + mostCommon)

        # Remove all the instances of the most common keyword
        #for index, item in enumerate(keywordArray):
    #        if(item == mostCommon):
    #            keywordArray.pop(index)
        # Find the most common keyword remaining which is the second most
        # common overall
        #secondCommon = max(set(keywordArray), key=keywordArray.count)
        #file.write('SECONDCOMMON=' + secondCommon)

if __name__ == '__main__':
    main("t")
