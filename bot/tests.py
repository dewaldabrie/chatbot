# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
class TestEngageView(TestCase):

    def test_response(self):
        response = self.client.get('/')
        self.assertContains(response, 'Hello')