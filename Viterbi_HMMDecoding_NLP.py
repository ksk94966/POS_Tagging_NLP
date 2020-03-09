import sys
import re

if __name__== "__main__":

    # path = sys.argv[1]    #for getting filename as argument
    # f = open(path,"r")

    input_sent = sys.argv[1]

    observations = input_sent.strip().split(" ")

    states = ['NNP','MD','VB','JJ','NN','RB','DT']

    start_prob = {'NNP':0.2767,'MD':0.0006,'VB':0.0031,'JJ':0.0453,'NN':0.0449,'RB':0.0510,'DT':0.2026}

    trans_prob = {}   #Storing the trasition probabilities                  
    trans_prob['NNP']=  {'NNP':0.3777,'MD':0.0110,'VB':0.0009,'JJ':0.0084,'NN':0.0584,'RB':0.0090,'DT':0.0025}
    trans_prob['MD']=   {'NNP':0.0008,'MD':0.0002,'VB':0.7968,'JJ':0.0005,'NN':0.0008,'RB':0.1698,'DT':0.0041}
    trans_prob['VB']=   {'NNP':0.0322,'MD':0.0005,'VB':0.0050,'JJ':0.0837,'NN':0.0615,'RB':0.0514,'DT':0.2231}
    trans_prob['JJ']=   {'NNP':0.0366,'MD':0.0004,'VB':0.0001,'JJ':0.0733,'NN':0.4509,'RB':0.0036,'DT':0.0036}
    trans_prob['NN']=   {'NNP':0.0096,'MD':0.0176,'VB':0.0014,'JJ':0.0086,'NN':0.1216,'RB':0.0177,'DT':0.0068}
    trans_prob['RB']=   {'NNP':0.0068,'MD':0.0102,'VB':0.1011,'JJ':0.1012,'NN':0.0120,'RB':0.0728,'DT':0.0479}
    trans_prob['DT']=   {'NNP':0.1147,'MD':0.0021,'VB':0.0002,'JJ':0.2157,'NN':0.4744,'RB':0.0102,'DT':0.0017}

    emission_prob = {}              #storing the emission probabilities

    emission_prob['NNP']={'Janet':0.000032,'will':0,'back':0,'the':0.000048,'bill':0}
    emission_prob['MD']={'Janet':0,'will':0.308431,'back':0,'the':0,'bill':0}
    emission_prob['VB']={'Janet':0,'will':0.000028,'back':0.000672,'the':0,'bill':0.000028}
    emission_prob['JJ']={'Janet':0,'will':0,'back':0.000340,'the':0,'bill':0}
    emission_prob['NN']={'Janet':0,'will':0.000200,'back':0.000223,'the':0,'bill':0.002337}
    emission_prob['RB']={'Janet':0,'will':0,'back':0.010446,'the':0,'bill':0}
    emission_prob['DT']={'Janet':0,'will':0,'back':0,'the':0.506099,'bill':0}


    final_tag =  {s:{} for s in states}

    best_tag = {}

    temp_tag = "rand1"
    temp_high = -1
    for s in states:                            #Storing the intial states and observations
        o = observations[0]
        temp_val = start_prob[s]*emission_prob[s][o]
        final_tag[s][(o,s)] = temp_val
        if temp_val>temp_high:
            o = list([s])
            best_tag[s] = o
    
    #print(final_tag)
    #print(best_tag)

    for o in range(1,len(observations)):                        #Calculating for each observation
        for s in range(0,len(states)):
            st = states[s]
            ob = observations[o]
            maxprob_val = -1000
            temp_tag = "rand"
            for x in range(0,len(states)):
                prev_obs = observations[o-1]      
                temp = final_tag[states[x]][(prev_obs,states[x])]   
                cal = temp* trans_prob[states[x]][st]
                if cal>maxprob_val:
                    maxprob_val = cal
                    temp_tag = states[x]
            best_tag[st].append(temp_tag)                       #Backpointer - here kept track of the state
            final_tag[st][(ob,st)] = emission_prob[st][ob]*maxprob_val          

    #print(final_tag)
    #print(best_tag)

    tag_assign = {}

    x = observations[len(observations)-1]
    max_tag_value = -2000
    tag = 0
    for y in final_tag:                         #Selecting the best tag based on the maximum probability among the generated
        for z in final_tag[y]:
            #print(z)
            if(z[0]==x):
                if max_tag_value<final_tag[y][z]:
                    max_tag_value = final_tag[y][z]
                    #print(z[1])
                    tag = z[1]
    best_tag['final'] = dict() 
    best_tag['final'][len(observations)] = (tag,max_tag_value)
    
    start = 'final'
    
    final_tags_list = [best_tag['final'][len(observations)][0]]
    #print(best_tag[start])
    finaltag_prob = [best_tag['final'][len(observations)][1]]
    for i in range(len(observations),0,-1):   
        if i!=len(observations):
            #print(start)
            final_tags_list.append(start)
        #print(start)
        if i== len(observations):
            temp_s = best_tag[start][i][0]
        else :
            temp_s = best_tag[start][i]
        start = best_tag[temp_s][i-1]
        

    #Assigning tags to the sentence
    final_str = ""
    for i in range(len(final_tags_list)-1,-1,-1):
        tem = observations[len(observations)-i-1]
        #print(tem)
        final_str += tem+"_"+final_tags_list[i]+" "
    
    print("Input sentence after POS tagging\n",final_str)

    print("Probability of the seqeunce:\n",best_tag['final'][len(observations)][1])

