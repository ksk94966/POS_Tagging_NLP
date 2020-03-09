import sys
import re
import itertools

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

    #print(len(tags_all))
    for t in tags_all:
        if t not in dict_tags:
            dict_tags[t] = 1                                    #Generating unigrams of tag and its respective counts 
        else:
            dict_tags[t] += 1

    #print(dict_tags['VBZ'])
    #print(dict_tags['DT'])



    #Calculating the probabilities
    prob_wordTag = {}
    for i in dict_wordTags:
        prob_wordTag[i] =  dict_wordTags[i]/dict_tags[i[1]]

    prob_tagTag = {}
    for j in dict_tagTags:
        prob_tagTag[j] = dict_tagTags[j]/dict_tags[j[1]]

    #print(prob_wordTag[('is','VBZ')])                       #testing the probabilities
    #print(prob_tagTag[('NN','DT')])                         #testing the probabilities

    given_str = sys.argv[2];                                 #getting the input sentence

    #ls_str = re.split(r'[;,\s]\s*', given_str)
    ls_str = given_str.strip().split(" ");                #Storing the given string in a list

    givenstr_wordtag = {}
    for i in ls_str:
        ls = []
        for j in dict_wordTags:             #Finding all the possible tags for the given string 
            if(j[0]==i):
                ls.append(j[1])
        givenstr_wordtag[i] = ls

    #print(givenstr_wordtag)

    combi_list = []

    for i in givenstr_wordtag:                      #Storing dictionary values of lists to a single list
        combi_list.append(givenstr_wordtag[i])

    #print(combi_list)

    res = list(itertools.product(*combi_list)) #for generating all the combinations
    #print(res);

    prob_allcomb = {}             #dictionary for storing all combination probabilities            
    max_prob = 1;
    for i in res:
        max_product=1
        for y in range(0,len(i)):
            if (ls_str[y],i[y]) in prob_wordTag:
                max_product *= prob_wordTag[(ls_str[y],i[y])]   #generating product for word tag sequence
            else:
                max_product = 0
        for y in range(1,len(i)):
            if (i[y],i[y-1]) in prob_tagTag:                    #generating product for tag tag sequence
                max_product *= prob_tagTag[(i[y],i[y-1])]
            else:
                max_product = 0
        f_char = '<s>'
        l_char = '</s>'                                                         
        if (i[0],f_char) in prob_tagTag:
            max_product *= prob_tagTag[(i[0],f_char)]           #generating product for (first_tag,<s>)
        else:
            max_product = 0
        if (l_char,i[len(i)-1]) in prob_tagTag:
            max_product *= prob_tagTag[(l_char,i[len(i)-1])]    #generating product for (<s>,last_tag)
        else:
            max_product = 0
        #print(max_product)
        prob_allcomb[i] = max_product                           #Storing all the respective tag combination probablities
    
    #print(prob_allcomb)

    besttag_combination = max(prob_allcomb, key=prob_allcomb.get)  #Selecting the best probability tag


    fin_generated_string = ""                            #For storing the output

    for i in range(0,len(besttag_combination)):
        fin_generated_string += ls_str[i] + "_" + besttag_combination[i] + " ";

    print("Input sentence after POS tagging:\n",fin_generated_string)                     #printing the output

    print("Best tag combination is:",besttag_combination)
    print("Its probability is:",prob_allcomb[besttag_combination])
            

