import pandas as pd

#class yang berisi method yang sering digunakan
class PostProcessing :
        
    #memisahkan kalimat menjadi kata
    def splitWords(String):
        String = String.split(" ")
        while "" in String :
            String.remove("")
        for word in String :
            if word[0] == "#":
                String.remove(word)
        return String

    #memisahkan string dengan koma atau titik menjadi list yang berisi anak kalimat
    def splitSentences(String):
        output = list()
        if "." not in String and "," not in String :
            return String
        String = String.split(".")
        for i in String :
            if "," in i:
                i = i.split(",")
                for j in i :
                    output.append(j)
            else:
                output.append(i)
        return output

    #membersihkan string dari karakter yang tak diinginkan
    def cleanString(String):
        String = String.lower()
        i = 0
        while i < len(String):
            if not((ord(String[i]) >= 97 and ord(String[i]) <= 122) or ord(String[i]) == 32
                   or ord(String[i]) == 46 or ord(String[i]) == 44) :
                String = String.replace(String[i], "")
            else:
                i+=1
        return String

    #return list 2d yang berisi kumpulan kata per kalimat
    def bagOfWordsPerSentence(String):
        output = list()
        String = PostProcessing.cleanString(String)
        sentences = PostProcessing.splitSentences(String)
        for sentence in sentences :
            output.append(PostProcessing.splitWords(sentence))
        return output



class Level2 :
    #field : column, data
    def __init__(self):
        self.data = dict()

    def insert(self, user, word1, word2):
        try :
            self.data[user][word1][word2] += 1
        except :
            try :
                self.data[user][word1][word2] = 1
            except :
                try:
                    self.data[user][word1] = dict()
                    self.data[user][word1][word2] = 1
                except :
                    self.data[user] = dict()
                    self.data[user][word1] = dict()
                    self.data[user][word1][word2] = 1

    def toCsv(self, path):
        data = dict()
        data["user"] = list()
        data["word1"] = list()
        data["word2"] = list()
        data["freqs"] = list()
        for user in self.data :
            for word1 in self.data[user] :
                for word2 in self.data[user][word1]:
                    data["user"].append(user)
                    data["word1"].append(word1)
                    data["word2"].append(word2)
                    data["freqs"].append(self.data[user][word1][word2])

        self.df = pd.DataFrame(data)
        self.df.to_csv(path, index=False)

    def level1ToLevel2(self, dfLevel1):
        users = list(dfLevel1["ACCOUNTS"])
        posts = list(dfLevel1["POSTS"])
        for i in range(len(users)) :
            print(str(i) + " rows have been processed")
            user = users[i]
            bagOfWordsPerSentence = PostProcessing.bagOfWordsPerSentence(str(posts[i]))
            for words in bagOfWordsPerSentence :
                for j in range(len(words)-1):
                    self.insert(user, words[j], words[j+1])
                    
                
                    

#main program
if __name__ == "__main__":
    level2 = Level2()
    df = pd.read_csv("level 1.csv")
    level2.level1ToLevel2(df)
    level2.toCsv("level 2.csv")
    print("Conversion done")
            
