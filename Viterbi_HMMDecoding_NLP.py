import sys
import re

if __name__== "__main__":

    #states = ['healthy','fever']

    states = ['NNP','MD','VB','JJ','NN','RB','DT']

    #observations = ['normal', 'cold' , 'dizzy']

    observations = ['Janet','will','back','the','bill']

    #start_prob = {'healthy': 0.6,'fever' : 0.4}

    start_prob = {'NNP':0.2767,'MD':0.0006,'VB':0.0031,'JJ':0.0453,'NN':0.0449,'RB':0.0510,'DT':0.2026}

    #trans_prob = { 'healthy' : {'healthy' : 0.7, 'fever' : 0.3},'fever':{'healthy':0.4,'fever':0.6}}

    trans_prob = {}
    trans_prob['NNP']=  {'NNP':0.3777,'MD':0.0110,'VB':0.0009,'JJ':0.0084,'NN':0.0584,'RB':0.0090,'DT':0.0025}
    trans_prob['MD']=   {'NNP':0.0008,'MD':0.0002,'VB':0.7968,'JJ':0.0005,'NN':0.0008,'RB':0.1698,'DT':0.0041}
    trans_prob['VB']=   {'NNP':0.0322,'MD':0.0005,'VB':0.0050,'JJ':0.0837,'NN':0.0615,'RB':0.0514,'DT':0.2231}
    trans_prob['JJ']=   {'NNP':0.0366,'MD':0.0004,'VB':0.0001,'JJ':0.0733,'NN':0.4509,'RB':0.0036,'DT':0.0036}
    trans_prob['NN']=   {'NNP':0.0096,'MD':0.0176,'VB':0.0014,'JJ':0.0086,'NN':0.1216,'RB':0.0177,'DT':0.0068}
    trans_prob['RB']=   {'NNP':0.0068,'MD':0.0102,'VB':0.1011,'JJ':0.1012,'NN':0.0120,'RB':0.0728,'DT':0.0479}
    trans_prob['DT']=   {'NNP':0.1147,'MD':0.0021,'VB':0.0002,'JJ':0.2157,'NN':0.4744,'RB':0.0102,'DT':0.0017}

    

    # emission_prob = {
    #     'healthy' : {'normal':0.5,'cold':0.4,'dizzy':0.1},
    #     'fever' : {'normal':0.1,'cold':0.3,'dizzy':0.6}
    # }

    emission_prob = {}

    emission_prob['NNP']={'Janet':0.000032,'will':0,'back':0,'the':0.000048,'bill':0}
    emission_prob['MD']={'Janet':0,'will':0.308431,'back':0,'the':0,'bill':0}
    emission_prob['VB']={'Janet':0,'will':0.000028,'back':0.000672,'the':0,'bill':0.000028}
    emission_prob['JJ']={'Janet':0,'will':0,'back':0.000340,'the':0,'bill':0}
    emission_prob['NN']={'Janet':0,'will':0.000200,'back':0.000223,'the':0,'bill':0.002337}
    emission_prob['RB']={'Janet':0,'will':0,'back':0.010446,'the':0,'bill':0}
    emission_prob['DT']={'Janet':0,'will':0,'back':0,'the':0.506099,'bill':0}


    final_tag =  {s:{} for s in states}


    for s in states:
        o = observations[0]
        final_tag[s][(o,s)] = start_prob[s]*emission_prob[s][o];

    #print(final_tag);


    for o in range(1,len(observations)):
        for s in range(0,len(states)):
            st = states[s]
            ob = observations[o]
            maxprob_val = 0
            for x in range(0,len(states)):
                prev_obs = observations[o-1]      
                temp = final_tag[states[x]][(prev_obs,states[x])]   
                cal = temp* trans_prob[states[x]][st]
                maxprob_val = max(cal,maxprob_val)
            final_tag[st][(ob,st)] = emission_prob[st][ob]*maxprob_val


    print(final_tag)
    
    tag_assign = {}

    for x in observations:
        max_tag_value = -1
        tag = 0
        for y in final_tag:
            for z in final_tag[y]:
                #print(z)
                if(z[0]==x):
                    if max_tag_value<final_tag[y][z]:
                        max_tag_value = final_tag[y][z]
                        #print(z[1])
                        tag = z[1]
        tag_assign[x] = tag


    print(tag_assign)










