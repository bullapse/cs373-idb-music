FILES :=                        \
	.travis.yml					\
	apiary.apib					\
	app.yaml					\
	main.py						\
	appengine_config.py			\
	getSpotify.py				\
	model.html					\
	requirements.txt			\
	ULM.pdf						\
	vendor.py


ifeq ($(shell uname), Darwin)          # Apple
	PYTHON   := python3.5
	PIP      := pip3.5
	PYLINT   := pylint
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
	PYTHON   := python3.5
	PIP      := pip3.5
	PYLINT   := pylint
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3
	AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
	PYTHON   := python3.5
	PIP      := pip3.5
	PYLINT   := pylint
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
else ifeq ($(shell whoami), sbull)     # Spencer
	PYTHON   := python3.5
	PIP      := pip3
	PYLINT   := pylint
	COVERAGE := coverage
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
else                                   # UTCS
	PYTHON   := python3.5
	PIP      := pip3
	PYLINT   := pylint3
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
endif

.pylintrc:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

get_artist:
	$(PYTHON) -c 'import getSpotify; print(getSpotify.get_artist())'

get_album:
	$(PYTHON) -c 'import getSpotify; print(getSpotify.get_album())'

get_track:
	$(PYTHON) -c 'import getSpotify; print(getSpotify.get_track())'

IDB1.log:
	git log > IDB1.log

IDB1.html:
	$(PYDOC) -w ./notspotify/model.py

check:
	@not_found=0;                                 \
	for i in $(FILES);                            \
	do                                            \
		if [ -e $$i ];                            \
		then                                      \
			echo "$$i found";                     \
		else                                      \
			echo "$$i NOT FOUND";                 \
			not_found=`expr "$$not_found" + "1"`; \
		fi                                        \
	done;                                         \
	if [ $$not_found -ne 0 ];                     \
	then                                          \
		echo "$$not_found failures";              \
		exit 1;                                   \
	fi;                                           \
	echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__

config:
	git config -l

format:
	$(AUTOPEP8) -i main.py
	$(AUTOPEP8) -i getSpotify.py
	$(AUTOPEP8) -i appengine_config.py
	$(AUTOPEP8) -i notspotify/model.py
	$(AUTOPEP8) -i notspotify/tests.py

scrub: clean
	rm -f model.html
	rm -f IDB1.log

test_not_spotify:
	-$(PYLINT) main.py
	-$(PYLINT) getSpotify.py
	-$(PYLINT) appengine_config.py
	-$(PYLINT) notspotify/model.py
	-$(PYLINT) notspotify/tests.py
	$(COVERAGE) run    --branch notspotify/tests.py > TestNotSpotify.tmp 2>&1
	$(COVERAGE) report -m                      >> TestNotSpotify.tmp
	cat TestCollatz.tmp

run:
	$(PYTHON) main.py

test: IDB1.html IDB1.log test_not_spotify check
