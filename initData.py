##This files store all the 
# Using class InitialData we store , 12 initial conditions
#Author- Aniruddha Roy, Department of Electrical Engineering, mail-ee18d031@smail.iitm.ac.in
#
#
#import nmerical python library
import numpy as np
class InitialData: # stored initial data-name InitilaData
    def __init__(self):
        self.Xinit = np.empty(shape=(12,10), dtype=float)
        #par.iXd1=[0;0];iXd2=[1;1.5];iXd3=[-1;0]; iXt=[0;1];iXa=[-2;2]
        self.Xinit[0] = np.array([0,0,1,1.5,-1,0,0,1,-2,2]) #initial condition1 
        self.Xinit[1] = np.array([0,0,1,1.5,1,0,0.6,1,-2,2])  #initial condition2
        self.Xinit[2] = np.array([0,0,-1,1.5,-1,0,0.5,1,1,-1]) ##initial condition3
        self.Xinit[3] = np.array([-1,0.5,1,1.5,-1,1,0.6,1,-1,2]) #initial condition4
        self.Xinit[4] = np.array([0,0,0.8,1.5,-1,0,1,1,-2,2]) #initial condition 5
        self.Xinit[5] = np.array([-1,1,1,1,-1,0,-0.6,1,-2,2]) #initial condition6
        self.Xinit[6] = np.array([0,0,0.8,1.5,-1,0,-2,1,-1,2]) #initial condition7
        self.Xinit[7] = np.array([-1,1,1,1,-1,0,0,1,1,1.5]) #initial condition8
        self.Xinit[8] = np.array([1.8123,1.5455,0.0516,1.3975,0.2481,2.5163,0.9674,2.6360,0.5749,1.5894]) #initial condition9
        self.Xinit[9] = np.array([0.3831,1.2748,1.6011,1.0923,2.7298,0.3914,0.2629,-0.7499,1.9105,1.8671]) #initial conditio10
        self.Xinit[10] = np.array([1.2458,1.0700,0.3914,-0.2226,1.3165,-0.3429,-0.0322,2.3312,0.5811,0.8597]) #initial condition11
        self.Xinit[11] = np.array([2.9085,1.1222,2.0470,0.7731,0.8375,1.6901,1.5558,-0.1203,-0.5327,-0.0979]) #initial condition12
        self.Xinit = self.Xinit.T #make it transpose, bacasue date store in row wise 
