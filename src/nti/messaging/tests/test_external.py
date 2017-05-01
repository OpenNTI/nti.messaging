#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_entries

import unittest

from zope import interface

from zope.security.interfaces import IPrincipal

from nti.coremetadata.interfaces import system_user

from nti.externalization.externalization import to_external_object

from nti.messaging.model import SystemMessage
from nti.messaging.model import ReceivedMessage
from nti.messaging.model import PeerToPeerMessage

from nti.messaging.tests import SharedConfiguringTestLayer


@interface.implementer(IPrincipal)
class MockPrincipal(object):

    title = description = u''

    def __init__(self, pid):
        self.id = pid


class TestExternal(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_message(self):
        message = PeerToPeerMessage(body=[u'bleach'],
                                    To=[MockPrincipal(u'azien@bleach.org')],
                                    From=MockPrincipal(u'ichigo@bleach.org'),
                                    Subject=u'Bankai')
        ext_obj = to_external_object(message)
        assert_that(ext_obj,
                    has_entries('body', [u'bleach'],
                                'From', u'ichigo@bleach.org',
                                'To', [u'azien@bleach.org'],
                                'Date', is_not(none()),
                                'Class', 'PeerToPeerMessage',
                                'Subject', u'Bankai',
                                'MimeType', 'application/vnd.nextthought.messaging.peertopeermessage'))

        message = SystemMessage(body=[u'bleach'],
                                To=[MockPrincipal(u'rukia@bleach.org')],
                                From=system_user,
                                Subject=u'Shikai')
        ext_obj = to_external_object(message)
        assert_that(ext_obj,
                    has_entries('body', [u'bleach'],
                                'From', u'zope.security.management.system_user',
                                'To', [u'rukia@bleach.org'],
                                'Date', is_not(none()),
                                'Class', 'SystemMessage',
                                'Subject', u'Shikai',
                                'MimeType', 'application/vnd.nextthought.messaging.systemmessage'))

        message = ReceivedMessage(Message=message)
        message.mark_viewed(should_notify=False)
        message.mark_replied_to(should_notify=False)
        ext_obj = to_external_object(message)
        assert_that(ext_obj,
                    has_entries('ViewDate', is_not(none()),
                                'ReplyDate', is_not(none()),
                                'Class', 'ReceivedMessage',
                                'MimeType', 'application/vnd.nextthought.messaging.receivedmessage',
                                'Message', is_not(none())))
