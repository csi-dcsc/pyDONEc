import numpy
import ctypes
import os 


class optimizer():
    #initialization, parameters are:
    #startvect: Initial guess of the minimum position
    #d=degrees of freedom
    #lb=global lower bound, or ndarray of lower bounds (the length must be equal to the number of degrees of freedom)
    #ub=global upper bound, or ndarray of upper bounds (the length must be equal to the number of degrees of freedom)
    #D=number of basis functions
    #lam=regularization parameter
    #sigma=expected width of the metric function spectra
    #expl=size of the exploration steps
    #memory= size of the memory buffer for the function fit
    def __init__(self,startvect,d,lb,ub,D,lam,sigma,expl,memory):

        #load the done step function from the dll

        cwd = os.getcwd()
        os.chdir("dlls")
        DONEdll = ctypes.cdll.LoadLibrary("DONEdll.dll")
                                        
        self.DONEvect= getattr(DONEdll,"?DONE@@YAHPEAN0H00NNN0HH@Z")
        os.chdir(cwd)
        
        #store values of the parameters
        self.d=int(d)
        self.D=ctypes.c_double(D)
        self.sigma=ctypes.c_double(sigma)
        self.lam=ctypes.c_double(lam)
        self.memory=int(memory)
        if type(lb)==numpy.ndarray:
            self.lb=lb
        else:
            self.lb=numpy.ones(d)*lb
        if type(ub)==numpy.ndarray:
            self.ub=ub
        else:
            self.ub=numpy.ones(d)*ub
        if type(expl)==numpy.ndarray:
            self.expl=expl
        else:
            self.expl=numpy.ones(d)*expl

        self.reset=True
        
        #converts Python ndarrays to pointers to c++ vectors 
        self.lbpoint=self.lb.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        self.ubpoint=self.ub.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        self.explpoint=self.expl.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        #creates the expected minimum coordinates and next step information, and converts in c++ vectors
        self.x0=startvect
        self.x0point=self.x0.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        
        #the next step information has size d+1, and contains the parameters used for the measurement, followed by the corresponding value of the metric
        self.measinfo=numpy.zeros(self.d+1)
        self.measinfo[0:self.d]=self.x0

        self.measinfopoint=self.measinfo.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    #step function of the algorithm, evalulates the passed function in the next step location and updates x0 and measinfo
    def step(self,function):
        self.measinfo[self.d]=function(self.measinfo[0:self.d])
        if self.reset:
            self.DONEvect(self.measinfopoint,self.x0point,self.d,self.lbpoint,self.ubpoint,self.D,self.lam,self.sigma,self.explpoint,self.memory,1)
            self.reset=False
        else:
            self.DONEvect(self.measinfopoint,self.x0point,self.d,self.lbpoint,self.ubpoint,self.D,self.lam,self.sigma,self.explpoint,self.memory,0)

    #null step function of the algorithm, performs a step in a user defined location, with a user defined corresponding value of the metric function
    def nullstep(self,x,metric):
        self.measinfo[self.d]=metric
        self.measinfo[0:self.d]=x
        if self.reset:
            self.DONEvect(self.measinfopoint,self.x0point,self.d,self.lbpoint,self.ubpoint,self.D,self.lam,self.sigma,self.explpoint,self.memory,1)
            self.reset=False
        else:
            self.DONEvect(self.measinfopoint,self.x0point,self.d,self.lbpoint,self.ubpoint,self.D,self.lam,self.sigma,self.explpoint,self.memory,0)

    #returns the expected position of the minimum
    def getmin(self):
        return self.x0
    #returns the most recent dataset and metric value
    def getlaststep(self):
        return self.measinfo[0:self.d],self.measinfo[self.d]


