import copy

symbols = "!?@#$%^&*():;/<>.,\"\'\n"

def get_freq(sentences):
    freq = {}
    for i in sentences:
        for j in i.split():
            word = j.strip(symbols).lower()
            if word != "": freq[word] = freq.get(word, 0) + 1
    return freq

def dict_sum(dicts):
    new_dict = {}
    for i in dicts:
        for j in i:
            new_dict[j] = []
    for n in range(len(dicts)):
        for i in new_dict:
            new_dict[i].append(dicts[n].get(i,0))
    return new_dict


if __name__ == "__main__":
    wordsCh = []
    freq = []
    with open('words.csv') as wordsFile:
        for i in wordsFile.readlines():
            wordEn = i.split(',')[0]
            wordsCh.append(i.split(',')[1])
        wordsFile.close()
    with open('freq.csv', mode='w') as freqFile:
        freqFile.write(','.join(['words']+wordsCh)+'\n')
        for wordCh in wordsCh:
            with open('{}_{}.txt'.format(wordEn,wordCh)) as sentencesFile:
                freq.append(get_freq(sentencesFile.readlines()))
                sentencesFile.close()
        temp_dict = dict_sum(freq)
        for i in temp_dict:
            print(i)
            print(temp_dict[i])
            freqFile.write(','.join(map(str, [i]+list(map(lambda x: x + 1,temp_dict[i]))))+'\n')    

