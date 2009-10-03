import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Recite(db.Model):
  #uid = 
  word = db.StringProperty(multiline=False)
  question = db.StringProperty(multiline=False)
  answer = db.StringProperty(multiline=False)

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    nickName = 'guest';
    if user:
      nickName = user.nickname()
    else:
      self.redirect(users.create_login_url(self.request.uri))
    
    self.response.out.write(getHtmlStart())
    self.response.out.write("""
      <style>
      .cls_try { FONT-FAMILY: verdana; font-size: 24px; border-color: black black #000000; border-style: solid; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 1px; border-left-width: 0px}
      .cls_rightanswer { FONT-FAMILY: verdana; font-size: 24px; }
      .cls_big { FONT-FAMILY: verdana; font-size: 24px; }
      .cls_rightalign  { align:right }
      
      </style>
      <script>
      $(document).ready(function(){
        //alert("jquery");
        
        $(".cls_right").hide();
        $(".cls_rightanswer").hide();

        $("input[name='tryanswer']").change(function(event){

           var tryanswer = $(this)[0].value;

           var resultArea = $(this).next();
           var rightanswer = resultArea.children(".cls_rightanswer").html();
           
           var key = resultArea.children("input")[0].value;
           

           if( tryanswer == rightanswer ){
              resultArea.children(".cls_right").attr("src","images/right.png").show();
              resultArea.children(".cls_rightanswer").css("color","green");

              $(this).css("color","green");
              
              go_result(1, key, tryanswer);
           }
           else{
              resultArea.children(".cls_right").attr("src","images/wrong.png").show();

              $(this).css("color","red");
              resultArea.children(".cls_rightanswer").css("color","red");
              
              go_result(0, key, tryanswer);
           }
        });

        $(".cls_result").toggle(
          function () {
            $(".cls_rightanswer", this).show();
            $(".cls_right", this).hide();
          },
          function () {
            $(".cls_rightanswer", this).hide();
            $(".cls_right", this).show();
          }
        );
        
        $(".cls_purewin").each(function(i){
           
           num = $(this).text();
           if( 10 < num ){
              $(this).parent().hide();
           }
           
        }); 
        
        $("input[name='b1']").click(function(event){
          $(".cls_exam").show();
        }); 
      });
      
      var go_result = function(right, key, answer){
        rightFlag = '&wrong=1';
        if( 1 == right ){
          rightFlag = '&right=1';
        }
        
        url = '/record?w=achieve' + rightFlag + '&key=' + key + '&answer=' + answer;
        
        //alert(url);
        $.ajaxSetup({
          cache: false,
          type: "GET"
        });
        $.get(url,{}, function(data){
          //alert("Data Loaded: " + data);
        }); 
        
        
      }
      </script>
      """)

    req_word = 'achieve'
    if self.request.get('w'):
      req_word = self.request.get('w')

    log = reciteLog()
    log.owner = user
    log.word =  req_word
    log.grade = '0'
    log.status = 'start'
    log.put()
      
    self.response.out.write('<span class="cls_big">The word is <b>%s</b> </span>' % (req_word) )
    self.response.out.write('<span class="cls_rightalign"> %s | <a href=\"%s\">Sign out</a></span><hr/>' %( nickName, users.create_logout_url("/")))

    recites = db.GqlQuery("SELECT * FROM Recite WHERE word=:1 LIMIT 30",  req_word )

    for recite in recites:
      
      results = db.GqlQuery("SELECT * FROM Result WHERE reciteKey=:1 ",  recite.key() )
      
      rightCount = 0
      wrongCount = 0
      
      for result in results:
        rightCount = result.rightCount
        wrongCount = result.wrongCount

      self.response.out.write('<div class="cls_exam">')
      self.response.out.write('<span>%s &nbsp;&nbsp; %s-%s=</span><span class="cls_purewin" ><b>%s</b></span>' % (recite.question, rightCount, wrongCount, rightCount-wrongCount ) )
      self.response.out.write('<br/><input type="text" name="tryanswer" value="" size="80" class="cls_try">' )
      self.response.out.write('<span class="cls_result"><br/><span class="cls_rightanswer">%s</span>' % recite.answer)
      self.response.out.write('<img src="images/right.png" class="cls_right" />')
      self.response.out.write('<input type="hidden" name="key" value="%s"></span>' % recite.key())
      self.response.out.write('</div>')

    self.response.out.write('<input type="button" name="b2" value="Commit Answer"> <input type="button" name="b1" value="Show All"><hr/>' )
    # Write the submission form and the footer of the page
    self.response.out.write("""<br/><br/><hr/>
          <form action="/add" method="post">
            <div>Word: <input type="text" name="word" value="%s" ></div>
            <div>Question: <input type="text" name="question" value="" size="80"></div>
            <div>Answer:&nbsp;&nbsp;&nbsp;<input type="text" name="answer" value="" size="80"></div>
            <div><input type="submit" value="Add"></div>
          </form>
        """ % req_word )

    self.response.out.write(getHtmlEnd())

def getHtmlStart():
  return """<html>
    <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>jint.org</title>
    <!--    -->
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.js"></script>
    
    <!--    
    <script type="text/javascript" src="images/jquery.js"></script>
    -->
    </head>
    <body>"""

def getHtmlEnd():
  return "</body></html>"


class addWord(webapp.RequestHandler):
  def post(self):
    recite = Recite()

    if users.get_current_user():
      user = users.get_current_user()

    recite.word = self.request.get('word')
    recite.question = self.request.get('question')
    recite.answer   = self.request.get('answer')
    recite.put()
    self.redirect('/?w=' + recite.word )

class Result(db.Model):
  word =  db.StringProperty(multiline=False)
  reciteKey = db.ReferenceProperty(Recite)
  owner = db.UserProperty()
  rightCount = db.IntegerProperty()
  wrongCount = db.IntegerProperty()

class Wrong(db.Model):
  word =  db.StringProperty(multiline=False)
  reciteKey = db.ReferenceProperty(Recite)
  owner = db.UserProperty()
  wrongText = db.StringProperty(multiline=False)

class reciteLog(db.Model):
  owner = db.UserProperty()
  word =  db.StringProperty(multiline=False)
  start_time = db.DateTimeProperty(auto_now_add=True)
  end_time = db.DateTimeProperty(auto_now_add=True)
  grade = db.StringProperty(multiline=False)
  status = db.StringProperty(multiline=False)
  

class recordResult(webapp.RequestHandler):
  def get(self):
    # check if login
    user = users.get_current_user()
    nickname = 'guest';
    if user:
      nickname = user.nickname()
    else:
      self.redirect(users.create_login_url(self.request.uri))
    
    textKey = self.request.get("key")
    if textKey:
      objKey = db.Key(textKey)
    else:
      return ""
    
    word = self.request.get('w')
      
    right = 0
    if self.request.get("right"):
      right = 1
      
    wrong = 0
    if self.request.get("wrong"):
      wrong = 1
      # record of wrong answer
      wrong_db = Wrong()
      wrong_db.word = word
      wrong_db.reciteKey = objKey
      wrong_db.owner = user
      wrong_db.wrongText = self.request.get("answer")
      wrong_db.put()
    
    #result = db.get(objKey)  #Result(reciteKey=objKey, owner=user)
    results = db.GqlQuery("SELECT * FROM Result WHERE owner = :1 and reciteKey= :2 and word= :3", user, objKey, word )
    result = results.get()
    if result:
      result.rightCount = int(result.rightCount) + right
      result.wrongCount = int(result.wrongCount) + wrong
    else:
      result = Result()
      result.word = word
      result.reciteKey = objKey
      result.owner     = user
      result.rightCount = 0
      result.wrongCount = 0
      result.rightCount = result.rightCount + right
      result.wrongCount = result.wrongCount + wrong
    
    result.put()
    #self.redirect('/?w=' + result.word )

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/add', addWord),
                                      ('/record', recordResult)
                                      ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()