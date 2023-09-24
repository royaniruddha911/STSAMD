##This is algorithm for the Recedinig Horizon implementation  
##we have 3 individual defenders, one attacker and one target
#Author- Aniruddha Roy, Department of Electrical Engineering, mail-ee18d031@smail.iitm.ac.in 
#
#
#import the libraries 
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.linalg import expm,norm
from initData import InitialData
from RHdata import RHdata
IC=InitialData() #initial data 
T =1 # time horizon of the game 
delta = 0.005 # sampling value to discretize the time horizon
senseflag = 1 # 1 meane sense and communication , 0 means sense only 

[R,cR,Int] = RHdata(T,delta,1) #call the RH date function

Interception = Int
kappa = 6
radius = dict({'a':0.1,'d1':0.1,'d2':0.1,'d3':0.1}) #capture radius of the players
RH =30
RHsteps =50
terminalflag =0
xcnt =0                     #0 instead of 1 as in matlab
Time=np.arange(T,-delta,-delta)

##########################################################################################
# field names 
fields = ['x--Defender1','y--Defender1','x--Defender2','y--Defender2','x--Defender3','y--Defender3','x--Target','y--Target','x--Attacker','y--Attacker']      
file1 = "TrajectoryData.csv" # name of csv file which stores the trejectory data
# writing to csv file 
file = open("Output",'w')  #opening a file 
#############################################################################################

if senseflag == 0:#only sense
    Rescue = R
    print("Game in Sense only mode")
    file.write("\nGame in Sense only mode\n\n")
else : 
    Rescue = cR #sense and communication
    print("Game in Sense and comuunication mode")
    file.write("\nGame in Sense and communication mode\n\n")

class termination:
    def __init__(self):
        self.termflag = 0
        self.player = 5
        self.xdata = np.empty(shape=(1,len(Time)-1),dtype =float)
        self.ydata = np.empty(shape=(1,len(Time)-1),dtype =float)



x= np.empty(shape=(10,1), dtype=float) ###
x[:,0] = IC.Xinit[:,9] #initial condition

xfin = x[:,0]
cmode = np.empty(shape=RHsteps+1,dtype = int)
## function for determine the mode of the game at initial time 
def findmode(x,kappa,radius):
    dist = norm(x[8:10]-x[6:8])-kappa*radius['a'] #condition for determine the mode the game at intiallly
    if dist>0:
        mode = 0   #Rescue mode 
    else :
        mode = 1   #Interception mode 
    return mode 
#################### function for determine game termination condition###############################
def gmterm(x,radius,mode):
    termdata = termination()
    if mode >0 :
        dist1 = norm(x[8:10]-x[0:2]) #distance betwwen attacker and defender-1
        dist2 = norm(x[8:10]-x[2:4]) #distance betwwen attacker and defender-2
        dist3 = norm(x[8:10]-x[4:6]) #distance betwwen attacker and defender-3
        dista = norm(x[8:10]-x[6:8]) #distance betwwen attacker and target

        if (dist1<radius['d1']) or (dist2<radius['d2']) or (dist3<radius['d3']) : #distence condition 
            termdata.termflag = 1     #intercept
            a=[dist1-radius['d1'],dist2-radius['d2'],dist3-radius['d3']]
            termdata.player = a.index(min(a))
            termdata.xdata = x[2*termdata.player]
            termdata.ydata = x[2*termdata.player+1]
        elif(dista<radius['a']):
            termdata.termflag = 2   #capture  
            termdata.player = 4
            termdata.xdata = x[2*termdata.player]
            termdata.ydata = x[2*termdata.player+1]
        else :
            termdata.termflag =0     #no outcome
    else :
        dist1 = norm(x[0:2]-x[6:8]) #distance betwwen defender-1 and target 
        dist2 = norm(x[2:4]-x[6:8]) #distance betwwen defender-2 and target
        dist3 = norm(x[4:6]-x[6:8]) #distance betwwen defender-3 and target
        dista = norm(x[8:10]-x[6:8]) #distance betwwen attacker and target

        if (dist1<radius['d1']) and (dist2<radius['d2']) and (dist3<radius['d3']) : #distance condition
            termdata.termflag = 3   #rescue
            a=[dist1-radius['d1'],dist2-radius['d2'],dist3-radius['d3']]
            termdata.player = a.index(min(a))
            termdata.xdata = x[2*termdata.player]
            termdata.ydata = x[2*termdata.player+1]
        elif(dista<radius['a']):
            termdata.termflag = 4    #capture
            termdata.player = 4
            termdata.xdata = x[2*termdata.player]
            termdata.ydata = x[2*termdata.player+1]
        else :
            termdata.termflag =0    # no outcome
    return termdata

def findmode1(x):
    d1 =  norm(x[6:8]-x[0:2]) #distance between target and defender-1 
    d2 =  norm(x[6:8]-x[2:4]) #distance between target and defender-2 
    d3 =  norm(x[6:8]-x[4:6]) #distance between target and defender-3
    da =  norm(x[6:8]-x[8:10]) #distance between target and atatcker 
    trigger = 1
    if da/min([d1,d2,d3])/da>trigger :               
        mode =1 
    else :
        mode = 0
    return mode

################file starting and writing the conditions required##################
file.write("The starting intial condition is \n")                
file.write(np.array_str(xfin)) #will write in the text file

for k in range(1,RHsteps+1):                            
    aclcnt =0                                #aclcnt starts from 0
    mode = findmode(xfin,kappa,radius) #calling the find mode function
    cmode[k] = mode
######### game starting mode################################
    if k == 1 :                                    
        if cmode[k] == 0:
            print("Game starts in the Rescue mode ")
            file.write("\n Game starts in the Rescue mode\n")
        else:
            print("Game starts in the Interception mode")
            file.write("\n Game starts in the Interception mode\n")
#################game switching mode#######################################
    if k > 1 :
        if abs(cmode[k]-cmode[k-1])>0:
            if cmode[k] == 1:
                print("Game switches to Interception mode at {}".format((k-1)*delta*RH))
                file.write("Game switches to Rescue mode at {}\n\n".format((k-1)*delta*RH)) 
            else :
                print("Game switches to Rescue mode at {}".format((k-1)*delta*RH))   
                file.write("Game switches to Rescue mode at {}\n\n".format((k-1)*delta*RH)) 
   
###Receding horion mode implementation##################################      
     
    for i in np.arange(((k-1)*RH+1)*delta,(k*RH+1)*delta,delta):       
        if mode >0:
            Acl = Interception #Interception mode data 
            d=expm(Acl[aclcnt]*delta)@x[:,xcnt] #computes the matrix exponential of the closed loop matrix
            d=d.reshape(-1,1)
            x=np.append(x,d,axis=1) ##
            #x[:,xcnt+1] = expm(Acl[aclcnt]*delta)@x[:,xcnt]
            xcnt+=1
            aclcnt+=1
            termdata = gmterm(x[:,xcnt],radius,mode) #calling the game termination function 
            if termdata.termflag != 0:
                terminalflag =1
                break
        else:
            Acl = Rescue #Rescue mode data
            e=expm(Acl[aclcnt]*delta)@x[:,xcnt] #computes the matrix exponential of the closed loop matrix
            e=e.reshape(-1,1)
            x=np.append(x,e,axis=1)
            #x[:,xcnt+1] = expm(Acl[aclcnt]*delta)@x[:,xcnt] 
            xcnt+=1
            aclcnt+=1
            termdata = gmterm(x[:,xcnt],radius,mode) #calling the game termination function 
            if termdata.termflag != 0:
                terminalflag =1
                break
 ####game termination output 
    if terminalflag == 1:
        if termdata.termflag ==4 or termdata.termflag ==2:
            print("\n Game terminates at {} with attacker capturing the target".format((xcnt+1)*delta))
            file.write("\n Game terminates at {} with attacker capturing the target".format((xcnt+1)*delta))
            file.write("\n Trajectories of the agents are written in the .csv file TrajectoryData.csv")
        elif termdata.termflag ==1 :
            print('\n Game terminates at {} with defender {} intercepting the attacker '.format((xcnt+1)*delta,termdata.player+1))
            file.write('\n Game terminates at {} with defender {} intercepting the attacker'.format((xcnt+1)*delta,termdata.player+1))
            file.write("\n Trajectories of the agents are written in the .csv file TrajectoryData.csv")
        elif termdata.termflag ==3 :
            print('\n Game terminates at {} with defender {} rescuing the target '.format((xcnt+1)*delta, termdata.player+1) )
            file.write('\n Game terminates at {} with defender {} rescuing the target'.format((xcnt+1)*delta, termdata.player+1) )
            file.write("\n Trajectories of the agents are written in the .csv file TrajectoryData.csv")
        elif termdata.termflag ==0 :
            print('\n Game has no outcome ')
            file.write('\n Game has no outcome')
            file.write("\n Trajectories of the agents are written in the .csv file TrajectoryData.csv")
        break

    xfin = x[:,xcnt]
    wnd = np.arange((k-1)*RH,(k)*RH)
    if termdata.termflag!=0:
        wnd  = np.arange((k-1)*RH,xcnt)
    with open(file1, 'w') as csvfile: #csv file data 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) #header name
        #csvwriter.writerows(rows) #rows name for each player
        csvwriter.writerows(x.T) #state data in each row 
    plt.subplot(1,2,1)
    plt.plot(x[0,wnd],x[1,wnd],'b',x[2,wnd],x[3,wnd],'b',x[4,wnd],x[5,wnd],'b',x[6,wnd],x[7,wnd],'k',x[8,wnd],x[9,wnd],'r')
    plt.show
    file.close  #file closing 
    
# lebelling all the players 
l=0.001
plt.text(x[0,0]+l,x[1,0]+l,'$d_{1}$',None,fontsize = 14) #defender-1
plt.text(x[2,0]+l,x[3,0]+l,'$d_{2}$',None,fontsize = 14) #defender-2
plt.text(x[4,0]+l,x[5,0]+l,'$d_{3}$',None,fontsize = 14) #defender-3
plt.text(x[6,0]+l,x[7,0]+l,r'$\tau$',None,fontsize = 14) # target 
plt.text(x[8,0]+l,x[9,0]+l,'a',None,fontsize = 14) #attacker 
Intercepting_Circle=plt.Circle((termdata.xdata,termdata.ydata),radius['d1'],fill = False,color='black') 
#figure, axes = plt.subplots() 
#axes.add_patch(Intercepting_Circle )
#plotting the capture radius 
plt.gca().add_patch(Intercepting_Circle) 
plt.subplot(1,2,2)

vect  = x[8:10,:]-x[6:8,:]
vect1 = np.sqrt(np.sum(vect*vect,axis =0))

tval = delta*np.arange(1,len(vect[0])+1,1)
plt.plot(tval,vect1)
plt.plot(tval,kappa*radius['a']*np.ones(len(tval)))
plt.xlim([0,max(tval)*1.1])
plt.ylim([0,max(vect1)*1.1])
plt.text(0.05,1.1*kappa*radius['a'],r'$\kappa a$',fontsize = 14)
plt.text(0.05,max(vect1),r'$||X_{a}-X_{\tau}||$',fontsize =14)
yln = np.linspace(0,5,100)
for k in range(1,21):
    plt.plot(k*RH*delta*np.ones(len(yln)),yln,linestyle='dashed',color='gray')


