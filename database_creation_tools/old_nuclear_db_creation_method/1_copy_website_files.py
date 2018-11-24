#still to address MT101g and MT101m
# refered to as states
import shutil
import os
import re
import time
from nuc_data_lib import *
import numpy as np

def make_dir(dir):
    try:
        os.mkdir(dir)
    except:
        pass




particlem=0
particlec=0

pwd=os.path.dirname(os.path.realpath(__file__))
print(pwd)


lib_dir='libraries/n'


#evaluation_list=['cendl3.1','eaf.2010','endfb7.1','irdff1.0','jeff3.2','jendl.2007.he','jendl4.0','jendl.4.0.he','tendl.2017']

#evaluation_list=['tendl.2017', 'jendl.2016', 'endfb8.0', 'kaeri', 'iaea', 'bofod', 'lanl', 'jeff3.3', 'jendl4.0.he', 'jendl.2007.he', 'jendl4.0', 'cendl3.1', 'irdff1.0', 'eaf.2010', 'ibandl', 'jendl.2005']
evaluation_list=['jeff3.3','endfb8.0']

dir_unique = []
for root, dirs, files in os.walk(lib_dir):
    for dir in dirs:
        if dir =='xs' :
            potential_lib = root.split('/')[-2]
            #print(potential_lib)
            if potential_lib not in dir_unique and potential_lib[0].isupper()==False:
                print(root,potential_lib)
                dir_unique.append(potential_lib)
evaluation_list=dir_unique
print('evaluation_list',evaluation_list)
  
    
table_dirs=[]
file_counter=0
for root, dirs, files in os.walk(lib_dir):
    for dir in dirs:

        if dir == 'xs':

            #print(str(folder_counter)+' table dirs found')
            print(root)
            #table_dirs.append(os.path.join(root,dir))

            for file in os.listdir(root+'/xs/'):
                if file!='mtlist' and file.endswith('.eps')==False:

                    chopup=file.lower().split('-')
                    if len(chopup)==3:
                        #print(file)
                        atomic_number_list=re.split('(\d+)',chopup[1])

                        #atomic_number_string=chopup[1][-3:]
                        atomic_number_string=atomic_number_list[1]+atomic_number_list[2]

                        if atomic_number_string.startswith('000'):
                            pass
                        elif atomic_number_string.startswith('00'):
                            atomic_number_string=atomic_number_string[2:]
                        elif atomic_number_string.startswith('0'):
                            atomic_number_string=atomic_number_string[1:]

                        #print(atomic_number_string)

                        particle=chopup[0]
                        element=atomic_number_list[0]

                        MT_number_string = chopup[2].split('.')[0][2:]

                        if len(MT_number_string)>3:
                            #print(MT_number_string)
                            state = MT_number_string[-1]
                            MT_number_int=MT_number_string[:-1]
                            #print(MT_number_int)
                            #print(state)
                        else:
                            MT_number_int=MT_number_string
                            state=''

                        if MT_number_string.startswith('0'):
                            MT_number_string=MT_number_string[1:]
                        if MT_number_string.startswith('0'):
                            MT_number_string=MT_number_string[1:]

                        try:
                            evaluation = root.split(os.path.sep)[-2]
                            #print(evaluation)
                            #evaluation = file.split('.')[1] + '.'+file.split('.')[2]
                        except:
                            print(root.split(os.path.sep))
                            print('evaluation not found')
                            input()

                        #if evaluation in evaluation_list and MT_number_string in list_of_MT_numbers and ((element+atomic_number_string) in list_of_isotopes or atomic_number_string=='000'):
                        if evaluation in evaluation_list :
                            file_counter=file_counter+1
                            #print(particle +' ' + element+' ' +atomic_number_string +' '+evaluation +' '+MT_number_string)

                            try:
                                energy,xs, =np.genfromtxt(fname=os.path.join(root,'xs', file), usecols = (0, 1) ,unpack=True,comments='#')
                                if os.path.isdir(os.path.join(pwd,'xs',particle,element,atomic_number_string,evaluation) == false:
                                    os.makedirs(os.path.join(pwd,'xs',particle,element,atomic_number_string,evaluation)
                                #make_dir(os.path.join(pwd,'xs'))
                                #make_dir(pwd+'/xs/'+particle)
                                #make_dir(pwd+'/xs/'+particle+'/'+element)
                                #make_dir(pwd+'/xs/'+particle+'/'+element+'/'+atomic_number_string)
                                #make_dir(pwd+'/xs/'+particle+'/'+element+'/'+atomic_number_string+'/'+evaluation)
                                shutil.copy2(os.path.join(root,'xs',file),os.path.join(pwd,'xs',particle,element,atomic_number_string,evaluation,MT_number_string))
                            except:
                                pass


                            elementfull=element_lookup(element)

                            #"08-27-2015 07:25:00AM".match(/[a-zA-Z]+|[0-9]+/g)

                            #list_file.write(particle_short+element+atomic_number_string+evaluation_short+str(int(MT_number_string))+"','")
                            if atomic_number_string =='000':
                                atomic_number='Natural'
                            else:
                                if atomic_number_string.startswith('00'): 
                                    atomic_number=atomic_number_string[2:]
                                elif atomic_number_string.startswith('0'): 
                                    atomic_number=atomic_number_string[1:]
                                else:
                                    atomic_number=atomic_number_string

                            evaluations = evaluation.upper()

                            if mtlookup(particle,str(MT_number_string)) == 'none found':

                                particlem = particlem + 1
                            else:

                                particlec = particlec + 1

                        else:
                            particlem = particlem + 1



print('missed particles ='+str(particlem))
print('caught particles ='+str(particlec))
print(file_counter)
