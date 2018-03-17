TEMPLATES=$(wildcard templates/*.html)
GENERATORS=$(wildcard src/*.py)
ACTIVITIES=activities.csv

ALL_FILES=index.html matematika.html informatika.html fyzika.html chemie.html \
          biologie.html geologie.html
ALL=$(patsubst %,build/%,$(ALL_FILES))

all: $(ALL)

build/index.html: $(TEMPLATES) $(GENERATORS) $(ACTIVITIES)
	./scr/generator.py -o $@ -a $(ACTIVITIES)

build/%.html: $(TEMPLATES) $(GENERATORS) $(ACTIVITIES)
	./scr/generator.py -o $@ -a $(ACTIVITIES) -f $(patsubst build/%.html,%,$@)

clean:
	rm -r $(ALL)

.PHONY: all clean
