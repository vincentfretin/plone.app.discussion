# -*- coding: utf-8 -*-

import unittest

from plone.mocktestcase import MockTestCase

from zope.component import createObject

from Products.PloneTestCase.ptc import PloneTestCase
from plone.app.discussion.tests.layer import DiscussionLayer
from Products.CMFCore.utils import getToolByName

from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.conversation import Conversation
from plone.app.discussion.comment import Comment

from plone.app.discussion.browser.comments import AjaxCommentLoad

try:
    # These exist in new versions, but not in the one that comes with Zope 2.10.
    from BTrees.LOBTree import LOBTree
except ImportError: # pragma: no cover
    from BTrees.OOBTree import OOBTree as LOBTree # pragma: no cover

COMMENT_COUNT = 50


class AjaxLoadTest(MockTestCase):

    def setUp(self):
        context_mock = self.mocker.mock()
        request_mock = self.mocker.mock()
        conversation = Conversation()
        conversation._children = LOBTree()
        for i in range(COMMENT_COUNT):
            comment = Comment()
            #comment = self.mocker.mock('plone.Comment')
            #comment.in_reply_to = 0
            comment.text = 'Comment %i text' % i
            conversation.addComment(comment)
        self.context_mock = context_mock
        self.request_mock = request_mock
        self.replay()
        
    def test_ajax_full_view(self):
        full_view = AjaxCommentLoad(self.context_mock, self.request_mock)
        replies = full_view.get_replies()
        self.assertEqual(len(tuple(replies)), COMMENT_COUNT)

    def test_ajax_load_batch_view(self):
        batch_view = AjaxCommentLoad(self.context_mock, self.request_mock)
        replies = batch_view.get_replies(start=0, size=10)
        self.assertEqual(len(tuple(replies)), 10)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
