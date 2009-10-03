#!/usr/bin/env python

import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    self.response.out.write("""
          <form action="/sign" method="post">
            <div>Welcome!</div>
          </form>
        </body>
      </html>""")

class About(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    self.response.out.write("""
          <form action="/sign" method="post">
            <div>About!</div>
          </form>
        </body>
      </html>""")


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/about', About )
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
