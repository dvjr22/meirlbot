import sys
def main(temp):
    keywordArray = []
    with open('keywords.txt') as my_file:
        for line in my_file:
            keywordArray.append(line.rstrip())
            print(line.rstrip())
    print('\n' + max(set(keywordArray), key=keywordArray.count))

    with open('keywords.txt', 'w') as file:
        file.write(max(set(keywordArray), key=keywordArray.count))

if __name__ == '__main__':
    main("yeah")
