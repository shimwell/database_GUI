
import shutil
import os
import re, sys
from nuc_data_lib import *

def make_dir(dir):
    try:
        os.mkdir(dir)
    except:
        pass

        
pwd=os.path.dirname(os.path.realpath(__file__))
print(pwd)

lib_dir='libraries'

#list_file = open('cross_section_database_exfor.txt','w')
#list_file_ajax = open('cross_section_database_exfor_ajax.txt','w')

 


particlem=0
particlec=0
table_dirs=[]
file_counter=0
for root, dirs, files in os.walk(lib_dir):
    
    for file in files:
            
        

        if len(root.split('/xs/'))==2:
        #if  root.split('/xs/'==:
            #print(os.path.split(root))
            #print(root.split('/')[-3])
            print(root)
            if 'exfor' == root.split('/')[-3]:
                #print(dirs)
                #print(root.split('/'))
                root_simple=root.replace('\\','/')
                root_chop_up=root_simple.split('/')
                #print(root_chop_up)
                #print(root+' ' + file)
                
                #print(root_chop_up)
                particle=root_chop_up[-5].lower()
                #print('particle',particle)
                MT_number_string=root_chop_up[-1]
                #print('mt number',MT_number_string)
                #sys.exit()

                if len(MT_number_string)>3:
                    #print(MT_number_string)
                    state = MT_number_string[-1]
                    MT_number_int=MT_number_string[:-1]
                    #print(MT_number_int)
                else:
                    MT_number_int=MT_number_string
                    state=''
                #print(state)
                    
                if mtlookup(particle,str(int(MT_number_string))) =='none found':
                
                    particlem=particlem+1
                else:
                    particlec=particlec+1
                    element_full=root_chop_up[-4]
                    element=re.split('(\d+)',element_full)[0].lower()
                    #print(re.split('(\d+)',element_full)[1])
                    atomic_number_string=re.split('(\d+)',element_full)[1].lower()
                    
                    

                    if len(re.split('(\d+)',element_full)) ==3:
                        atomic_number_string=re.split('(\d+)',element_full)[1]+re.split('(\d+)',element_full)[2]
                    if atomic_number_string.endswith('mm'):
                        atomic_number_string=atomic_number_string[:-1]
                    evaluation=root_chop_up[-3].lower()
                    
                    #experiment=file[:-4]
                    experiment=file.split('-')[3]+'-'+file.split('-')[4][:-5]+'-'+file.split('.')[-1]
                    print(experiment)
                    

                    
                    experiment=experiment.lower()
                    if atomic_number_string.startswith('000'):
                        pass
                    elif atomic_number_string.startswith('00'):
                        atomic_number_string=atomic_number_string[2:]
                    elif atomic_number_string.startswith('0'):
                        atomic_number_string=atomic_number_string[1:]
                    atomic_number_string=atomic_number_string.lower()
                        
                    if MT_number_string.startswith('0'):
                        MT_number_string=MT_number_string[1:]
                    if MT_number_string.startswith('0'):
                        MT_number_string=MT_number_string[1:]
                    MT_number_string=MT_number_string.lower()
                    #print(atomic_number_string)
                    
                    make_dir(pwd+'/xs')
                    make_dir(pwd+'/xs/'+particle)
                    make_dir(pwd+'/xs/'+particle+'/'+element)
                    make_dir(pwd+'/xs/'+particle+'/'+element+'/'+atomic_number_string)
                    make_dir(pwd+'/xs/'+particle+'/'+element+'/'+atomic_number_string+'/'+evaluation)
                    make_dir(pwd+'/xs/'+particle+'/'+element+'/'+atomic_number_string+'/'+evaluation+'/'+MT_number_string)

                    
                    
                    #elementfull=element_lookup(element)
                    print(pwd+'/xs/'+particle+'/'+element+'/'+atomic_number_string+'/'+evaluation+'/'+MT_number_string+'/'+experiment)
                    shutil.copy2(root+'/'+file,pwd+'/xs/'+particle+'/'+element+'/'+atomic_number_string+'/'+evaluation+'/'+MT_number_string+'/'+experiment)
                    

                    
                    

                    

print('missed particles ='+str(particlem))
print('caught particles ='+str(particlec))
            
        
print(file_counter)
#list_file_ajax.close()
#list_file_beta.close()