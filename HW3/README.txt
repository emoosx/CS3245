This is the README file for A0105860L's submission

== General Notes about this assignment ==
The code of this assignment based on top of HW2. The tuple in each postings follows the example shown on the website, plus an additional field for weightage of the term in the document. That is done by making another pass of the dictionary and calculating the log_tfs of the term.

Moreover, I store the total length of the document in a file called FILE_COUNT which I can read and use it back from SearchIndex to calculate idf of query terms. I follow the algorithm in the lecture notes for the computation of cosine scores. And the score results are passed into a heap (which makes use of python's built in module `heapq`). However, since heapq is min-heap, the scores are inverted when popping into the heap in order to simulate a max-heap. (Surprisingly that is the standard practice unless you implement your own heap class or override the comparator or `__ltr__` of heapq)

== Files included with this submission ==

ESSAY.txt             - Answers to the Essay Questions
README.txt            - This file
dictionary.txt        - Pickle dump of dictionary
postings.txt          - Pickle dump of postings list
Makefile              - To automate tasks for development
index.py              - Indexing
search.py             - Entry point for query searches
search_index.py       - Class for a SearchIndex which will perform and generate search results


== Statement of individual work ==

Please initial one of the following statements.

[I] I, A0105860L, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

== References ==

Python documentation in general and particularly on `pickle` and file I/O operations
http://stackoverflow.com/questions/7219511/whats-the-difference-between-io-open-and-os-open-on-python
http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python

This stackoverflow post which makes the cosine similarity concept really clear
http://stackoverflow.com/questions/1746501/can-someone-give-an-example-of-cosine-similarity-in-very-simple-graphical-way

PyMOTW post on heapq
http://pymotw.com/2/heapq/

Discussion posts from IVLE forum.
