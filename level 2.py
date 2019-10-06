import pandas as pd

#memisahkan kalimant menjadi kata
def splitWords(String):
    String = String.split(" ")
    while "" in String :
        String.remove("")
    return String

#memisahkan string dengan koma atau titik menjadi list yang berisi kalimat
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

#mencari index dictionary sebuah pair words, return -1 jika tidak ada
def findIndex(dictionary, id_user, word1, word2):
    for i in range(len(dictionary["id_user"])): 
        if dictionary["word2"][i] == word2:
            if dictionary["word1"][i] == word1 :
                if dictionary["id_user"][i] == id_user :
                    return i

    return -1


#membaca dataset level 1
db1 = pd.read_csv("level 1.csv").loc[: , ["ACCOUNTS", "POSTS"]]
data = {"id_user" : [], "word1" : [], "word2" : [], "freqs" : []}


#membuat id_user
account_code = dict()
code = 0
for i in db1["ACCOUNTS"]:
    if i not in account_code :
        account_code[i] = code
        code += 1

#memeriksa semua row db1
for i in range(len(db1["ACCOUNTS"])):
    id_user = account_code[db1.loc[i]["ACCOUNTS"]]
    #memecah post menjadi beberapa kalimat
    post = splitSentences(cleanString(db1.loc[i]["POSTS"]))
    for sentence in post :
        #memecah kalimat menjadi beberapa kata
        words = splitWords(sentence)
        for j in range(len(words)-1):
            index = findIndex(data, id_user, words[j], words[j+1])
            if(index != -1):
                data["freqs"][index] += 1
            else :
                data["id_user"].append(id_user)
                data["word1"].append(words[j])
                data["word2"].append(words[j+1])
                data["freqs"].append(1)

    print(i)

db2 = pd.DataFrame(data)
db2.to_csv("level 2.csv", index = False)


