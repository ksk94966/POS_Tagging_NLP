import sys
import re

if __name__== "__main__":

    path = sys.argv[1]    #for getting filename as argument
    f = open(path,"r")
    #in_sent = sys.argv[2]

    #splitting sentence from the given data text file by stripping the trailing spaces

    corpus_Sentences = f.read().strip().split("\n")   

    dict_tagTags = {};                  #to store (word,tag) combinations and respective counts
    dict_wordTags = {};                 #to store (tag,tag) combinations and respective counts
    tags_all = []                       #to store all tags including special tags

    for sent in corpus_Sentences:
        temp_tag_list = []                                           #Created a temporary list for storing that particular sentence tags
        token_sent = sent.strip().split(" ")
        fchar = '<s>'                                               
        ftag = token_sent[0].split("_")[1]
        tags_all.append(fchar)
        tags_all.append(ftag)
        if (ftag,fchar) not in dict_tagTags:                        #Adding (firsttag,<s>)  combination
            dict_tagTags[(ftag,fchar)] = 1
        else:
            dict_tagTags[(ftag,fchar)] += 1
        lchar = '</s>'
        ltag = token_sent[len(token_sent)-1].split("_")[1]
        tags_all.append(lchar)
        if (lchar,ltag) not in dict_tagTags:
            dict_tagTags[(lchar,ltag)] = 1                          #Adding (</s>,lasttag)  combination
        else:
            dict_tagTags[(lchar,ltag)] += 1
        for x in token_sent:
            (word,tag) = x.split("_")
            temp_tag_list.append(tag)
            if (word,tag) not in dict_wordTags:
                dict_wordTags[(word,tag)] = 1                       #Generating Bigrams of word-tag combination and its respective counts
            else:
                dict_wordTags[(word,tag)] += 1
        for y in range(1,len(temp_tag_list)):
            tag1 = temp_tag_list[y-1]
            tag2 = temp_tag_list[y]                             
            tags_all.append(tag2)
            if (tag2,tag1) not in dict_tagTags:                 #Generating Bigrams of tag-tag combination and its respective counts
                dict_tagTags[(tag2,tag1)] = 1
            else:
                dict_tagTags[(tag2,tag1)] += 1

    dict_tags = {};

    print(len(tags_all))
    for t in tags_all:
        if t not in dict_tags:
            dict_tags[t] = 1                                    #Generating unigrams of tag and its respective counts 
        else:
            dict_tags[t] += 1


    print(dict_tags['VBZ'])
    print(dict_tags['DT'])



    #Calculating the probabilities


    prob_wordTag = {}

    for i in dict_wordTags:
        prob_wordTag[i] =  dict_wordTags[i]/dict_tags[i[1]]

    
    prob_tagTag = {}

    for j in dict_tagTags:
        prob_tagTag[j] = dict_tagTags[j]/dict_tags[j[1]]

    print(prob_wordTag[('is','VBZ')])                       #testing the probabilities

    print(prob_tagTag[('NN','DT')])                         #testing the probabilities
    

        


            

    


                


