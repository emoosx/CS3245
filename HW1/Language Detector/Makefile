LM_FILE=build_test_LM.py
INPUT_TRAIN=input.train.txt
INPUT_SHORT=input.short.txt
INPUT_TEST=input.test.txt
INPUT_PREDICT=input.predict.txt

all:	build_predict

build_predict:	build_test_LM.py
	python $(LM_FILE) -b $(INPUT_SHORT) -t $(INPUT_TEST) -o $(INPUT_PREDICT)
