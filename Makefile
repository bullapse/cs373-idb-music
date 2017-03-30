get_artist:
	python3.5 -c 'import getSpotify; print(getSpotify.get_artist())'

get_album:
	python3.5 -c 'import getSpotify; print(getSpotify.get_album())'

get_track:
	python -c 'import getSpotify; print(getSpotify.get_track())'

IDB1.log:
	git log > IDB1.log

IDB1.html:
	pydoc3 -w ./app/model.py
