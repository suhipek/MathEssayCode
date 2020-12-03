#reference: https://github.com/observerss/ngender/blob/master/ngender/ngender.py

DONT_BE_TOO_SMALL = 1600  # 防止太小的数相乘导致尾数溢出，最后都是算比例比大小所以不影响
symbols = "!?@#$%^&*():;/<>.,\"\'\n"  # 特殊符号表
strip_symbols = lambda x: x.strip(symbols)  # 去除字符串两端特殊符号
split_by_comma = lambda x: x.split(',')  # 将字符串用逗号分开

def read_csv(file_name='freq.csv'):  # 读取csv文件的函数
    with open(file_name) as file_obj:
         csv_list = map(strip_symbols, file_obj.readlines())  # 去除换行符
         file_obj.close()
         return list(map(split_by_comma, csv_list))  # 转换为二维列表

class Guesser():

    def __init__(self):
        self.total_each_meaning = []  # 原型词作某一义项的文本量，顺序和meanings一致
        self.pxm = {}  # 存储个义项的频率，也就是P(X_m)
        self.freq = {}  
        # 原型词作某一义项的文本中单词n出现的频率，存储在字典值中，顺序和meanings一致
        self.meanings = []  # 这个list顺序很重要，freq的value都是按他的顺序排序的字典
        data = read_csv()
        self.meanings = data[0][1:]  # 将表头中的义项存起来
        pxm_data = read_csv('words.csv')
        
        for line in pxm_data:
            self.pxm[line[1]] = float(line[3])

        for index in range(len(self.meanings)):  # 按照顺序统计原型词作各义项的文本量
            times_of_meaning = map(int, [line[index + 1] for line in data[1:]])
            self.total_each_meaning.append(sum(times_of_meaning))
        
        for line in data[1:]:  # 计算原型词作某一义项的文本中单词line[0]出现的频率
            self.freq[line[0]] = \
                [(int(line[index + 1]) * DONT_BE_TOO_SMALL / \
                    self.total_each_meaning[index]) \
                        for index in range(len(self.meanings))]

    def prob(self, words_list: list, meaning: str):
        meaning_index = self.meanings.index(meaning)  # 保存义项的索引备用
        p = self.pxm[meaning]
        for word in words_list:  # 遍历句中所有词，并将p自乘P(Y_n | X_m)
            p *= self.freq.get(word, (1, 1))[meaning_index]  # 没这个词就返回1(平滑)
        return p  # 返回计算到的P(X_m | Y_1,Y_2,…,Y_n)（其实少除了一个P(Y_1,Y_2,…,Y_n)）

    def guess(self, sentence: str):
        p = {}  # 所有P(X_m | Y_1,Y_2,…,Y_n)
        total = max_p = 0  
        # 所有P(X_m | Y_1,Y_2,…,Y_n)之和，最大的所有P(X_m | Y_1,Y_2,…,Y_n)
        words_list = list(map(strip_symbols, sentence.lower().split()))  # 分词
        for m in self.meanings:  # 调用prob函数计算所有的义项的可能性
            si_prob = self.prob(words_list, m)
            p[m] = si_prob
            total += si_prob
        for i in p:  # 计算可能性最大的义项
            if p[i] > max_p:
                ans, ansp, max_p = i, p[i] / total, p[i]
                # 计算该义项的真正的P(X_m | Y_1,Y_2,…,Y_n)
        return ans, ansp

if  __name__ == "__main__":
    g = Guesser()
    wrong = right = 0
    with open('stock_股票.txt') as f:
        for i in f.readlines():
            if g.guess(i)[0] == '股票':
                right += 1
            else: wrong += 1
        f.close()
    print(right)
    print(wrong)