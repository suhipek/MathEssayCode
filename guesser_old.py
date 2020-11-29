#reference: https://github.com/observerss/ngender/blob/master/ngender/ngender.py

symbols = "!@#$%^&*():;/<>.,\"\'\n"

class Guesser():

    def __init__(self):
        self.total = 0
        self.totals = {}
        self.freq = {}
        self.header = []

        with open('freq.csv') as freqFile:
            for i in freqFile.readline().strip('\n').split(',')[1:]:
                self.totals[i] = 0
                self.header.append(i)
            for i in freqFile.readlines():
                freqLine = i.strip('\n').split(',')
                self.freq[freqLine[0]] = freqLine[1:]
                for j in self.totals:
                    self.totals[j] += int(freqLine[self.header.index(j)+1])
            freqFile.close()

        for i in self.freq:
            for j in range(len(self.freq[i])):
                self.freq[i][j] = float(self.freq[i][j]) / self.totals[self.header[j]]
        
        for i in self.totals:
            self.total += self.totals[i]


    def prob(self, words_in_sen, wordCh):
        p = self.totals[wordCh] / self.total
        for word in words_in_sen:
            p *= self.freq.get(word, [0] * len(self.header))[self.header.index(wordCh)] 
        return p

    def guess(self,sen):
        p = {}
        words = map(lambda x: x.lower(),map(lambda x: x.strip(symbols),sen.split()))
        total = 0
        for i in self.header:
            print(i)
            p[i] = self.prob(words,i)
            total += p[i]
        print(p)
        ans = max(p,key=p.get)
        ansp = p[ans] / total
        return ans,ansp

