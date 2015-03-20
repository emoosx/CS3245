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


all: clean index search
