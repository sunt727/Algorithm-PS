def sort_anagrams(words):
    '''
    Sort anagrams to appear adjacent to each other in a returned list.
    Input:  list of strings which contain only lower-case letters
    Output: sorted list, with anagrams appearing consecutively
    '''

    letters = 'abcdefghijklmnopqrstuvwxyz'
    histograms = {}  # map a word to its histogram
    for word in words:
        basic = [0]*26
        wordlist = list(word)
        for letter in set(wordlist):  # avoid duplicated letters
            index = list(letters).index(letter)  # get the order of alphabet
            basic[index] = wordlist.count(letter)
        histograms[word] = basic


    def countSort(l, k):
        '''input a word list, counting sort it by k th English letter'''
        # make an empty list formatted as words list
        output = [""] * len(l)

        # assume no English word includes more than 19 same letters
        count = [0]*20

        # store the count of the kth English letter of each word to the previous step
        for word in l:
            count[histograms[word][k]+1] += 1

        # Swift to real index
        for i in range(len(count)):
            count[i] += count[i - 1]

        # build a output list
        for i in range(len(l)):
            # insert the word by following the order we see it
            output[count[histograms[l[i]][k]]] = l[i]
            # go to the next position of this count
            count[histograms[l[i]][k]] += 1

        # show the steps for debugging
        # print(output) if output != l else print('nothing change')

        # inject output list into the original list
        l[:] = output
        return l

    # radix sort by counting sort the words by z-a order
    for i in range(26):
        countSort(words, 25-i)

    return words
