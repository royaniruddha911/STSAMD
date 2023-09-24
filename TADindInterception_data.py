## This is the function associated the problem Data in the interception mode. 
## we have 3 individual defenders, one attacker and one target
#Author- Aniruddha Roy, Department of Electrical Engineering, mail-ee18d031@smail.iitm.ac.in
#Step-1: We stored all the problem parameters data by defining a class Parameter.
#Inside the class Parameter, we introduce the variable lambda_var (line-53). This parametr is associated the Attacker 
#Step-2: We define a function TADindInterception(lamda_var).
# Based on the lamda_var (0 or 1), we will get the problem parameters when attacker is either suicidal or non-suicidal mode 
#
#
#import librarries
import numpy as np
from scipy.linalg import block_diag
Ap = np.zeros((2,2)) #null matrix with 2 by 2 diimension
I2=np.identity(2) #identity matrix with 2 by 2 dimension
I3=np.identity(3) #identity matrix with 3 by 3 dimension
n=3; #number of the defenders

#The following are the interaction parameters among the players in the interception mode 
fd1a=1;fd2a=1;fd3a=1; fta=1; 
fad1=1;fad2=1;fad3=1; fat=1;

#The following are the weight parameters of the weight matrix which is the penalty on the states 
qd1a=1;qd2a=1;qd3a=1; qta=1; 
qad1=1;qad2=1;qad3=1; qat=1;

#The following are the weight parameters of the weight matrix which is the penalty on the contros
rd1=1;rd2=1;rd3=1;rt=1.2;ra=0.8; 

### We created the class--named as--Parametr--where all the problem parameters is there 
class Parameter: 
    def __init__(self,lamda_var):
        #A,Bi matrices from the global state dynamics 
        self.Bd1= np.kron(np.r_[I3[:,0],[0]],I2).T # Bd1--input matrix of the defender-1
        self.Bd2= np.kron(np.r_[I3[:,1],[0]],I2).T # Bd2--input matrix of the defender-2
        self.Bd3= np.kron(np.r_[I3[:,2],[0]],I2).T # Bd2--input matrix of the defender-3
        self.Bt = np.kron(np.array([0,0,0,1]).T,I2).T  # Bt--input matrix of the target 
        self.Ba = np.kron(np.array([-1,-1,-1,-1]).T,I2).T #Ba-- input matrix of the atacker 
        self.A  = np.kron(np.zeros((4,4)),Ap) # A--is the system matrix of the global state dynamics
        #Individual Defenders weight matrices
        self.Fd1 = np.kron(block_diag(fd1a,0,0,0),I2) #terminal weight matrix- defender-1
        self.Fd2 = np.kron(block_diag(0,fd2a,0,0),I2) #terminal weight matrix- defender-2
        self.Fd3 = np.kron(block_diag(0,0,fd3a,0),I2) #terminal weight matrix- defender 3
        self.Qd1 = np.kron(block_diag(qd1a,0,0,0),I2) #weight matrix on the state-defender-1
        self.Qd2 = np.kron(block_diag(0,qd2a,0,0),I2) #weight matrix on the state-defender-2
        self.Qd3 = np.kron(block_diag(0,0,qd3a,0),I2) #weight matrix on the state-defender-3
        self.Rd1 = I2  #weight matrix on the control-defender-1
        self.Rd2 = I2  #weight matrix on the control-defender-2
        self.Rd3 = I2  #weight matrix on the control-defender-3
        #Target Weight Matrices
        self.Ft = block_diag(np.zeros((2*n,2*n)),-fta*I2) #terminal weight matrix-target
        self.Qt = block_diag(np.zeros((2*n,2*n)),-qta*I2) #weight matrix on the state-target
        self.Rt = I2 #weight matrix on the control-target
        #The following varibale value can be either 0 or 1. If it is 0--which means we consider the suicidl attacker and 1 means non-suicidal attacker
        self.lamda_var = lamda_var 
        #Attacker Weight Matrix
        self.Fa = np.kron(block_diag(-self.lamda_var*fad1,-self.lamda_var*fad2,-self.lamda_var*fad3,fat),I2) #terminal weight matrix-attacker 
        self.Qa = np.kron(block_diag(-self.lamda_var*qad1,-self.lamda_var*qad2,-self.lamda_var*qad3,qat),I2) #weight matrix on the control-attacker
        self.Ra = I2
        # Si- matrices Si=Bi*inverse(Ri)*transpose(Bi)
        self.Sd1 = np.matmul(np.matmul(self.Bd1,np.linalg.inv(self.Rd1)),self.Bd1.T) #defendr-1
        self.Sd2 = np.matmul(np.matmul(self.Bd2,np.linalg.inv(self.Rd2)),self.Bd2.T) #defendr-2
        self.Sd3 = np.matmul(np.matmul(self.Bd3,np.linalg.inv(self.Rd3)),self.Bd3.T) #defendr-3
        self.St  = np.matmul(np.matmul(self.Bt,np.linalg.inv(self.Rt)),self.Bt.T)    #target
        self.Sa  = np.matmul(np.matmul(self.Ba,np.linalg.inv(self.Ra)),self.Ba.T)    #attacker 
        
## The following function will call the class Parameter and which is function of the lambda variable, which takes 1 or 0
## This function provides all the problem parametr data for the interception mode 
def TADindInterception(lamda_var):
    par  = Parameter(lamda_var) # call the class- Parametr()
    return par
