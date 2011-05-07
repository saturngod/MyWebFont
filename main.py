#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os


class HomeHandler(webapp.RequestHandler):
	def get(self):
		template_value={
			'title':'Myanmar Web Font by saturngod'
		}
		path=os.path.join(os.path.dirname(__file__),'view/index.html')
		self.response.out.write(template.render(path,template_value))

class MainHandler(webapp.RequestHandler):
    def get(self):
		#check font name
		font_family="Master Piece Uni Sans"
		font_file=self.request.get("font").lower();
		if(self.request.get("font").lower()=='yunghkio'):
			font_file="yunghkio"
			font_family="Yunghkio"
		elif(self.request.get("font").lower()=='myanmar3'):
			font_file="myanmar3"
			font_family="Myanmar3"
		elif(self.request.get("font").lower()=='padauk'):
			font_file="padauk"
			font_family="Padauk"
		elif(self.request.get("font").lower()=='parabaik'):
			font_file="parabaik"
			font_family="Parabaik"
		
		browsername=Getbrowsername()
		font_type=""
		
		#check browser .. Myanmar Unicode Font Embed only work on firefox, opera and ie
		if(browsername=='firefox' or browsername=='opera'):
			font_type='ttf'
		elif(browsername=='ie'):
			font_type='eot'
		
		#not supported on mac
		if(mac_os()):
			font_type=""
		
		
		#check and forece Masterpiece if OS is apple related
		if(browsername=='iPhone' or browsername=='iPad' or (mac_os() and browsername=='safari')):
			font_family="Masterpiece Uni Sans"
			font_file="masterpiece"
			font_type="ttf"
			
		#zawgyi font support all browser
		if(self.request.get("font").lower()=='zawgyi'):
			font_family="Zawgyi-One"
			font_file="zawgyi"
			font_type="ttf"
			
		if(self.request.get("font").lower()=='zawgyi' and browsername=='ie'):
			font_family="Zawgyi-One"
			font_file="zawgyi"
			font_type="eot"					
		
		#check font type to load or not. Unicode font can't load in Android and chrome
		if(font_type!=""):
			css="@font-face {\nfont-family:"+font_family+";"
			
			if(browsername!='ie'):
				css+="\nsrc:local('"+font_family+"'),"
					
			font_path=self.request.host_url+"/font/"+font_file+"."+font_type
			
			if(browsername!='ie'):
				css+="url('"+font_path+"');\n}"
			else:
				css+="\nsrc:url('"+font_path+"');"
				css+="\n}"
			self.response.headers["Access-Control-Allow-Origin"] = "*"
			self.response.headers["Content-Type"] = "text/css"
			self.response.out.write(css)

def Getbrowsername():
	if(os.environ['HTTP_USER_AGENT'].find('iPhone')!=-1):
		return "iPhone"
	elif(os.environ['HTTP_USER_AGENT'].find('iPad')!=-1):
		return "iPad"
	elif(os.environ['HTTP_USER_AGENT'].find('Chrome')!=-1):
		return "chrome"
	elif(os.environ['HTTP_USER_AGENT'].find('Safari')!=-1):
		return "safari"
	elif(os.environ['HTTP_USER_AGENT'].find('Firefox')!=-1):
		return "firefox"
	elif(os.environ['HTTP_USER_AGENT'].find('Opera')!=-1):
		return "opera"
	elif(os.environ['HTTP_USER_AGENT'].find('MSIE')!=-1):
		return "ie"

def mac_os():
	if(os.environ['HTTP_USER_AGENT'].find('Mac')!=-1):
		return True
	return False
			
def main():
    application = webapp.WSGIApplication([('/', HomeHandler),('/css', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
