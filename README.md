# README

## Executing the file
Please proceed to the foo_lang.py

```
python foo_lang.py
```

## Sample lisp syntax for play around

```
(define (square x) (* x x))

(square 3)

(define factorial (lambda (n) (if (= n 0) 1 (* n (factorial (- n 1))))))
```


## Running the test

Run `pip install -r requirements.txt`

```
pytest foo_lang_test.py
```
