# Copyright 2015 Google Inc.
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

import re

from configtest import *
from flaky import flaky
import pytest
import pymysql

# Mark all test cases in this class as flaky, so that if errors occur they
# can be retried. This is useful when databases are temporarily unavailable.
@flaky(rerun_filter=flaky_filter)
# Tell pytest to use both the app and model fixtures for all test cases.
# This ensures that configuration is properly applied and that all database
# resources created during tests are cleaned up. These fixtures are defined
# in conftest.py
@pytest.mark.usefixtures('app', 'model')
class TestCrudActions(object):

    def test_add(self, app, model):
        for n in TEST_IDS:
            model.Artist.query.filter_by(id = ('id' + str(n))).delete()

        beforeAmount = model.Artist.query.count()

        for n in TEST_IDS:
            obj = dict()
            obj['id'] = 'id' + str(n);
            obj['spotify_uri'] = 'id' + str(n);
            obj['name'] = 'name' + str(n);
            obj['image_url'] = 'img' + str(n);
            obj['followers'] = n
            obj['popularity'] = n
            model.create_artist(obj)

        afterAmount = model.Artist.query.count()
        assert afterAmount > beforeAmount

        for n in TEST_IDS:
            model.Artist.query.filter_by(id = ('id' + str(n))).delete()

        model.db.session.commit()

    def test_add_invalid(self, app, model):
        beforeAmount = model.Artist.query.count()

        obj = dict()
        obj['id'] = 'id'
        obj['spotify_uri'] = 'id'
        obj['name'] = 'name'
        obj['image_url'] = 'img'
        obj['followers'] = 'invalid_property'
        obj['popularity'] = 0

        with pytest.raises(Exception) as excinfo:
            model.create_artist(obj)
        model.db.session.rollback()

        afterAmount = model.Artist.query.count()
        assert afterAmount == beforeAmount

    # def test_edit(self, app, model):
    #     existing = model.create({'title': "Temp Title"})
    #
    #     with app.test_client() as c:
    #         rv = c.post(
    #             '/books/%s/edit' % existing['id'],
    #             data={'title': 'Updated Title'},
    #             follow_redirects=True)
    #
    #     assert rv.status == '200 OK'
    #     body = rv.data.decode('utf-8')
    #     assert 'Updated Title' in body
    #     assert 'Temp Title' not in body
    #
    # def test_delete(self, app, model):
    #     existing = model.create({'title': "Temp Title"})
    #
    #     with app.test_client() as c:
    #         rv = c.get(
    #             '/books/%s/delete' % existing['id'],
    #             follow_redirects=True)
    #
    #     assert rv.status == '200 OK'
    #     assert not model.read(existing['id'])
