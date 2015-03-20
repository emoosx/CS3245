DOC=~/nltk_data/corpora/reuters/training
DICT=dictionary.txt
POSTINGFILE=postings.txt

QUERIES=queries/query.txt
JIN_QUERIES=queries/jin_query.txt
OUTPUT=output.txt
TEMP=temp/

index: index.py
	python index.py -i $(DOC) -d $(DICT) -p $(POSTINGFILE)

search: search.py $(QUERIES)
	python search.py -d $(DICT) -p $(POSTINGFILE) -q $(QUERIES) -o $(OUTPUT)

search_jin: search.py $(JIN_QUERIES)
	python search.py -d $(DICT) -p $(POSTINGFILE) -q $(JIN_QUERIES) -o $(OUTPUT)

clean:
	if [ -d "$(TEMP)" ]; then \
	    rm -rf $(TEMP); \
	fi
	rm *.pyc

test:
	nosetests

build:
	rm -rf *.zip
	if [ -d A0105860L/ ]; then \
	    rm -rf A0105860L/ ; \
	fi
	mkdir A0105860L
	git archive master | tar -x -C A0105860L
	rm -rf A0105860L/__init__.py
	rm -rf A0105860L/FILE_COUNT
	rm -rf A0105860L/queries
	rm -rf A0105860L/output.txt
	zip -r ~/Desktop/A0105860L.zip A0105860L
	rm -r A0105860L


all: clean index search
