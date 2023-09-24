#This is algorithm for finding the solution of the coupled Riccation differential equations (cRDEs) for resucue mode
##we have 3 individual defenders, one attacker and one target
#Author- Aniruddha Roy, Department of Electrical Engineering, mail-ee18d031@smail.iitm.ac.in 
#
#
#importing important libraries
import numpy as np
#from numpy import linalg as LA 
#scientific python for maths
#solve_ivp uses 'RK45' method by default to solve the initial value problem
from scipy.integrate import solve_ivp

#functions and classes from other python programs
from symgen import symgen
from vectgen import vectgen
#from TADindRescue import Parameter #filename----class
from initData import InitialData

N=5 # no of players 
n=2*N #total state space dimension
nz=2*N-2 # state space dimension in the transformed coordinate

I2=np.identity(2)
I3=np.identity(3)

#Loading the Data of parameters and initial conditions(Creating an Object)
IC=InitialData()
#par=Parameter()
#give initial condition here
#Xinit=IC.Xinit[:,4]

#coupled RDE solving function 
def RDE_solver(t,y,par):
    dy=np.zeros(180)
    Pd1=symgen(y[0:36]);Pd2=symgen(y[36:72]);Pd3=symgen(y[72:108])
    Pt=symgen(y[108:144]);Pa=symgen(y[144:180])
    Acl=par.A-par.Sd1@Pd1-par.Sd2@Pd2-par.Sd3@Pd3-par.St@Pt-par.Sa@Pa
    dPd1=-Acl.T@Pd1-Pd1@Acl-par.Qd1-Pd1@par.Sd1@Pd1
    dPd2=-Acl.T@Pd2-Pd2@Acl-par.Qd2-Pd2@par.Sd2@Pd2
    dPd3=-Acl.T@Pd3-Pd3@Acl-par.Qd3-Pd3@par.Sd3@Pd3
    dPt=-Acl.T@Pt-Pt@Acl-par.Qt-Pt@par.St@Pt
    dPa=-Acl.T@Pa-Pa@Acl-par.Qa-Pa@par.Sa@Pa
    dy = np.r_[vectgen(dPd1),vectgen(dPd2),vectgen(dPd3),vectgen(dPt),vectgen(dPa)]
    
    return dy

def solution_rescue(par,T,delta):
    init = np.r_[vectgen(par.Fd1),vectgen(par.Fd2),vectgen(par.Fd3),vectgen(par.Ft),vectgen(par.Fa)] #initial values to run ode solvers 
    t_eval=np.arange(T,-delta,-delta)
    #Defining the Function using Lambda
    F = lambda t,y:RDE_solver(t,y,par) ## same as like matlab @function 
    #as final value is ignored in python, instead of zero, final value is -0.005
    sol=solve_ivp(F, [T,-delta],init, t_eval=t_eval)

    #don't use np.flip as it flips both row and column,
    # while matlab flip does only row by default
    time=np.flipud(sol.t)
    Gain=np.flipud(np.transpose(sol.y))

    #################
    ######placeholders#######
    Pd1 = np.zeros((len(time),nz,nz))
    Pd2 = np.zeros((len(time),nz,nz))
    Pd3 = np.zeros((len(time),nz,nz))
    Pt = np.zeros((len(time),nz,nz))
    Pa = np.zeros((len(time),nz,nz))
    Aclz = np.zeros((len(time),nz,nz))
    Aclx_sol = np.zeros((len(time),n,n))
    #################################
    for i in range(len(time)):
        Pd1[i]=symgen(Gain[i,0:36].T)
        Pd2[i]=symgen(Gain[i,36:72].T)
        Pd3[i]=symgen(Gain[i,72:108].T)
        Pt[i]=symgen(Gain[i,108:144].T)
        Pa[i]=symgen(Gain[i,144:180].T)
        Aclz[i]=par.A-par.Sd1@Pd1[i]-par.Sd2@Pd2[i]-par.Sd3@Pd3[i]-par.St@Pt[i]-par.Sa@Pa[i]
        Csup=np.array([[1,0,0,-1,0],[0,1,0,-1,0],[0,0,1,-1,0],[0,0,0,-1,1]])
        C = np.kron(Csup,I2)
        #ecah element of Aclx is 10x10 matrix
        Aclx_sol[i]= np.r_[-I2@np.linalg.inv(par.Rd1)@par.Bd1.T@Pd1[i]@C,-I2@np.linalg.inv(par.Rd2)@par.Bd2.T@Pd2[i]@C,-I2@np.linalg.inv(par.Rd3)@par.Bd3.T@Pd3[i]@C,-I2@np.linalg.inv(par.Rt)@par.Bt.T@Pt[i]@C,-I2*np.linalg.inv(par.Ra)@par.Ba.T@Pa[i]@C]
    return Aclx_sol





