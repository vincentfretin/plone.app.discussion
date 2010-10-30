from Products.PloneTestCase.ptc import PloneTestCase
from plone.app.discussion.tests.layer import DiscussionLayer
from Products.CMFCore.utils import getToolByName


from plone.app.discussion.interfaces import IConversation

from plone.app.discussion.browser.comments import AjaxCommentLoad

from zope.component import createObject
import unittest


class AjaxLoadTest(PloneTestCase):

    layer = DiscussionLayer

    def afterSetUp(self):
        # First we need to create some content.
        self.loginAsPortalOwner()
        typetool = self.portal.portal_types
        typetool.constructContent('Document', self.portal, 'doc1')
        self.typetool = typetool
        self.portal_discussion = getToolByName(self.portal, 
                                               'portal_discussion', 
                                               None)
        # we publish it
        wft = getToolByName(self.portal, 'portal_workflow')
        wft.doActionFor(self.portal.doc1, 'publish')
        # and enable discussion on it
        self.portal_discussion.overrideDiscussionFor(self.portal.doc1, True)
        # Create a very long conversation with hundreds of comments
        # so that we can start a ZServer and fiddle with firebug
        conversation = IConversation(self.portal.doc1)
        for i in range(100):
            comment = createObject('plone.Comment')
            comment.title = 'Comment %i' % i
            comment.text = 'Comment %i text' % i
            conversation.addComment(comment)

    def test_ajax_load_view(self):
        view = AjaxCommentLoad(self.portal.doc1, self.app.REQUEST)

        #result = view()
    def xtest_ajax_load(self):
        '''
        This is not a "real" test method.
        I'm using it to develop ajax loading of comments.
        I'll converti it to a Selenium test soon.
        This should be a starting point: https://weblion.psu.edu/svn/weblion/weblion/assessmentmanagement.core/trunk/assessmentmanagement/core/selenium/testSelenium.py

        This too: http://pastebin.com/Dnx4WSMk
        '''
        import Testing
        host, port = Testing.ZopeTestCase.utils.startZServer()
        obj_path = self.portal.doc1.virtual_url_path()
        url = "http://%s:%i/%s" % (host, port, obj_path)
        print
        print url
        import transaction
        # The next line should NOT be committed uncommented
        #transaction.commit() # I know I shouldn't do this, but this way it works

        # Fire your favourite debugger (pdb obviously),
        # open Firebug. and start coding!
        # XXX this should become a real test
        

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

