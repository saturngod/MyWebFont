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
import os

class HomeHandler(webapp.RequestHandler):
    def get(self):
		self.response.out.write("""
			<html>
				<head>
					<title>Myanmar Web Font</title>
				</head>
				<body>
					<p>Supported Unicode Fonts are 
					Yunghkio, Myanmar3 , Paduk, Parabaik.
					</p>
					<p>Also support Zawgyi-One</p>
					
					<h1>CSS link</h1>
					<h2>Yunghkio</h2>
					<code>
						&lt;link href='http://mywebfont.appspot.com/css?font=yunghkio' rel='stylesheet' type='text/css'&gt;
					</code>
					<h2>Myanmar3</h2>
					<code>
						&lt;link href='http://mywebfont.appspot.com/css?font=myanmar3' rel='stylesheet' type='text/css'&gt;
					</code>
					<h2>Padauk</h2>
					<code>
						&lt;link href='http://mywebfont.appspot.com/css?font=padauk' rel='stylesheet' type='text/css'&gt;
					</code>
					<h2>Parabaik</h2>
					<code>
						&lt;link href='http://mywebfont.appspot.com/css?font=parabaik' rel='stylesheet' type='text/css'&gt;
					</code>
					<h2>Zawgyi-One</h2>
					<code>
						&lt;link href='http://mywebfont.appspot.com/css?font=zawgyi' rel='stylesheet' type='text/css'&gt;
					</code>
					
					<h1>Need to do </h1>
					You need to declare font-family in CSS like following
					<code>
						h1 { font-family:"Masterpiece Uni Sans",Yunghkio,Myanmar3}
					</code>
					<blockquote>
						I recommend to start with Masterpiece Uni Sans.It's for some peple who use iOS or Mac. Mac and iOS can use Masterpiece only. So, please start with <span style='color:red'>"Masterpiece Uni Sans"</span>.
					</blockquote>
				</body>
			</html>
		""")
class MainHandler(webapp.RequestHandler):
    def get(self):
		#check font name
		font_family="Master Piece Uni Sans"
		font_file=self.request.get("font").lower();
		if(self.request.get("font").lower()=='yunghkio'):
			font_family="Yunghkio"
		elif(self.request.get("font").lower()=='myanmar3'):
			font_family="Myanmar3"
		elif(self.request.get("font").lower()=='padauk'):
			font_family="Padauk"
		elif(self.request.get("font").lower()=='parabaik'):
			font_family="Parabaik"
		
		browsername=Getbrowsername()
		font_type=""
		
		#check browser .. Myanmar Unicode Font Embed only work on firefox, opera and ie
		if(browsername=='firefox' or browsername=='opera' or browsername=='chrome' ):
			font_type='ttf'
		elif(browsername=='ie'):
			font_type='eot'
		
		#not supported on mac
		if(mac_os()):
			font_type=""
		
		
		#check and forece Masterpiece if OS is apple related
		if(browsername=='iPhone' or browsername=='iPad'):
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
				css+="\nsrc:local('"+font_family+"');\n}"
				
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
    application = webapp.WSGIApplication([('/',HomeHandler),('/css', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
