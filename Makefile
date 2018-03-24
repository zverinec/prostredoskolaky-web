TEMPLATES=$(wildcard templates/*.html)
GENERATORS=$(wildcard scr/*.py)
ACTIVITIES=activities.csv
GDRIVE_DATA=$(wildcard static/drive-data/drive-data/*)
STATIC_DATA=$(wildcard static/drive-data/*)

ALL_FILES=index.html matematika.html informatika.html fyzika.html chemie.html \
          biologie.html geologie.html ekonomie.html
ALL=$(patsubst %,build/%,$(ALL_FILES))

all: $(ALL)

build/index.html: $(TEMPLATES) $(GENERATORS) $(ACTIVITIES) $(GDRIVE_DATA) $(STATIC_DATA)
	./scr/generator.py -o $@ -a $(ACTIVITIES)

build/%.html: $(TEMPLATES) $(GENERATORS) $(ACTIVITIES) $(GDRIVE_DATA) $(STATIC_DATA)
	./scr/generator.py -o $@ -a $(ACTIVITIES) -f $(patsubst build/%.html,%,$@)

clean:
	rm -r $(ALL)

.PHONY: all clean
