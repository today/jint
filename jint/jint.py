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
import cgi
import datetime
import time
import wsgiref.handlers


from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Todo(db.Model):
  uid = db.IntegerProperty(required=True)
  author = db.UserProperty(required=True)
  content = db.StringProperty(multiline=True)
  startDate = db.DateTimeProperty(auto_now_add=True)
  finishDate = db.DateTimeProperty(auto_now_add=False)
  status = db.IntegerProperty()  # 0 new   1 finish   2 delay
  remark = db.StringProperty(multiline=True)


class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      self.response.headers['Content-Type'] = 'text/html'
    else:
      self.redirect(users.create_login_url(self.request.uri))

    self.response.out.write("""
        <html>
        <head>
        <script src="js/jquery-1.2.6.js"></script>
        <script>
            $(document).ready(function() {
                //
                //$(".datetime").hide();
                $(".remark").hide();
                //
                //$(".content").hover(function() {
                //    $(this).next("").fadeIn();
                //}, function() {
                //	$(this).next("").fadeOut();
                //});
            });

            var go_f = function(id){
                document.form0.action="/change";
                document.form0.method="post";
                document.form0.uid.value = id;
                document.form0.status.value = 1;
                
                $(".remark").show();
            }
                        
            var go_delay = function(id){
                document.form0.action="/change";
                document.form0.method="post";
                document.form0.uid.value = id;
                document.form0.status.value = 2;
                document.form0.submit();
            }
            
            var go_renew = function(id){
                document.form0.action="/change";
                document.form0.method="post";
                document.form0.uid.value = id;
                document.form0.status.value = 0;
                document.form0.submit();
            }

            var go_reload = function(id){
                document.form0.action="/";
                document.form0.method="get";
                document.form0.status.value = id;
                document.form0.submit();
            }

        </script>
        <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
        <title>Todo List</title>
        </head><body>
        """)

    self.response.out.write("""<table border="0"><tr><td>""")
    self.response.out.write("""<div class="create" >
          <form name="form1" action="/sign" method="post">
            <div>Add Todo:<br/>
            <textarea name="content" rows="3" cols="40"></textarea><br/>
            <input type="submit" value="record"></div>
          </form>
          </div>
          """)

    greetings = db.GqlQuery("SELECT * "
                            "FROM Todo "
                            "WHERE author=:TheAuthor AND status=0"
                            "ORDER BY startDate DESC LIMIT 10",
                            TheAuthor=users.get_current_user())

    self.response.out.write("""<div >Todo List:<br/>
                            <table border="1" style="font-size:24" ><tr>
                            <th>&nbsp;</th>
                            <th>&nbsp;</th>
                            <th width="300">Todo</th>
                            <th>&nbsp;</th></tr>"""
                           )
    
    count = 1
    for greeting in greetings:
      sUID = greeting.uid
      sContent = cgi.escape(greeting.content)
      sDate = greeting.startDate.strftime("%Y-%m-%d %H:%M:%S")
      sUser = greeting.author
      sEndTime = ""
      if greeting.finishDate:
        sEndTime = greeting.finishDate.strftime("%Y-%m-%d %H:%M:%S")

      self.response.out.write("""<tr>
                                <td><input type="button" name="b11" value="Finish" onclick="go_f('%s')" /></td>
                                <td>%d</td>
                                <td><span class="content">%s</span>
                                <br/><span style="font-size:16;color:blue">Create at %s</span></td>
                                <td>
                                <input type="button" name="b12" value="Delay" onclick="go_delay('%s')" />
                                </td>
                                </tr>"""
        % ( sUID, count, sContent, sDate, sUID) )
      count+=1

    self.response.out.write("""
          </table></div>
          </td></tr>
          <tr><td>
          <div class="remark" >
          <form name="form0" action="" method="post">
            <input type="hidden" name="uid" value="">
            <input type="hidden" name="status" value="">
            Remark:<br/>
            <textarea name="remark" rows="3" cols="40"></textarea><br>
            <input type="submit" name="s2" value=" O K ">
          </form>
          </div>
          
          </td></tr></table>
      """)

    iStatus = 1
    if self.request.get('status'):
        sStatus = self.request.get('status')
        iStatus = long(sStatus)
        #self.response.out.write("##############iStatus=%d ###########" % iStatus )


    greetings = db.GqlQuery("SELECT * "
                            "FROM Todo "
                            "WHERE author=:1 AND status=:2 "
                            "ORDER BY startDate DESC LIMIT 40"
                            , users.get_current_user(), iStatus)

    self.response.out.write("""
                            <form name="form2" action="" method="get">
                            <input type="button" name="b2" value="Finished List" onclick="go_reload(1)" >
                            <input type="button" name="b3" value="Delay List" onclick="go_reload(2)" >
                            <input type="button" name="b4" value="Todo List" onclick="go_reload(0)" >
                            </form>
                            """)
    if 0 == iStatus :
        self.response.out.write("Todo List:")
    elif 1 == iStatus :
        self.response.out.write("Finish List:")
    elif 2 == iStatus :
        self.response.out.write("Delay List:")
    else :
        self.response.out.write("Error")
    
    self.response.out.write("""                           
                            <table border="1" width=""><tr>
                            <th >&nbsp;</th>
                            <th >ID</th>
                            <th width="250">Content</th>
                            <th NOWRAP>period</th>
                            <th>Author</th>
                            <th>Remark</th>
                            <th>&nbsp;</th>
                            </tr>""")

    count = 1
    for greeting in greetings:
        sUID = greeting.uid
        sContent = cgi.escape(greeting.content)
        sStartTime = greeting.startDate.strftime("%Y-%m-%d<br/>%H:%M:%S")
        sUser = greeting.author
        sEndTime = "&nbsp;"
        if greeting.finishDate:
            sEndTime = greeting.finishDate.strftime("%Y-%m-%d<br/>%H:%M:%S")
            
        sRemark = "&nbsp;"
        if greeting.remark:
            sRemark = greeting.remark
            
        self.response.out.write("""<tr>
                                <td>%d</td>
                                <td>%s</td>
                                <td width="150">%s</td>
                                <td NOWRAP>%s<br/>~<br/>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td><input type="button" name="b12" value="Renew" onclick="go_renew('%s')" /></td>
                                </tr>"""
                    % ( count, sUID, sContent, sStartTime, sEndTime, sUser, sRemark, sUID ) )
        count+=1

    self.response.out.write("""</table></body></html>""")

class CreateTask(webapp.RequestHandler):
  def post(self):
    user = None
    if users.get_current_user():
      user = users.get_current_user()
    else :
      self.redirect('/')

    nowTime = datetime.datetime.now()
    sUid = long( time.mktime( nowTime.timetuple() ) )


    task = Todo( uid=sUid, author=user )

    task.content = self.request.get('content')
    task.status = 0

    task.put()
    self.redirect('/')

class ChangeTask(webapp.RequestHandler):
  def post(self):
    UID = self.request.get('uid')
    q = db.GqlQuery("SELECT * FROM Todo WHERE uid = :1", long(UID) )
    task = q.get()
    task.finishDate = datetime.datetime.now()
    
    if self.request.get('remark'):
        task.remark = self.request.get('remark')
    
    if self.request.get('status'):
        task.status = long( self.request.get('status') )
        
    task.put()

    self.redirect('/')

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/sign', CreateTask),
  ('/change', ChangeTask)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
