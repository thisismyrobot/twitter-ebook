""" Markov-chained twitter fun, in a Google App Engine app.
"""
import ebook_client
import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        """ Do an update.
        """
        ebook_client.update()


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=False)
