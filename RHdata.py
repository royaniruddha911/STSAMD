##The following function RHdata(), will give the problem data for the interception mode and rescue mode
##we have 3 individual defenders, one attacker and one target
#Author- Aniruddha Roy, Department of Electrical Engineering, mail-ee18d031@smail.iitm.ac.in
#
#
## From the file name TADindRescue_fn, we import the function for rescue mode problem data
from TADindRescue_data import TADindRescue
## From the file name TAdindInterception_fn, we import the function for interception mode problem data
from TADindInterception_data import TADindInterception
## From the file name solver_interception, we import the function solver_interception for interception mode problem solution
from solution_interception import solution_interception
## From the file name solver_rescue, we import the function solver_rescue for rescue mode problem solution
from solution_rescue import solution_rescue
##Following function RHdata(), will give the problem data for the interception mode and rescue mode
def RHdata(T,delta,lamda_var):
    ###rescue mode-mu=0########
    Rpar  = TADindRescue(0) #resue mode data when the parametr mu=0
    Rescue = solution_rescue(Rpar,T,delta) #resue mode RDE solution when mu=0
    ###rescue mode-mu=1###########
    Rcpar = TADindRescue(1)#resue mode data when the parametr mu=1
    cRescue = solution_rescue(Rcpar,T,delta) #resue mode RDE solution when mu=1
    ## Interception mode when attacker is non-suicidal 
    Ipar  = TADindInterception(lamda_var) #Interception mode data 
    Interception = solution_interception(Ipar,T,delta) #Interception mode solution
    return Rescue,cRescue,Interception

#[rescue,crescue,Interception] = RHdata(6,0.05,1)
# print(rescue)
