TEMPLATES=$(wildcard templates/*.html)
SOC_TEMPLATES=$(wildcard templates/soc/*.html)
ACTIVITY_GENERATORS=$(wildcard scr/activity*.py) scr/util.py scr/config.py
SOC_GENERATORS=$(wildcard scr/soc*.py) scr/util.py scr/config.py
ACTIVITIES=data/activities.csv
SOC_TOPICS=$(wildcard data/soc_topics*.csv)
SOC_GARANTS=data/soc_garants.csv
GDRIVE_DATA=$(wildcard static/drive-data/*)
STATIC_DATA=$(wildcard static/*)

ALL_FILES=index.html matematika.html informatika.html fyzika.html chemie.html \
          biologie.html vedy-o-zemi.html ekonomie.html soc/index.html soc/all.html
ALL=$(patsubst %,build/%,$(ALL_FILES))
COMMA=,
EMPTY=
SPACE=$(EMPTY) $(EMPTY)

SOC_WITH_COMMAS=$(subst $(SPACE),$(COMMA),$(SOC_TOPICS))

all: $(ALL)

build/index.html: $(TEMPLATES) $(ACTIVITY_GENERATORS) $(ACTIVITIES) $(GDRIVE_DATA) $(STATIC_DATA) Makefile
	./scr/activity_generator.py -o $@ -a $(ACTIVITIES)

build/%.html: $(TEMPLATES) $(ACTIVITY_GENERATORS) $(ACTIVITIES) $(GDRIVE_DATA) $(STATIC_DATA) Makefile
	./scr/activity_generator.py -o $@ -a $(ACTIVITIES) -f $(patsubst build/%.html,%,$@)

build/soc/index.html: $(SOC_TEMPLATES) $(SOC_GENERATORS) $(SOC_TOPICS) $(SOC_GARANTS) data Makefile
	./scr/soc_generator.py -o $@ -t $(SOC_WITH_COMMAS) -g $(SOC_GARANTS) -s volno,obsazeno -m templates/soc/index.html

build/soc/all.html: $(SOC_TEMPLATES) $(SOC_GENERATORS) $(SOC_TOPICS) $(SOC_GARANTS) data Makefile
	LC_ALL=en_US.UTF-8 ./scr/soc_generator.py -o $@ -t $(SOC_WITH_COMMAS) -g $(SOC_GARANTS) \
		-s volno,obsazeno,ukončeno -m templates/soc/all.html

clean:
	rm -r $(ALL)

check:
	flake8 scr/*.py

.PHONY: all clean check
