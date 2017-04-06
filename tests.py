import unittest
import flask_testing
import notspotify
import config


def check_is_sorted(page, val):
    l = list(map(lambda e: e[val], page));
    return sorted(l) == l

#The tests use the GCP DB so we have to make sure to clean up for any tests that we write
class MyTest(flask_testing.TestCase):

    model = None

    def create_app(self):
        # pass in test configuration
        return notspotify.create_app(config, testing=True)

    def setUp(self):
        global model
        model = notspotify.get_model()
        #clean up test objects in db before running
        model.Artist.query.filter_by(id = 'id').delete()
        model.Album.query.filter_by(id = 'id').delete()
        model.Track.query.filter_by(id = 'id').delete()

    def tearDown(self):
        #clean up test objects in db after tests
        model.Artist.query.filter_by(id = 'id').delete()
        model.Album.query.filter_by(id = 'id').delete()
        model.Track.query.filter_by(id = 'id').delete()

    def test_add_artist1(self):
        model.Artist.query.filter_by(id = 'id').delete()

        beforeCount = model.Artist.query.count()

        obj = dict()
        obj['id'] = 'id'
        obj['spotify_uri'] = 'id'
        obj['name'] = 'name'
        obj['image_url'] = 'img'
        obj['followers'] = 1
        obj['popularity'] = 1
        model.create_artist(obj)

        afterCount = model.Artist.query.count()
        self.assertEqual(afterCount, beforeCount + 1)

        model.Artist.query.filter_by(id = 'id').delete()
        model.db.session.commit()

    def test_add_artist2(self):
        model.Artist.query.filter_by(id = 'id').delete()

        obj = dict()
        obj['id'] = 'id'
        obj['spotify_uri'] = 'id'
        obj['name'] = 'name'
        obj['image_url'] = 'img'
        obj['followers'] = 1
        obj['popularity'] = 1
        model.create_artist(obj)

        result = list(map(model.from_sql, model.Artist.query.filter_by(id = 'id')))

        self.assertEqual(result[0]['name'], 'name')

        model.Artist.query.filter_by(id = 'id').delete()
        model.db.session.commit()

    def test_add_artist_invalid(self):
        beforeCount = model.Artist.query.count()

        obj = dict()
        obj['id'] = 'id';
        obj['spotify_uri'] = 'id';
        obj['name'] = 'name';
        obj['image_url'] = 'img';
        obj['followers'] = 'invalid'
        obj['popularity'] = 1
        try:
            model.create_artist(obj)
        except Exception:
            pass
        model.db.session.rollback()

        afterCount = model.Artist.query.count()
        self.assertEqual(afterCount, beforeCount)

    def test_add_artist_empty(self):
        beforeCount = model.Artist.query.count()

        obj = dict()
        obj['id'] = 'id'
        try:
            model.create_artist(obj)
        except Exception:
            pass
        model.db.session.rollback()

        afterCount = model.Artist.query.count()
        self.assertEqual(afterCount, beforeCount)


    def test_rest_artist_paging1(self):
        page = model.list_artists()

        self.assertEqual(len(page[0]), 10)
        self.assertEqual(page[1], 10)

    def test_rest_artist_paging2(self):
        page = model.list_artists(cursor=10)

        self.assertEqual(len(page[0]), 10)
        self.assertEqual(page[1], 20)

    def test_rest_artist_sort_name(self):
        page = model.list_artists(sort_by='name')
        self.assertTrue(check_is_sorted(page[0], 'name'))

    def test_rest_artist_sort_followers(self):
        page = model.list_artists(sort_by='followers')
        self.assertTrue(check_is_sorted(page[0], 'followers'))

    def test_rest_artist_sort_popularity(self):
        page = model.list_artists(sort_by='popularity')
        self.assertTrue(check_is_sorted(page[0], 'popularity'))

    def test_add_album1(self):

        model.Album.query.filter_by(id = 'id').delete()

        beforeCount = model.Album.query.count()

        obj = dict()
        obj['id'] = 'id'
        obj['name'] = 'name'
        obj['image_url'] = 'img'
        obj['release_date'] = '2012-3-04'
        obj['popularity'] = 50
        obj['number_of_tracks'] = 10
        model.create_album(obj)

        afterCount = model.Album.query.count()
        self.assertEqual(afterCount, beforeCount + 1)

        model.Album.query.filter_by(id = 'id').delete()
        model.db.session.commit()

    def test_add_album2(self):
        model.Album.query.filter_by(id = 'id').delete()

        obj = dict()
        obj['id'] = 'id'
        obj['name'] = 'name'
        obj['image_url'] = 'img'
        obj['release_date'] = '2012-3-04'
        obj['popularity'] = 50
        obj['number_of_tracks'] = 10
        model.create_album(obj)

        result = list(map(model.from_sql, model.Album.query.filter_by(id = 'id')))

        self.assertEqual(result[0]['number_of_tracks'],10)

        model.Album.query.filter_by(id = 'id').delete()
        model.db.session.commit()

    def test_add_album_invalid(self):
        beforeCount = model.Album.query.count()

        obj = dict()
        obj['id'] = 'id'
        obj['name'] = 'name'
        obj['image_url'] = 'img'
        obj['release_date'] = '2012-3-04'
        obj['popularity'] = "i'm pretty popular"
        obj['number_of_tracks'] = 10
        try:
            model.create_album(obj)
        except Exception:
            pass
        model.db.session.rollback()

        afterCount = model.Album.query.count()
        self.assertEqual(afterCount, beforeCount)

    def test_add_album_empty(self):
        beforeCount = model.Album.query.count()

        obj = dict()
        obj['id'] = 'id';
        try:
            model.create_album(obj)
        except Exception:
            pass
        model.db.session.rollback()

        afterCount = model.Album.query.count()
        self.assertEqual(afterCount, beforeCount)

    def test_rest_album_paging1(self):
        page = model.list_albums()

        self.assertEqual(len(page[0]), 10)
        self.assertEqual(page[1], 10)

    def test_rest_album_paging2(self):
        page = model.list_albums(cursor=10)

        self.assertEqual(len(page[0]), 10)
        self.assertEqual(page[1], 20)

    def test_add_track1(self):
        model.Track.query.filter_by(id = 'id').delete()

        beforeCount = model.Track.query.count()

        obj = dict()
        obj['id'] = 'id'
        obj['name'] = 'name'
        obj['spotify_uri'] = 'id'
        obj['explicit'] = True
        obj['popularity'] = 50
        obj['runtime'] = 1000000
        obj['preview_url'] = 'test.mp3'
        model.create_track(obj)

        afterCount = model.Track.query.count()
        self.assertEqual(afterCount, beforeCount + 1)

        model.Track.query.filter_by(id = 'id').delete()
        model.db.session.commit()

    def test_add_track2(self):
        model.Track.query.filter_by(id = 'id').delete()

        obj = dict()
        obj['id'] = 'id'
        obj['name'] = 'name'
        obj['spotify_uri'] = 'id'
        obj['explicit'] = True
        obj['popularity'] = 50
        obj['runtime'] = 1000000
        obj['preview_url'] = 'test.mp3'
        model.create_track(obj)

        result = list(map(model.from_sql, model.Track.query.filter_by(id = 'id')))

        self.assertTrue(result[0]['explicit'])

        model.Track.query.filter_by(id = 'id').delete()
        model.db.session.commit()

    def test_add_track_invalid(self):
        beforeCount = model.Track.query.count()

        obj = dict()
        obj['id'] = 'id'
        obj['name'] = 'name'
        obj['spotify_uri'] = 'id'
        obj['explicit'] = True
        obj['popularity'] = 50
        obj['runtime'] = "it's a pretty long song"
        obj['preview_url'] = 'test.mp3'
        try:
            model.create_track(obj)
        except Exception:
            pass
        model.db.session.rollback()

        afterCount = model.Track.query.count()
        self.assertEqual(afterCount, beforeCount)

    def test_add_track_empty(self):
        beforeCount = model.Track.query.count()

        obj = dict()
        obj['id'] = 'id';
        try:
            model.create_track(obj)
        except Exception:
            pass
        model.db.session.rollback()

        afterCount = model.Track.query.count()
        self.assertEqual(afterCount, beforeCount)

    def test_rest_track_paging1(self):
        page = model.list_tracks()

        self.assertEqual(len(page[0]), 10)
        self.assertEqual(page[1], 10)

    def test_rest_track_paging2(self):
        page = model.list_tracks(cursor=10)

        self.assertEqual(len(page[0]), 10)
        self.assertEqual(page[1], 20)

if __name__ == '__main__':
    unittest.main()
