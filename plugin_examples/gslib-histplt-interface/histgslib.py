#!/bin/python
import sgems, math, time, sys, os, sgems
import os.path

class histplugin():
  def __init__(self,parameters):

    # gui parameters from ar2gems  
    self.params=parameters

    # 'with file' dictionary
    self.dict_with_file={}
    # 'with property' dictionary
    self.dict_with_property={}
    
    # general parameters
    self.dict_gen_params={}
    self.dict_gen_params['gslib_executables_folder']='/home/attila/ar2-gslib/gslib90'
    self.dict_gen_params['gslib_hist_executable']='histplt'
    self.dict_gen_params['work_folder']='/home/attila/ar2-gslib'
    self.dict_gen_params['par_file']='hist.par'
    self.dict_gen_params['display_command']='evince'
    self.dict_gen_params['execution_status']='ok'
    self.dict_gen_params['path_separator']='/'
    self.dict_gen_params['datafilename_with_property']='data_1.dat'

    # SANITY CHECKS
    # look if we can read the executable
    if os.path.isfile(self.dict_gen_params['gslib_executables_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['gslib_hist_executable'])!=True:
      print "ERROR: Cannot find gslib histplt file!"
      self.dict_gen_params['execution_status']="ERROR"

  ### COLLECT USER GUI INPUTS ############################################################################
  def get_gui_input(self):

    ### FIRST CHOOSE BETWEEN 'with_file' and 'with_property'
    if (self.params['radioButton_5']['value']=='1' and self.params['radioButton_6']['value']=='0'):
      self.dict_gen_params['execution_type']='with_file'
    elif (self.params['radioButton_5']['value']=='0' and self.params['radioButton_6']['value']=='1'):
      self.dict_gen_params['execution_type']='with_property'
    elif (self.params['radioButton_5']['value']=='0' and self.params['radioButton_6']['value']=='0'):
      print "Plugin execution type not set.."
      self.dict_gen_params['execution_status']="ERROR"
    else:
      print "Error in execution type parameters."
      self.dict_gen_params['execution_status']="ERROR"
#      sys.exit(0)

    ### 'WITH FILE' INPUTS ###
    if self.dict_gen_params['execution_type']=='with_file':

      #input defined by the widget: a spinbox with -1 to 99 integers, default -1
      self.dict_with_file['number_of_quantiles']=self.params['spinBox_3']['value']
      # filechooser widget, must input a valid folder
      self.dict_gen_params['outputfile_folder']=self.params['filechooser_2']['value']
      # any name
      self.dict_gen_params['outputfile_name']=self.params['lineEdit_8']['value']
      # data file defined by the filechooser widget
      self.dict_with_file['datafile']=self.params['filechooser']['value']
      # 
      self.dict_with_file['number_of_classes']=self.params['spinBox_2']['value']
      self.dict_with_file['pos_stat']=self.params['doubleSpinBox']['value']
      self.dict_with_file['decimal_places']=self.params['spinBox_4']['value']
      self.dict_with_file['column_data']=self.params['spinBox']['value']
      self.dict_with_file['weight']=self.params['spinBox_5']['value']
      self.dict_with_file['lim_cut_min']=self.params['lineEdit']['value']
      self.dict_with_file['lim_cut_max']=self.params['lineEdit_2']['value']
      self.dict_with_file['value_min']=self.params['lineEdit_4']['value']
      self.dict_with_file['value_max']=self.params['lineEdit_3']['value']
      self.dict_with_file['title']=self.params['lineEdit_5']['value']
      self.dict_with_file['max_frequency']=self.params['lineEdit_7']['value']
      self.dict_with_file['reference_value']=self.params['lineEdit_6']['value']

      if (self.params['radioButton']['value']=='0' and self.params['radioButton_2']['value']=='1'):
        self.dict_with_file['scale']='0'
      elif (self.params['radioButton']['value']=='1' and self.params['radioButton_2']['value']=='0'):
        self.dict_with_file['scale']='1'
      elif (self.params['radioButton']['value']=='0' and self.params['radioButton_2']['value']=='0'):
        print "Scale parameter not set."
        self.dict_gen_params['execution_status']="ERROR"
      else:
        print "Error in scale parameters."
        self.dict_gen_params['execution_status']="ERROR"
  #      sys.exit(0)

      if (self.params['radioButton_4']['value']=='1' and self.params['radioButton_3']['value']=='0'):
        self.dict_with_file['histogram_type']='0' #frequency rb4
      elif (self.params['radioButton_4']['value']=='0' and self.params['radioButton_3']['value']=='1'):
        self.dict_with_file['histogram_type']='1' #acum rbutton_3
      elif (self.params['radioButton_4']['value']=='0' and self.params['radioButton_3']['value']=='0'):
        print "Histogram type not set."
        self.dict_gen_params['execution_status']="ERROR"
      else:
        print "Error in histogram type parameters."
        self.dict_gen_params['execution_status']="ERROR"
  #      sys.exit(0)

    ############ WITH PROPERTY INPUTS ##########
    if self.dict_gen_params['execution_type']=='with_property':
    
      self.dict_with_property['weight_region']=self.params['propertyselector_2']['region']
      self.dict_with_property['weight_property']=self.params['propertyselector_2']['property']
      self.dict_with_property['weight_grid']=self.params['propertyselector_2']['grid']
      self.dict_with_property['data_region']=self.params['propertyselector']['region']
      self.dict_with_property['data_property']=self.params['propertyselector']['property']
      self.dict_with_property['data_grid']=self.params['propertyselector']['grid']
      self.dict_gen_params['outputfile_folder']=self.params['filechooser_3']['value']
      self.dict_gen_params['outputfile_name']=self.params['lineEdit_9']['value']
      self.dict_with_property['lim_cut_min']=self.params['lineEdit_10']['value']
      self.dict_with_property['lim_cut_max']=self.params['lineEdit_11']['value']
      self.dict_with_property['value_min']=self.params['lineEdit_12']['value']
      self.dict_with_property['value_max']=self.params['lineEdit_13']['value']
      self.dict_with_property['max_frequency']=self.params['lineEdit_14']['value']
      self.dict_with_property['reference_value']=self.params['lineEdit_15']['value']
      self.dict_with_property['number_of_quantiles']=self.params['spinBox_8']['value']
      self.dict_with_property['number_of_classes']=self.params['spinBox_6']['value']
      self.dict_with_property['pos_stat']=self.params['doubleSpinBox_2']['value']
      self.dict_with_property['decimal_places']=self.params['spinBox_7']['value']
      self.dict_with_property['title']=self.params['lineEdit_16']['value']

      if (self.params['radioButton_7']['value']=='1' and self.params['radioButton_8']['value']=='0'):
        self.dict_with_property['scale']='0'
      elif (self.params['radioButton_7']['value']=='0' and self.params['radioButton_8']['value']=='1'):
        self.dict_with_property['scale']='1'
      elif (self.params['radioButton_7']['value']=='0' and self.params['radioButton_8']['value']=='0'):
        print "Scale parameter not set."
        self.dict_gen_params['execution_status']="ERROR"
      else:
        print "Error in scale parameters."
        self.dict_gen_params['execution_status']="ERROR"
  #      sys.exit(0)

      if (self.params['radioButton_9']['value']=='1' and self.params['radioButton_10']['value']=='0'):
        self.dict_with_property['histogram_type']='0'
      elif (self.params['radioButton_9']['value']=='0' and self.params['radioButton_10']['value']=='1'):
        self.dict_with_property['histogram_type']='1'
      elif (self.params['radioButton_9']['value']=='0' and self.params['radioButton_10']['value']=='0'):
        print "Histogram type not set."
        self.dict_gen_params['execution_status']="ERROR"
      else:
        print "Error in histogram type parameters."
        self.dict_gen_params['execution_status']="ERROR"
  #      sys.exit(0)
    
  ### WRITE .PAR FILE #############################################################################################
  def write_par_file(self):

    ## first try to open .par file for writing
    try:
      file=open(self.dict_gen_params['work_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['par_file'],'w')
    except:
      print 'Problem opening requested par file for writing.'
      self.dict_gen_params['execution_status']='ERROR'
#      sys.exit(0)

    if self.dict_gen_params['execution_status'] != 'ERROR' and self.dict_gen_params['execution_type']=='with_file':      
      writebuff="Parameters file generated by histgslib Ar2GeMS plugin, "+time.strftime("%c")+".\nPlugin execution type: "+self.dict_gen_params['execution_type']+'\n'
      file.write(writebuff)
      writebuff="START OF PARAMETERS:\n"
      file.write(writebuff)      
      writebuff=self.dict_with_file['datafile']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['column_data']+" "+self.dict_with_file['weight']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['lim_cut_min']+" "+self.dict_with_file['lim_cut_max']+"\n"
      file.write(writebuff)
      if (self.dict_gen_params['outputfile_folder'] != ''):
        writebuff=self.dict_gen_params['outputfile_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['outputfile_name']+"\n"
      else:
        writebuff=self.dict_gen_params['outputfile_name']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['value_min']+" "+self.dict_with_file['value_max']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['max_frequency']+"\n"
      file.write(writebuff)    
      writebuff=self.dict_with_file['number_of_classes']+"\n"
      file.write(writebuff)    
      writebuff=self.dict_with_file['scale']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['histogram_type']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['number_of_quantiles']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['decimal_places']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['title']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['pos_stat']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_file['reference_value']+"\n"
      file.write(writebuff)
      file.close()

    if self.dict_gen_params['execution_status'] != 'ERROR' and self.dict_gen_params['execution_type']=='with_property':      

      ### WRITE THE .PAR FILE (AFTER, THE DATA FILE WILL BE WRITTEN) ##
      writebuff="Parameters file generated by histgslib Ar2GeMS plugin, "+time.strftime("%c")+".\nPlugin execution type: "+self.dict_gen_params['execution_type']+"\n"
      file.write(writebuff)
      writebuff="START OF PARAMETERS:\n"
      file.write(writebuff)
      writebuff=self.dict_gen_params['work_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['datafilename_with_property']+'\n'
      file.write(writebuff)
      
      # column data will be 1 ever.
      # the weight column will depend if the weight is set, 0 if no weight is set, 2 if some weight is set.
      if (self.dict_with_property['weight_property']=='' or self.dict_with_property['weight_grid']==''):
        writebuff='1 0\n'
      else:
        writebuff='1 2\n'
      file.write(writebuff)

      writebuff=self.dict_with_property['lim_cut_min']+" "+self.dict_with_property['lim_cut_max']+"\n"
      file.write(writebuff)
      if (self.dict_gen_params['outputfile_folder'] != ''):
        writebuff=self.dict_gen_params['outputfile_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['outputfile_name']+"\n"
      else:
        writebuff=self.dict_gen_params['outputfile_name']+"\n"  
      file.write(writebuff)
      writebuff=self.dict_with_property['value_min']+" "+self.dict_with_property['value_max']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_property['max_frequency']+"\n"
      file.write(writebuff)    
      writebuff=self.dict_with_property['number_of_classes']+"\n"
      file.write(writebuff)    
      writebuff=self.dict_with_property['scale']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_property['histogram_type']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_property['number_of_quantiles']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_property['decimal_places']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_property['title']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_property['pos_stat']+"\n"
      file.write(writebuff)
      writebuff=self.dict_with_property['reference_value']+"\n"
      file.write(writebuff)
      file.close()

      ### in 'with_property' we write the data file from ar2gems in gslib format      
      self.write_datafile_from_ar2gems()
    
  ### EXECUTE GSLIB HIST #################################################################################
  def execute_gslib_hist(self):
    cmd=self.dict_gen_params['gslib_executables_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['gslib_hist_executable']+" "+self.dict_gen_params['work_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['par_file']
    os.system(cmd+" > "+self.dict_gen_params['work_folder']+self.dict_gen_params['path_separator']+"out.log 2>&1")
    ### print gslib message
    gslib_msg = os.popen('cat '+self.dict_gen_params['work_folder']+self.dict_gen_params['path_separator']+"out.log").read()
    print gslib_msg
    ### check if gslib hist finishes correctly
    if ('HISTPLT Version' not in gslib_msg and 'Finished' not in gslib_msg):
      print "Gslib Histogram did not finished."
      self.dict_gen_params['execution_status']='ERROR'
      
  ### visualize histogram ################################################################################
  def visualize_result(self):
    os.system(self.dict_gen_params['display_command']+' '+self.dict_gen_params['outputfile_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['outputfile_name'])
    
  ### write the datafile for the 'with_property' #########################################################
  def write_datafile_from_ar2gems(self):
    try:
      file=open(self.dict_gen_params['work_folder']+self.dict_gen_params['path_separator']+self.dict_gen_params['datafilename_with_property'],'w')
    except:
      print 'Problem opening requested par file for writing.'
      self.dict_gen_params['execution_status']='ERROR'
#      sys.exit(0)

    #get the data and weight, NOT CONSIDERING REGIONS YET
    data=sgems.get_property(self.dict_with_property['data_grid'],self.dict_with_property['data_property'])
    
    # if there is not weight, put just the data
    if self.dict_with_property['weight_property']=='':
      file.write('TITLE\n')
      file.write('1\n')
      file.write(self.dict_with_property['data_grid']+'\n')
      for item in data:
        file.write(str(item)+'\n')
      file.close()
    # put the data and the weight
    else:
      file.write('TITLE\n')
      file.write('2\n')
      file.write(self.dict_with_property['data_grid']+'\n')
      file.write(self.dict_with_property['weight_property']+'\n')
      data_weight=sgems.get_property(self.dict_with_property['weight_grid'],self.dict_with_property['weight_property'])
      # check if they have the same length
      if (len(data)==len(data_weight)):
        for x,y in zip(data,data_weight):
          file.write(str(x)+" "+str(y)+"\n")
      else:
        print "ERROR data and weight does not have the same lenght!"
        self.dict_gen_params['execution_status']='ERROR'
    
def read_params(a,j=''):
  if j=='':
    print "### Printing GUI parameters ###"
  for i in a:
    if (type(a[i])!=type({'a':1})):
      print j+"['"+str(i)+"']="+str(a[i])+" type: "+str(type(a[i]))
    else:
      read_params(a[i],j+"['"+str(i)+"']")

############################################################################################
class histgslib:
    def __init__(self):
        pass

    def initialize(self, params):
	self.params=params
        return True

    def execute(self):
#       print "Imprimindo parametros:"
#    	read_params(self.params)
#    	print "dicionario:"
#    	print self.params
    	
    	instance=histplugin(self.params)
    	instance.get_gui_input()
    	if instance.dict_gen_params['execution_status'] != 'ERROR':
          instance.write_par_file()
    	if instance.dict_gen_params['execution_status'] != 'ERROR':
          instance.execute_gslib_hist()
    	if instance.dict_gen_params['execution_status'] != 'ERROR':
          instance.visualize_result()
        else:
          print "ERROR in execution."
    	
	return True

    def finalize(self):
        return True

    def name(self):
        return "histgslib"
############################################
def get_plugins():
    return ["histgslib"]
