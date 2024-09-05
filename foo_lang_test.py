# Student Name   :  Win Htaik Aung
# Student Number :  0944750
# Course Name    :  Python Programming
# Course Code    :  CSD-1233
# Project Title  :  Mini-Lisp Interpreter

import pytest
from foo_lang import parse, eval, Env, standard_env, Procedure, tokenize

# Create a fresh environment for each test


@pytest.fixture
def env():
    return standard_env()


def test_tokenize():
    assert tokenize("(+ 1 2)") == ['(', '+', '1', '2', ')']
    assert tokenize("(define (square x) (* x x))") == [
        '(', 'define', '(', 'square', 'x', ')', '(', '*', 'x', 'x', ')', ')']
    assert tokenize("(if (> x 10) (print 'big) (print 'small))") == [
        '(', 'if', '(', '>', 'x', '10', ')', '(', 'print', "'big", ')', '(', 'print', "'small", ')', ')']
    assert tokenize("(quote (1 2 3))") == [
        '(', 'quote', '(', '1', '2', '3', ')', ')']
    assert tokenize("'(1 2 3)") == ["'", '(', '1', '2', '3', ')']


def test_lambda_expression():
    expected = ['lambda', ['x'], ['+', 'x', 1]]
    assert parse("(lambda (x) (+ x 1))") == expected


def test_function_definition():
    expected = ['define', ['square', 'x'], ['*', 'x', 'x']]
    assert parse("(define (square x) (* x x))") == expected


def test_if_expression():
    expected = ['if', ['>', 'x', 10], ['print', "'large"], ['print', "'small"]]
    assert parse("(if (> x 10) (print 'large) (print 'small))") == expected


def test_arithmetic_operations(env):
    assert eval(parse("(+ 1 2)"), env) == 3
    assert eval(parse("(- 5 3)"), env) == 2
    assert eval(parse("(* 4 2)"), env) == 8
    assert eval(parse("(/ 10 2)"), env) == 5


def test_nested_arithmetic(env):
    assert eval(parse("(+ (* 2 3) (- 10 5))"), env) == 11


def test_variable_definition_and_reference(env):
    eval(parse("(define x 10)"), env)
    assert eval(parse("x"), env) == 10
    assert eval(parse("(+ x 5)"), env) == 15


def test_if_statement(env):
    assert eval(parse("(if (> 5 3) 1 2)"), env) == 1
    assert eval(parse("(if (< 5 3) 1 2)"), env) == 2


def test_lambda_and_function_call(env):
    eval(parse("(define square (lambda (x) (* x x)))"), env)
    assert eval(parse("(square 4)"), env) == 16


def test_recursion(env):
    eval(parse("(define factorial (lambda (n) (if (= n 0) 1 (* n (factorial (- n 1))))))"), env)
    assert eval(parse("(factorial 5)"), env) == 120


def test_list_operations(env):
    assert eval(parse("(car (list 1 2 3))"), env) == 1
    assert eval(parse("(cdr (list 1 2 3))"), env) == [2, 3]
    assert eval(parse("(cons 1 (list 2 3))"), env) == [1, 2, 3]


def test_higher_order_functions(env):
    eval(parse("(define double (lambda (x) (* x 2)))"), env)
    result = eval(parse("(map double (list 1 2 3))"), env)
    assert list(result) == [2, 4, 6]


def test_quote(env):
    assert eval(parse("(quote (1 2 3))"), env) == [1, 2, 3]


def test_set(env):
    eval(parse("(define x 1)"), env)
    eval(parse("(set! x 2)"), env)
    assert eval(parse("x"), env) == 2
