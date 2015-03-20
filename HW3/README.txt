== General Notes ==

I create an additional data strcture on top of a singly-linked list to called PostingsListNode and PostingsList to contian the skip pointers information in each node if there is any. cPickle.dump is used to generate both dictionary and postings file. For each term in the dictionary, it contains a pointer index in the postings file that should be seekd to in order to obtain the beginng of the respective postings skiplist. This allows to read in only the necessary posting list.

After parsing queries, based on the frequency information, I try to estimate the query length (maximum possbile result set) of each query subclause.

== Files included with this submission ==
index.py              - Entry point for building index
search.py             - Entry point for query searches
search_index.py       - Class for a SearchIndex object which will perform and generate search results
querytree.py          - Entity class for QueryTree
boolean_operator.py   - Entity class for operators
Makefile              - To automate tasks
postings_list.py      - A linked list with additional attribute to contain pointers for skips
postings_list_node.py - Class for individual node of the skip list
dictionary.txt        - Pickle dump of dictionary
postings.txt          - Pickle dump of postings list

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

A lot of ideas from generation infix, prefix, postfix expression although not explicily converting in my code
http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html

Discussion posts from IVLE forum.
