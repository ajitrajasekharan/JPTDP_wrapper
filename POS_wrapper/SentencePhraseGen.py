# -*- coding: utf-8 -*-
import os
import ResponseHandler
import subprocess
import urllib

try:
    from subprocess import DEVNULL  # Python 3.
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

class SentencePhraseGen(ResponseHandler.ResponseHandler):
	def handler(self,write_obj = None):
		print "In derived class"
		if (write_obj is not None):
			print "Arg = ",write_obj.path[1:]
                        param=urllib.unquote(write_obj.path[1:]).decode('utf8')
                        param=param.replace("$","\\$")
			params = "./graph_process.sh \"%s\"" % (param)
			p = subprocess.Popen(params,shell=True,stdout=subprocess.PIPE,stderr=DEVNULL)
			out = p.communicate()
			print len(out)
			print  out[0]
			if (len(out) > 1):
				write_obj.wfile.write(out[0])
			else:
				write_obj.wfile.write("[]")
			#write_obj.wfile.write("NF_EOS\n")








def my_test():
    cl = SentencePhraseGen()

    cl.handler()




#my_test()
