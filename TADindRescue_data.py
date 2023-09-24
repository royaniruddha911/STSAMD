## This is the function associated the problem Data in the Rescue mode. 
## we have 3 individual defenders, one attacker and one target
#Author- Aniruddha Roy, Department of Electrical Engineering, mail-ee18d031@smail.iitm.ac.in
#Step-1: We stored all the problem parameters data by defining a class Parameter.
#Inside the class Parameter, we introduce the variable mu. (line-56)
#Step-2: We define a function TADindRescue(mu).
# Based on mu (0 or 1), we will get the problem parameters 
#
#
#import python librarries 
import numpy as np
from scipy.linalg import block_diag
Ap = np.zeros((2,2)) #null matrix with 2 by 2 dimension
I2=np.identity(2) #identity matrix with 2 bt 2 dimension
I3=np.identity(3) #identity matrix with 3 by 3 dimension
n=3;#number of defenders


#The following are the interaction parameters among the players in the Rescue mode 
fd1t=1;fd2t=1;fd3t=1; fta=1;#interaction parameters
ftd1=1;ftd2=1;ftd3=1; fat=1;
fad1=1;fad2=1;fad3=1;
fd1a=1;fd2a=1;fd3a=1;

#The following are the weight parameters of the weight matrix which is the penalty on the states 
qd1t=1;qd2t=1;qd3t=1; qta=1; #weight parameters on state 
qad1=1;qad2=1;qad3=1; qat=1;
qd1a=1;qd2a=1;qd3a=1;

#The following are the weight parameters of the weight matrix which is the penalty on the contros
rd1=1;rd2=1;rd3=1;rt=1.25;ra=0.75; #control parameters

#mu=1;
lambdavar=0; #Rescue mode attacker is suicidal

### We created the class--named as--Parametr--where all the problem parameters is there 

class Parameter():
    def __init__(self,mu):
        #A,Bi matrices from the global state dynamics 
        self.Bd1= np.kron(np.r_[I3[:,0],[0]],I2).T # Bd1--input matrix of the defender-1
        self.Bd2= np.kron(np.r_[I3[:,1],[0]],I2).T # Bd2--input matrix of the defender-2
        self.Bd3= np.kron(np.r_[I3[:,2],[0]],I2).T # Bd2--input matrix of the defender-3
        self.Bt = np.kron(np.array([-1,-1,-1,-1]).T,I2).T  #Bt-- input matrix of the atacker
        self.Ba = np.kron(np.array([0,0,0,1]).T,I2).T #Ba-- input matrix of the atacker 
        self.A  = np.kron(np.zeros((4,4)),Ap) # A--is the system matrix of the global state dynamics
        #Individual Defenders weight matrices
        self.Fd1 = np.kron(block_diag(fd1t,0,0,0),I2) #terminal weight matrix- defender-1
        self.Fd2 = np.kron(block_diag(0,fd2t,0,0),I2) #terminal weight matrix- defender-2
        self.Fd3 = np.kron(block_diag(0,0,fd3t,0),I2) #terminal weight matrix3 defender-3
        self.Qd1 = np.kron(block_diag(qd1t,0,0,0),I2) #weight matrix on the state-defender-1
        self.Qd2 = np.kron(block_diag(0,qd2t,0,0),I2) #weight matrix on the state-defender-2
        self.Qd3 = np.kron(block_diag(0,0,qd3t,0),I2) #weight matrix on the state-defender-3
        self.Rd1 = I2 #weight matrix on the control-defender-1
        self.Rd2 = I2 #weight matrix on the control-defender-2
        self.Rd3 = I2 #weight matrix on the control-defender-3
        #mu
        self.mu = mu
        #Target Weight Matrices
        self.Ft = np.kron(block_diag(self.mu*fd1t,self.mu*fd2t,self.mu*fd3t,-fat),I2) #terminal weight matrix-target
        self.Qt = np.kron(block_diag(self.mu*qd1t,self.mu*qd2t,self.mu*qd3t,-qat),I2) #weight matrix on the state-target
        self.Rt = I2
        #Attacker Weight Matrix
          
        #terminal weight matrix-attacker 
        self.Fa = np.kron([[-lambdavar*fad1,0,0,lambdavar*fad1],[0,-lambdavar*fad2,0,lambdavar*fad2],[0,0,-lambdavar*fad3,lambdavar*fad3],[lambdavar*fad1, lambdavar*fad2,lambdavar*fad3, fat-lambdavar*fad1-lambdavar*fad2-lambdavar*fad3]],I2)
        #weight matrix on the control-attacker
        self.Qa=np.kron([[-lambdavar*qad1,0,0,lambdavar*qad1],[0,-lambdavar*qad2,0,lambdavar*qad2],[0,0,-lambdavar*qad3,lambdavar*qad3],[lambdavar*qad1, lambdavar*qad2,lambdavar*qad3, qat-lambdavar*qad1-lambdavar*qad2-lambdavar*qad3]],I2)
        self.Ra = I2
        # Si- matrices  # Si- matrices Si=Bi*inverse(Ri)*transpose(Bi)
        self.Sd1 = self.Bd1@np.linalg.inv(self.Rd1)@(self.Bd1.T) #defendr-1
        self.Sd2 = self.Bd2@np.linalg.inv(self.Rd2)@(self.Bd2.T) #defendr-2
        self.Sd3 = self.Bd3@np.linalg.inv(self.Rd3)@(self.Bd3.T) #defendr-3
        self.St  = self.Bt@np.linalg.inv(self.Rt)@(self.Bt.T)  #target
        self.Sa  = self.Ba@np.linalg.inv(self.Ra)@(self.Ba.T) #attacker

## The following function will call the class Parameter and which is function of the mu variable, which takes 1 or 0
## This function provides all the problem parametr data for the Rescue mode 
def TADindRescue(mu):
    par = Parameter(mu) # call the class- Parametr()
    return par
