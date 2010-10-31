# -*- coding: utf-8 -*-

import unittest

from OFS.SimpleItem import SimpleItem

from zope.component import createObject
from zope.interface import implements
from zope.component import provideAdapter
from zope.annotation.interfaces import IAnnotatable, IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.attribute import AttributeAnnotations
from zope.publisher.browser import TestRequest

from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.conversation import Conversation, ANNOTATION_KEY
from plone.app.discussion.conversation import conversationAdapterFactory
from plone.app.discussion.comment import Comment
from plone.app.discussion.browser.comments import AjaxCommentLoad

try:
    # These exist in new versions, but not in the one that comes with Zope 2.10.
    from BTrees.LOBTree import LOBTree
except ImportError: # pragma: no cover
    from BTrees.OOBTree import OOBTree as LOBTree # pragma: no cover

COMMENT_COUNT = 50

class WorkflowMock(object):
    def getInfoFor(self, obj, info):
        return 'published'

class ContextMock(SimpleItem):
    implements(IAttributeAnnotatable, IAnnotatable)
    portal_workflow = WorkflowMock()


class AjaxLoadTest(unittest.TestCase):

    def setUp(self):
        context_mock = ContextMock()
        request_mock = TestRequest()
        conversation = Conversation()
        conversation._children = LOBTree()
        provideAdapter(AttributeAnnotations)
        provideAdapter(conversationAdapterFactory)
        IAnnotations(context_mock)[ANNOTATION_KEY] = conversation
        for i in range(COMMENT_COUNT):
            comment = Comment()
            comment.text = 'Comment %i text' % i
            conversation.addComment(comment)
        self.context_mock = context_mock
        self.request_mock = request_mock

    def test_ajax_full_view(self):
        view = AjaxCommentLoad(self.context_mock, self.request_mock)
        replies = view.get_replies()
        self.assertEqual(len(tuple(replies)), COMMENT_COUNT)

    def test_ajax_load_batch_view(self):
        view = AjaxCommentLoad(self.context_mock, self.request_mock)
        replies = tuple(view.get_replies(start=0, size=10))
        self.assertEqual(len(replies), 10)
        # Check that those are really the first 10 comments
        for i in range(10):
            text = replies[i]['comment'].text
            it_should_be = "Comment %i text" % i
            self.assertEqual(text, it_should_be)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
