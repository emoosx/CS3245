DOC=~/nltk_data/corpora/reuters/training
DICT=dictionary.txt
POSTINGFILE=postings.txt

QUERIES=query.txt
OUTPUT=output.txt
TEMP=temp/

all: clean index search

index: index.py
	python index.py -i $(DOC) -d $(DICT) -p $(POSTINGFILE)

search: search.py
	python search.py -d $(DICT) -p $(POSTINGFILE) -q $(QUERIES) -o $(OUTPUT)

clean:
	if [ -d "$(TEMP)" ]; then \
	    rm -rf $(TEMP); \
	fi
	rm *.pyc

test:
	nosetests
