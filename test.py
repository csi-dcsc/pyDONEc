import numpy as np
import pyDONEc

def paraboloid(x):
    centers=np.linspace(-10.0,10.0,degrees_of_freedom)
    parab= np.sum((x-centers)**2)
    noise=np.random.normal(0.0,1.0)

    return parab+noise


degrees_of_freedom=10
initial_guess=np.ones(degrees_of_freedom)*0.3
lower_bounds=np.ones(degrees_of_freedom)*(-20.0)
upper_bounds=np.ones(degrees_of_freedom)*(20.0)
cosine_number=1000
regularization_factor=1.0
cosine_sigma=0.05
expl_factors=np.ones(degrees_of_freedom)*0.5
memory_size=100


min_pos=np.linspace(-10.0,10.0,degrees_of_freedom)



#use with direct function call

opt=pyDONEc.optimizer(initial_guess,degrees_of_freedom,lower_bounds,upper_bounds,cosine_number,regularization_factor,cosine_sigma,expl_factors,memory_size)

for i in range(200):
    opt.step(paraboloid)
    print "iteration: "+str(i)+" rms error= "+str(np.sqrt(np.mean((opt.getmin()-min_pos)**2/degrees_of_freedom)))
print "minimum location: "+str(min_pos)
print "estimated minimum: "+str(opt.getmin())
print "final rms error: "+str(np.sqrt(np.mean((opt.getmin()-min_pos)**2/degrees_of_freedom)))
        
#use with separate metric measurement

opt=pyDONEc.optimizer(initial_guess,degrees_of_freedom,lower_bounds,upper_bounds,cosine_number,regularization_factor,cosine_sigma,expl_factors,memory_size)

a=np.ones(degrees_of_freedom)*0.3
for i in range(200):
    met=paraboloid(a)
    opt.nullstep(a,met)
    a=opt.getlaststep()[0]
    print "iteration: "+str(i)+" rms error= "+str(np.sqrt(np.mean((opt.getmin()-min_pos)**2/degrees_of_freedom)))
print "minimum location: "+str(min_pos)
print "estimated minimum: "+str(opt.getmin())
print "final rms error: "+str(np.sqrt(np.mean((opt.getmin()-min_pos)**2/degrees_of_freedom)))


