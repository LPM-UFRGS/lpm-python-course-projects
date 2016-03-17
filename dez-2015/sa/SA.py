#!/bin/python
import sgems, math

class SA:
    def __init__(self):
        pass

    def initialize(self, params):
	self.params=params
        print "initialize hello world"
        print "parametros: "+ str(params)
	print "chaves: "+str(params.keys())
	self.prop1 = params["GridName1"]["property"]
	self.prop2 = params["GridName2"]["property"]
	self.check = params["check1"]["value"]
	self.cte = params["ctevalue"]["value"]
	self.radio1 = params["radioButton"]["value"]
	self.radio2 = params["radioButton_2"]["value"]
        return True

    def execute(self):
	dif = []
	Prop1=sgems.get_property(self.params["GridName1"]["grid"],self.prop1)
	Prop2=sgems.get_property(self.params["GridName2"]["grid"],self.prop2)
	
	dif2 = []
	for i in range(len(Prop1)):
# 	  if(Prop1[i] != sgems.nan() and Prop2[i] != sgems.nan()): 
 	  if(math.isnan(Prop1[i]) == False and math.isnan(Prop2[i]) == False): 
	    dif.append((Prop1[i]-Prop2[i])/Prop1[i])
	  else:
	    dif.append(sgems.nan())
	final_prop = "Deviation"	
        lst = sgems.get_property_list(self.params["GridName1"]["grid"])
        if (final_prop in lst):
          flag = 0
          i = 1
          while(flag==0):
            new_prop_name = final_prop + "_"+ str(i)
            if(new_prop_name not in lst):
              flag = 1
              final_prop = new_prop_name
            i = i+1
        print final_prop
	#for i in range(len(Prop1)):
	 # dif2.append((Prop1[i]+dif[i]))
	
	sgems.set_property(self.params["GridName1"]["grid"],final_prop,dif)
	#sgems.set_property(self.params["GridName2"]["grid"],"sum",dif2)
	PP=[]
	a = float(self.cte)
	print a, self.cte
	for i in range(len(Prop2)):
	  if(self.check == '1'):
	    if(self.radio1 == '1'):
	      print Prop1[i], sgems.nan()
#  	      if(Prop1[i]==float(sgems.nan())):
  	      if(math.isnan(Prop1[i])==True):
		print 'estou no laco i =', i,
		PP.append(Prop2[i]+Prop2[i]*a)
	      else:
	        PP.append(Prop2[i])
	    if(self.radio2 == "1"):
	      if(math.isnan(Prop1[i]) == True):
		PP.append(Prop2[i]-Prop2[i]*a)
	      else:
	        PP.append(Prop2[i])
	final_prop2 = "Post_process"	
	lst2 = sgems.get_property_list(self.params["GridName2"]["grid"])
	if (final_prop2 in lst2):
	  flag = 0
 	  i = 1
	  while(flag==0):
	    new_prop_name2 = final_prop2 + "_"+ str(i)
	    if(new_prop_name2 not in lst2):
   	      flag = 1
	      final_prop2 = new_prop_name2
	  i = i+1
	print final_prop2
	sgems.set_property(self.params["GridName2"]["grid"],final_prop2,PP)  
	
	return True

    def finalize(self):
        return True

    def name(self):
        return "SA"
############################################
def get_plugins():
    return ["SA"]
