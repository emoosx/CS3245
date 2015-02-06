LM_FILE=build_test_LM.py
INPUT_TRAIN=input.train.txt
INPUT_TEST=input.test.txt
INPUT_PREDICT=input.predict.txt
INPUT_CORRECT=input.correct.txt

INPUT_SHORT=input.short.txt
INPUT_TEST_SHORT=input.test.short.txt
INPUT_TEST_PREDICT=input.test.predict.txt

all:	build_predict eval

build_predict:	build_test_LM.py
	python $(LM_FILE) -b $(INPUT_TRAIN) -t $(INPUT_TEST) -o $(INPUT_PREDICT)

test:	build_test_LM.py
	python $(LM_FILE) -b $(INPUT_SHORT) -t $(INPUT_TEST_SHORT) -o $(INPUT_TEST_PREDICT)

eval: eval.py
	python eval.py $(INPUT_PREDICT) $(INPUT_CORRECT)

cleanup:
	rm -rf A0105860L
	rm *.test.*.txt input.short.txt

zip:
	zip -r -X A0105860L.zip $(LM_FILE) ESSAY.txt eval.py Makefile README.txt

