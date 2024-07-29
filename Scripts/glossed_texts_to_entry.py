# -*- coding: utf-8 -*-

import os # package for accesing file structures
import string # package for manipulating strings
import re # package for regular expressions
import random

# Define function that strips 
def gloss_strip(sub1, sub2, text):
    # initializing substrings
    s=str(re.escape(sub1))
    e=str(re.escape(sub2))
    try:
        res=re.findall(s+"([^"+e+"]*)"+e,text)[0]
    except:
        res="?"
    return res

def gloss_sub(sub1, sub2, text):
    s=str(re.escape(sub1))
    e=str(re.escape(sub2))
    res = re.sub(s+"([^"+e+"]*)"+e,'',text)
    return res

def gloss_clean(text):
    clean = re.sub(r"\\glt ", "", text.strip())
    clean = re.sub(r"\\gll ", "", clean)
    clean = re.sub("\\\\\\\\", "", clean)
    clean = re.sub(", ", ",", clean)
    clean = re.sub(" ", ",", clean)
    # clean = re.sub("=", ",", clean)
    return clean

def ipa_con(text):
    res = re.sub("a", "A", text)
    res = re.sub("c", "\\\\t{dZ}", res)
    res = re.sub("ç", "\\\\t{tS}", res)
    res = re.sub("ε", "E", res)
    res = re.sub("e", "{\\\\ae}", res)
    res = re.sub("ê", "e", res)
    res = re.sub("i", "9", res)
    res = re.sub("î", "i", res)
    res = re.sub("j", "Z", res)
    res = re.sub("o", "o", res)
    res = re.sub("r", "R", res)
    res = re.sub("ř", "r", res)
    res = re.sub("ş", "S", res)
    res = re.sub("u", "8", res)
    res = re.sub("û", "u", res)
    res = re.sub("y", "j", res)
    res = re.sub("ġ", "K", res)
    res = re.sub("x", "X", res)
    res = re.sub("đ", "D", res)
    return res

def create_entry(entry):
    key2 = entry
    key2 = re.sub("ā-ā", "a-(a)", key2)
    key2 = re.sub("ā-ē", "(a)-ê", key2)
    key2 = re.sub("e-ā", "(e)-a", key2)
    key2 = re.sub("ā-e", "a-(e)", key2)
    key2 = re.sub("e-ē", "(e)-ê", key2)
    key2 = re.sub("ē-e", "ê-(e)", key2) #
    key2 = re.sub("e-e", "e-(e)", key2) #
    key2 = re.sub("e-û", "e-w", key2) #
    key2 = re.sub("-", "", key2) #
    return key2

# # Set boolean variable that controlls  morpheme spacing
spacebool = False

scList = []


dicText = {"headword": {"word-gloss": ['location']}}
defList = []
dicRefin = {}

# Select file name
file = "Glossed texts"
# # Initialize line variables
# opening = ""
label = ""
sentence = ""
words = []
glosses = []
headwords = []
trans = ""
# parsing = ""
# gloss = ""
# translation = ""
# close = ""

# Open file
with open(file + '_test_dic.tex', 'w', encoding="utf-8") as txtfile:
    # Process all dictionary entries
    with open(file + '.tex', encoding='utf-8') as readfile:
        for line in readfile:
            if "label" in line:
                label = gloss_strip("label{", "}", line)
            elif "textit" in line:
                sentence = line.strip()
            elif "gll" in line:
                words = gloss_clean(line).split(",")
                # print(words)
                # words = remove_items(words, '')
                spacebool = True
            elif spacebool:
                glosses = gloss_clean(line).split(",")
                headwords = []
                for gloss in glosses:
                    headword = gloss_sub("\\textsc{", "}", gloss)
                    headword = re.sub(r'=and', '', headword)
                    headword = re.sub(r'=be', '', headword)
                    headword = re.sub(r'-|\.', '', headword)
                    headwords.append(headword)
                # for i in range(len(glosses)):
                #     if glosses[i-1].endswith("\\textsc{"):
                #         glosses[i-1] = glosses[i-1][:-8]
                #     if glosses[i-1].endswith("\\textsc{"):
                #         glosses[i-1] = glosses[i-1][:-8]
                spacebool = False
            elif "glt" in line:
                trans = re.sub(r"\\glt ", "", line)
                # print(trans)
                for i in range(len(words)):
                    gloss = re.sub(r"\\\\", r"\\", glosses[i-1])
                    word = "\\textit{" + words[i-1] + "} " + "[" + gloss + "]"
                    hword = headwords[i-1]
                    # print(hword, word)
                    try:
                        if hword not in dicText:
                            dicText[hword] = {word: ["(" + label[:2] + "." + "\\ref{" + label + "})"]}
                        elif word not in dicText[hword]:
                            dicText[hword][word] = ["(" + label[:2] + "." + "\\ref{" + label + "})"]
                        else:
                            dicText[hword][word].append("(" + label[:2] + "." + "\\ref{" + label + "})")
                    except:
                        pass
    dicText = dict(sorted(dicText.items()))
    for key, items in dicText.items():
        eee = create_entry(random.choice(list(items.keys())))
        eee = gloss_strip("\\textit{", "}" ,eee)
        ipa = ipa_con(eee)
        entry = "\\entry{" + eee + "}{[\\textipa{"+ipa+"}]: " + key +"}{PoS}{" 
        for key2, item in items.items():
            entry += key2 + ": " 
            i = random.choice(item)
            entry += i + "; "
        entry = entry[:-2] + "}\n\n"
        # print(entry)
        txtfile.write(entry)
        # print(dicText)
    # key = gloss; items = 
    # for key, items in dicText.items():
    #     print(key, items)
    #     itete = json.loads(items)
    #     # morph_gloss = Lepzig
    #     morph_gloss = gloss_strip("textsc{", "}", key)
    #     if morph_gloss not in scList:
    #         scList.append(morph_gloss)
    #     # dic_entry = headword
    #     dic_entry = gloss_sub("\\textsc{", "}", key)
    #     dic_entry = re.sub('=and', '', dic_entry)
    #     dic_entry = re.sub('=be', '', dic_entry)
    #     if dic_entry not in dicRefin.keys():
    #         key2, tags = dicText[key].items()
    #         dicRefin[dic_entry] = {"\textit{"+key+"}": tags}
    #     print(dic_entry, dicRefin[dic_entry])
    #     print(key, dicText[key])
    # print(dicRefin.keys())








    #     for l in defList:
    #         ent = ""
    #         for key1, items1 in dicText.items():
    #             # if re.match(l, key1):
    #             if re.search(r"(?<![a-z])" + l + r"(?![a-z])", key1):
    #             # if l in key1:
    #                 try:
    #                     for key2, items2 in items1.items():
    #                         # keyClean = re.sub("}.", ".", key1)
    #                         test = [*key1]
    #                         # print(test)
    #                         if test.count("}") > test.count("{"):
    #                             key1 = key1[:-1]
    #                             # print(key1)
    #                         
    #                         ent += "\\textit{" + key2 + "} [" + key1 + "] "
    #                         # Add code that selects randomly
    #                         ent += items2[0] +"; "
    #                         dicRefin[l] = ent
    #                         # print(dicRefin[l])
    #                 except:
    #                     pass
                    # print(ent)
#         print(dicRefin)
# print(dicRefin.keys())

    # for key, items in dicRefin.items():
    #     entry = "\entry{}{[\\textipa{}]: " + key +"}{PoS}{" + items[:-2] + "}\n\n"
    #     # for key2, items2 in items.items():
    #     #     entry += key2 + " "
    #     #     for i in items2:
    #     #         entry += "\\r" + i.strip() + ", "
    #     #     entry = entry[:-2] 
    #     # print(entry)
    #     txtfile.write(entry)