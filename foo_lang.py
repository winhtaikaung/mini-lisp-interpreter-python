# Student Name   :  Win Htaik Aung
# Student Number :  0944750
# Course Name    :  Python Programming
# Course Code    :  CSD-1233
# Project Title  :  Mini-Lisp Interpreter

import operator as op


class Env(dict):
    """
    Environment with support for outer scopes.
    Implements a chain of nested dictionaries for variable lookup.
    """

    def __init__(self, parms=(), args=(), outer=None):
        """
        Initialize an environment.
        :param parms: List of parameter names
        :param args: List of argument values
        :param outer: Outer (enclosing) environment
        """
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """
        Find the innermost Env where var appears.
        :param var: Variable name to look up
        :return: The environment where var is defined
        :raises KeyError: If the variable is not found in any environment
        """
        return self if (var in self) else self.outer.find(var)


class Procedure(object):
    """
    A user-defined Scheme procedure.
    Represents a lambda function with its parameters, body, and defining environment.
    """

    def __init__(self, parms, body, env):
        """
        Initialize a Procedure.
        :param parms: List of parameter names
        :param body: The body of the procedure (Scheme expression)
        :param env: The environment in which the procedure was defined
        """
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        """
        Call the procedure with given arguments.
        :param args: Arguments to the procedure
        :return: Result of evaluating the procedure body
        """
        return eval(self.body, Env(self.parms, args, self.env))


def tokenize(chars):
    """
    Convert a string of characters into a list of tokens.
    :param chars: A string containing a Scheme expression
    :return: A list of tokens
    """
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    """
    Read a Scheme expression from a string.
    :param program: A string containing a Scheme expression
    :return: A Python representation of the Scheme expression
    """
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):
    """
    Read an expression from a sequence of tokens.
    :param tokens: A list of tokens
    :return: A Python representation of the Scheme expression
    :raises SyntaxError: If the tokens form an invalid expression
    """
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token):
    """
    Convert a token to a Python type.
    :param token: A string token
    :return: An int, float, or string depending on the token
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


def standard_env():
    """
    Create an environment with some Scheme standard procedures.
    :return: An Env object containing standard Scheme procedures
    """
    env = Env()
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs, 'append': op.add, 'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1], 'car': lambda x: x[0], 'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y, 'eq?': op.is_, 'equal?': op.eq,
        'length': len, 'list': lambda *x: list(x), 'list?': lambda x: isinstance(x, list),
        'map': map, 'max': max, 'min': min, 'not': op.not_,
        'null?': lambda x: x == [], 'number?': lambda x: isinstance(x, (int, float)),
        'procedure?': callable, 'round': round, 'symbol?': lambda x: isinstance(x, str),
        'print': print
    })
    return env


global_env = standard_env()


def eval(x, env=global_env):
    """
    Evaluate an expression in an environment.
    :param x: A Scheme expression
    :param env: An environment (defaults to the global environment)
    :return: The result of evaluating the expression
    """
    if isinstance(x, str):            # variable reference
        return env.find(x)[x]
    elif not isinstance(x, list):     # constant literal
        return x
    op, *args = x
    if op == 'quote':                 # quotation
        return args[0]
    elif op == 'if':                  # conditional
        (test, conseq, alt) = args
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif op == 'define':              # definition
        if isinstance(args[0], list):
            # (define (square x) (* x x))
            (symbol, parms) = args[0][0], args[0][1:]
            body = args[1]
            env[symbol] = Procedure(parms, body, env)
        else:
            (symbol, exp) = args
            env[symbol] = eval(exp, env)
    elif op == 'set!':                # assignment
        (symbol, exp) = args
        env.find(symbol)[symbol] = eval(exp, env)
    elif op == 'lambda':              # procedure
        (parms, body) = args
        return Procedure(parms, body, env)
    else:                             # procedure call
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]
        return proc(*vals)


def repl(prompt='lisp> '):
    """
    A prompt-read-eval-print loop for the Scheme interpreter.
    :param prompt: The prompt string to display (default is 'lisp> ')
    """
    while True:
        try:
            val = eval(parse(input(prompt)))
            if val is not None:
                print(schemestr(val))
        except EOFError:
            print("\nExiting REPL.")
            break
        except Exception as e:
            print(f"Error: {e}")


def schemestr(exp):
    """
    Convert a Python object back into a Scheme-readable string.
    :param exp: A Python object representing a Scheme expression
    :return: A string representation of the Scheme expression
    """
    if isinstance(exp, list):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


if __name__ == '__main__':
    repl()