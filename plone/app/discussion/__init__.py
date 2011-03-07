# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

import plone.app.vocabularies.types

PloneAppDiscussionMessageFactory = MessageFactory('plone.app.discussion')

from plone.app.discussion.compatibility import \
    PLONE_APP_VOCABULARIES_2_1_AND_UP

# Plone 4.0 still uses P.A.V. older than 2.1. These versions still blacklist
# Discussion Items from the catalog. Thats not the expected behaviour then
# using p.a.d.

if not PLONE_APP_VOCABULARIES_2_1_AND_UP:
    new_bad_types = list(plone.app.vocabularies.types.BAD_TYPES)
    if 'Discussion Item' in new_bad_types:
        new_bad_types.remove("Discussion Item")
    plone.app.vocabularies.types.BAD_TYPES = new_bad_types
