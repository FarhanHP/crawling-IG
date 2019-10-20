import pandas as pd
from pymongo import MongoClient

class Interface :
    def mainMenu():
        print("(1)\tWord Prediction\n"
              "(2)\tEvery Users' Post With Most Like\n"
              "(3)\tEvery Users' Post With Least Like\n"
              "(4)\tPosts With Certain Hashtags\n"
              "(5)\tTop Hashtags\n"
              "(else)\tExit Program")
        return input("Input : ")

    def wordPredict():
        return input("Input a word to predict : ").lower()

    def postWithCertainHashtags():
        return input("Input hashtags separated with space : ").replace("#", "").split(" ")

    def topHashtags():
        return input("Ammount of top hashtags : ")

class Database :
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client["CrawlingIG"]

    #memasukkan csv ke collection mongodb
    def insertCsvAsCollection(self, path, collectionName):
        df = pd.read_csv(path)
        #menghapus collection dengan nama yang sama
        self.db[collectionName].drop()
        self.db[collectionName].insert_many(df.to_dict("records"))

    #query mongodb dan return collection berbentuk list
    def query(self, collectionName, condition):
        return list(self.db[collectionName].find(condition))

    #getter untuk collection yang ada pada Database
    def getCollection(self, collectionName):
        return self.db[collectionName]

class Level1:
    def __init__(self, database, collectionName):
        self.db = database
        self.col = self.db.getCollection(collectionName)
        self.users = list()

        for row in self.col.find():
            if row["ACCOUNTS"] not in self.users :
                self.users.append(row["ACCOUNTS"])

    #get documents with most or least "LIKES" per users
    def getTopPostPerUser(self, top=True):
        output = list()
        for user in self.users :
            neededRows = list(self.col.find({"ACCOUNTS" : user}))
            tempRow = neededRows[0]
            for row in neededRows :
                if top and int(row["LIKES"]) > int(tempRow["LIKES"]):
                    tempRow = row
                elif not top and int(row["LIKES"]) < int(tempRow["LIKES"]):
                    tempRow = row
            output.append(tempRow)
        return output

    #get documents with certain hashtags
    def getPostBaseOnHashtags(self, hashtags):
        output = list()
        for row in self.col.find():
            eligible = True
            for hashtag in hashtags :
                if "#"+hashtag not in row["TAGS"].replace("[","").replace("]","").replace("'", "").split(", "):
                    eligible = False
                    break 
            if eligible :
                output.append(row)
        return output

    def getTopHashtags(self, ammount):
        hashtagsFreqs = dict()
        topTenHashtagsFreqs = dict()
        hashtags = list()
        for row in self.col.find() :
            hashtags.append(row["TAGS"].replace("[", "").replace("]", "").replace("'", "").split(", "))

        #menghitung freqs setiap hashtag di data
        for hashtagsPerRow in hashtags :
            for hashtag in hashtagsPerRow :
                if hashtag != "":
                    if hashtag in hashtagsFreqs:
                        hashtagsFreqs[hashtag] += 1
                    else :
                        hashtagsFreqs[hashtag] = 1

        for hashtag in hashtagsFreqs :
            if len(topTenHashtagsFreqs) <= int(ammount) :
                topTenHashtagsFreqs[hashtag] = hashtagsFreqs[hashtag]
            else :
                temp = [hashtag, hashtagsFreqs[hashtag]]
                for v in topTenHashtagsFreqs :
                    if topTenHashtagsFreqs[v] < temp[1] :
                        topTenHashtagsFreqs[temp[0]] = temp[1]
                        temp[0] = v
                        temp[1] = topTenHashtagsFreqs.pop(v)

        return topTenHashtagsFreqs
        

class Level2:
    def __init__(self, database, collectionName):
        self.db = database
        self.col = self.db.getCollection(collectionName)
        self.totalFreqs = 0
        
        for row in self.col.find():
            self.totalFreqs += row["freqs"]
        
    #menghasilkan prediksi kata selanjutnya dengan menggunakan naive bayes
    def naiveBayes(self, word1):
        #rows yang berisi "word1" == word1
        neededRows = list(self.col.find({"word1" : word1}))
        #menyimpan word2 beserta frequensinya
        words2freqs = dict()
        #menyimpan word2 yang berbeda pada "word1" == word1
        words2 = dict()
        #nilai p(word1)
        pWord1 = 0
        totalFreqs = 0

        visitedWords = list()
        for row in neededRows :
            #untuk menghindari proses perhitungan lama maka kandidat word2 hanya 5 besar
            if row["word2"] not in visitedWords:
                visitedWords.append(row["word2"])
                if len(words2) <= 5 :
                    words2[row["word2"]] = row["freqs"]
                else :
                    temp = [row["word2"], row["freqs"]]
                    for key in words2 :
                        if words2[key] < temp[1]:
                            words2[temp[0]] = temp[1]
                            temp[1] = words2.pop(key)
                            temp[0] = key
            totalFreqs += row["freqs"]

        #menghitung frequensi masing2 words2 pada data secara keseluruhan
        for key in words2 :
            words2freqs[key] = 0
            tempRows = self.col.find({"word2" : key})
            for row in tempRows :
                words2freqs[key] += row["freqs"]

        pWord1 = totalFreqs / self.totalFreqs

        #menghitung naive bayes
        output = None
        for word2 in words2 :
            if output == None :
                output = word2
                
            #nilai p(word1|word2)
            pWord1Word2 = 0
            #nilai p(word2)
            pWord2 = 0
            
            for row in neededRows :
                if row["word2"] == word2:
                    pWord1Word2 += row["freqs"]
            pWord1Word2 /= words2freqs[word2]

            for row in self.col.find({"word2" : word2}, {"freqs" : 1}):
                pWord2 += row["freqs"]

            pWord2 /= self.totalFreqs

            #p(word2|word1) = (p(word1|word2)*p(word2))/p(word1)
            words2[word2] = (pWord1Word2*pWord2)/pWord1

            if words2[output] < words2[word2]:
                output = word2

        return output
            

if __name__ == "__main__" :
    db = Database()
    print("load level 1.csv to mongoDb")
    db.insertCsvAsCollection("level 1.csv", "level_1")
    level1 = Level1(db, "level_1")
    print("load level 2.csv to mongoDb")
    db.insertCsvAsCollection("level 2.csv", "level_2")
    level2 = Level2(db, "level_2")
    print("loading csv done\n\n")
    
    while True :
        try:
            command = Interface.mainMenu()
            if int(command) == 1 :
                #ditambahkan .split(" ") untuk mengantisipasi jika yang diinput adalah kalimat
                word1 = Interface.wordPredict()
                word = word1.split(" ")
                try :
                    print("Result : "+ word1 + " " + level2.naiveBayes(word[-1]))
                except :
                    print("Result : "+word1)
                print("\n\n")
            elif int(command) == 2 :
                rows = level1.getTopPostPerUser()
                for row in rows :
                    print(row)
                    print("\n\n")
            elif int(command) == 3 :
                rows = level1.getTopPostPerUser(False)
                for row in rows :
                    print(row)
                    print("\n\n")
            elif int(command) == 4 :
                hashtags = Interface.postWithCertainHashtags()
                rows = level1.getPostBaseOnHashtags(hashtags)
                for row in rows :
                    print(row)
                    print("\n\n")
            elif int(command) == 5 :
                output = level1.getTopHashtags(Interface.topHashtags())
                #print berurut dari yang terbesar
                while len(output) > 0 :
                    big = None
                    for i in output :
                        if big == None :
                            big = i
                        else :
                            if output[big] < output[i]:
                                big = i
                    print(big+"\t : "+str(output[big])+"\n")
                    output.pop(big)
            else :
                break
        except :
            break
        
