# -*- coding: utf-8 -*-
import os
import ResponseHandler 
import subprocess
import urllib
import jPTDP
import tempfile

global base_path
global first_call
global parser
global args
global options
global counter 
first_call = 0
try:
    from subprocess import DEVNULL  
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

class PhraseServer(ResponseHandler.ResponseHandler):
	def handler(self,write_obj = None,data = None):
		print "In derived class"
		if (write_obj is not None):
			global first_call
			global parser
			global args
			global options
			global base_path
			prog_path = ""
			model_path = ""
			model_params_path = ""
			if (first_call == 0):
				if ("CONFIG_DIR"  in os.environ ):
					prog_path = os.environ["CONFIG_DIR"] + '/' + "other/jPTDP.py"
					model_path = os.environ["CONFIG_DIR"] + '/' + "UD_English/model"
					model_params_path = os.environ["CONFIG_DIR"] + '/' + "UD_English/model.params"
				else:
					base_path = os.getcwd()
					print "CONFIG_DIR NOT SET!!! USING DEFAULT TEST PATH!!!!", base_path
					#prog_path = base_path + '/' + "other"
					prog_path = base_path
					model_path = base_path + '/' + "UD_English/model"
					model_params_path = base_path + '/' + "UD_English/model.params"
				first_call = 1
				argv = [prog_path, '--predict', '--model', model_path, '--params', model_params_path, '--test', 'dummy', '--outdir', '.', '--output', 'dummy.tag', '--istext', '1']
				print "FIRST CALL!!!!", argv
				options,args = jPTDP.init(argv)
				parser = jPTDP.load_model(options)
			else:
				print "SUBSEQUENT CALLS"
			inp_file_name = tempfile.NamedTemporaryFile(dir='.').name
			out_file_name = tempfile.NamedTemporaryFile(dir='.').name
			ifp = open(inp_file_name,'w')
			ifp.write(data.encode('utf-8'))
			ifp.close()
			jPTDP.predict_text(parser,inp_file_name,out_file_name)
			os.remove(inp_file_name)
			ofp = open(out_file_name,'r')
			out_data = ofp.read()
			ofp.close()
			os.remove(out_file_name)
			print "Arg = ",data,"\n",out_data
			if (len(out_data) > 1):
				write_obj.wfile.write(out_data)
			else:
				write_obj.wfile.write("[]")
			write_obj.wfile.write("\n")








def my_test():
    cl = FastBulkCompare()

    cl.handler()




#my_test()
