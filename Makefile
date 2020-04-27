TEMPLATES=$(wildcard templates/*.html)
SOC_TEMPLATES=$(wildcard templates/soc/*.html)
ACTIVITY_GENERATORS=$(wildcard scr/activity*.py) scr/util.py scr/config.py
SOC_GENERATORS=$(wildcard scr/soc*.py) scr/util.py scr/config.py
ACTIVITIES=activities.csv
SOC_TOPICS=soc_topics.csv
SOC_GARANTS=soc_garants.csv
GDRIVE_DATA=$(wildcard static/drive-data/*)
STATIC_DATA=$(wildcard static/*)

ALL_FILES=index.html matematika.html informatika.html fyzika.html chemie.html \
          biologie.html vedy-o-zemi.html ekonomie.html soc/index.html
ALL=$(patsubst %,build/%,$(ALL_FILES))

all: $(ALL)

build/index.html: $(TEMPLATES) $(ACTIVITY_GENERATORS) $(ACTIVITIES) $(GDRIVE_DATA) $(STATIC_DATA)
	./scr/activity_generator.py -o $@ -a $(ACTIVITIES)

build/%.html: $(TEMPLATES) $(ACTIVITY_GENERATORS) $(ACTIVITIES) $(GDRIVE_DATA) $(STATIC_DATA)
	./scr/activity_generator.py -o $@ -a $(ACTIVITIES) -f $(patsubst build/%.html,%,$@)

build/soc/%.html: $(SOC_TEMPLATES) $(SOC_GENERATORS) $(SOC_TOPICS) $(SOC_GARANTS)
	./scr/soc_generator.py -o $@ -t $(SOC_TOPICS) -g $(SOC_GARANTS)

clean:
	rm -r $(ALL)

check:
	flake8 scr/*.py

.PHONY: all clean check
