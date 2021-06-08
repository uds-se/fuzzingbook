#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Tracking Information Flow" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/InformationFlow.html
# Last change: 2021-06-02 17:49:12+02:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Fuzzing Book - Tracking Information Flow

This file can be _executed_ as a script, running all experiments:

    $ python InformationFlow.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.InformationFlow import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/InformationFlow.html

This chapter provides two wrappers to Python _strings_ that allow one to track various properties. These include information on the security properties of the input, and information on originating indexes of the input string.

For tracking information on security properties, use `tstr` as follows:

>>> thello = tstr('hello', taint='LOW')

Now, any operation from `thello` that results in a string fragment would include the correct taint. For example:

>>> thello[1:2].taint
'LOW'

For tracking the originating indexes from the input string, use `ostr` as follows:

>>> ohw = ostr("hello\tworld", origin=100)

The originating indexes can be recovered as follows:

>>> (ohw[0:4] +"-"+ ohw[6:]).origin
[100, 101, 102, 103, -1, 106, 107, 108, 109, 110]


For more details, source, and documentation, see
"The Fuzzing Book - Tracking Information Flow"
at https://www.fuzzingbook.org/html/InformationFlow.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Tracking Information Flow
# =========================

if __name__ == '__main__':
    print('# Tracking Information Flow')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## A Vulnerable Database
## ---------------------

if __name__ == '__main__':
    print('\n## A Vulnerable Database')



INVENTORY = """\
1997,van,Ford,E350
2000,car,Mercury,Cougar
1999,car,Chevy,Venture\
"""

VEHICLES = INVENTORY.split('\n')

class SQLException(Exception):
    pass

class DB:
    def __init__(self, db={}):
        self.db = dict(db)

### Representing Tables

if __name__ == '__main__':
    print('\n### Representing Tables')



class DB(DB):
    def create_table(self, table, defs):
        self.db[table] = (defs, [])

class DB(DB):
    def table(self, t_name):
        if t_name in self.db:
            return self.db[t_name]
        raise SQLException('Table (%s) was not found' % repr(t_name))

def sample_db():
    db = DB()
    inventory_def = {'year': int, 'kind': str, 'company': str, 'model': str}
    db.create_table('inventory', inventory_def)
    return db

if __name__ == '__main__':
    db = sample_db()
    db.table('inventory')

class DB(DB):
    def column(self, table_decl, c_name):
        if c_name in table_decl: 
            return table_decl[c_name]
        raise SQLException('Column (%s) was not found' % repr(c_name))

if __name__ == '__main__':
    db = sample_db()
    decl, rows = db.table('inventory')
    db.column(decl, 'year')

### Executing SQL Statements

if __name__ == '__main__':
    print('\n### Executing SQL Statements')



class DB(DB):
    def do_select(self, query):
        assert False
    def do_update(self, query):
        assert False
    def do_insert(self, query):
        assert False
    def do_delete(self, query):
        assert False
    
    def sql(self, query):
        methods = [('select ', self.do_select), 
                   ('update ', self.do_update),
                   ('insert into ', self.do_insert),
                   ('delete from', self.do_delete)]
        for key, method in methods:
            if query.startswith(key):
                return method(query[len(key):])
        raise SQLException('Unknown SQL (%s)' % query)

### Selecting Data

if __name__ == '__main__':
    print('\n### Selecting Data')



class DB(DB):
    def do_select(self, query):
        FROM, WHERE = ' from ', ' where '
        table_start = query.find(FROM)
        if table_start < 0:
            raise SQLException('no table specified')

        where_start = query.find(WHERE)
        select = query[:table_start]

        if where_start >= 0:
            t_name = query[table_start + len(FROM):where_start]
            where = query[where_start + len(WHERE):]
        else:
            t_name = query[table_start + len(FROM):]
            where = ''
        _, table = self.table(t_name)

        if where:
            selected = self.expression_clause(table, "(%s)" % where)
            selected_rows = [hm for i, data, hm in selected if data]
        else:
            selected_rows = table

        rows = self.expression_clause(selected_rows, "(%s)" % select)
        return [data for i, data, hm in rows]

class DB(DB):
    def expression_clause(self, table, statement):
        selected = []
        for i, hm in enumerate(table):
            selected.append((i, self.my_eval(statement, {}, hm), hm))

        return selected

class DB(DB):
    def my_eval(self, statement, g, l):
        try:
            return eval(statement, g, l)
        except:
            raise SQLException('Invalid WHERE (%s)' % repr(statement))

if __name__ == '__main__':
    db = sample_db()
    db.sql('select year from inventory')

if __name__ == '__main__':
    db = sample_db()
    db.sql('select year from inventory where year == 2018')

### Inserting Data

if __name__ == '__main__':
    print('\n### Inserting Data')



class DB(DB):
    def do_insert(self, query):
        VALUES = ' values '
        table_end = query.find('(')
        t_name = query[:table_end].strip()
        names_end = query.find(')')
        decls, table = self.table(t_name)
        names = [i.strip() for i in query[table_end + 1:names_end].split(',')]

        # verify columns exist
        for k in names:
            self.column(decls, k)

        values_start = query.find(VALUES)

        if values_start < 0:
            raise SQLException('Invalid INSERT (%s)' % repr(query))

        values = [
            i.strip() for i in query[values_start + len(VALUES) + 1:-1].split(',')
        ]

        if len(names) != len(values):
            raise SQLException(
                'names(%s) != values(%s)' % (repr(names), repr(values)))

        # dict lookups happen in C code, so we cant use that
        kvs = {}
        for k,v in zip(names, values):
            for key,kval in decls.items():
                if k == key:
                    kvs[key] = self.convert(kval, v)
        table.append(kvs)

import ast

class DB(DB):
    def convert(self, cast, value):
        try:
            return cast(ast.literal_eval(value))
        except:
            raise SQLException('Invalid Conversion %s(%s)' % (cast, value))

if __name__ == '__main__':
    db = sample_db()
    db.sql('insert into inventory (year, kind, company, model) values (1997, "van", "Ford", "E350")')
    db.table('inventory')

if __name__ == '__main__':
    db.sql('select year + 1, kind from inventory')

if __name__ == '__main__':
    db.sql('select year, kind from inventory where year == 1997')

### Updating Data

if __name__ == '__main__':
    print('\n### Updating Data')



class DB(DB):
    def do_update(self, query):
        SET, WHERE = ' set ', ' where '
        table_end = query.find(SET)
        
        if table_end < 0:
            raise SQLException('Invalid UPDATE (%s)' % repr(query))
            
        set_end = table_end + 5
        t_name = query[:table_end]
        decls, table = self.table(t_name)
        names_end = query.find(WHERE)
        
        if names_end >= 0:
            names = query[set_end:names_end]
            where = query[names_end + len(WHERE):]
        else:
            names = query[set_end:]
            where = ''
            
        sets = [[i.strip() for i in name.split('=')]
                for name in names.split(',')]

        # verify columns exist
        for k, v in sets:
            self.column(decls, k)

        if where:
            selected = self.expression_clause(table, "(%s)" % where)
            updated = [hm for i, d, hm in selected if d]
        else:
            updated = table

        for hm in updated:
            for k, v in sets:
                # we can not do dict lookups because it is implemetned in C.
                for key, kval in decls.items():
                    if key == k:
                        hm[key] = self.convert(kval, v)
                
        return "%d records were updated" % len(updated)

if __name__ == '__main__':
    db = sample_db()
    db.sql('insert into inventory (year, kind, company, model) values (1997, "van", "Ford", "E350")')
    db.sql('select year from inventory')

if __name__ == '__main__':
    db.sql('update inventory set year = 1998 where year == 1997')
    db.sql('select year from inventory')

if __name__ == '__main__':
    db.table('inventory')

### Deleting Data

if __name__ == '__main__':
    print('\n### Deleting Data')



class DB(DB):
    def do_delete(self, query):
        WHERE = ' where '
        table_end = query.find(WHERE)
        if table_end < 0:
            raise SQLException('Invalid DELETE (%s)' % query)
        t_name = query[:table_end].strip()
        _, table = self.table(t_name)
        where = query[table_end + len(WHERE):]
        selected = self.expression_clause(table, "%s" % where)
        deleted = [i for i, d, hm in selected if d]
        for i in sorted(deleted, reverse=True):
            del table[i]
        return "%d records were deleted" % len(deleted)

if __name__ == '__main__':
    db = sample_db()
    db.sql('insert into inventory (year, kind, company, model) values (1997, "van", "Ford", "E350")')
    db.sql('select year from inventory')

if __name__ == '__main__':
    db.sql('delete from inventory where company == "Ford"')

if __name__ == '__main__':
    db.sql('select year from inventory')

### All Methods Together

if __name__ == '__main__':
    print('\n### All Methods Together')



if __name__ == '__main__':
    db = DB()

if __name__ == '__main__':
    inventory_def = {'year': int, 'kind': str, 'company': str, 'model': str}
    db.create_table('inventory', inventory_def)

def update_inventory(sqldb, vehicle):
    inventory_def = sqldb.db['inventory'][0]
    k, v = zip(*inventory_def.items())
    val = [repr(cast(val)) for cast, val in zip(v, vehicle.split(','))]
    sqldb.sql('insert into inventory (%s) values (%s)' % (','.join(k),
                                                          ','.join(val)))

if __name__ == '__main__':
    for V in VEHICLES:
        update_inventory(db, V)

if __name__ == '__main__':
    db.db

if __name__ == '__main__':
    db.sql('select year,kind from inventory')

if __name__ == '__main__':
    db.sql("select company,model from inventory where kind == 'car'")

if __name__ == '__main__':
    db.sql("update inventory set year = 1998, company = 'Suzuki' where kind == 'van'")

if __name__ == '__main__':
    db.db

if __name__ == '__main__':
    db.sql('select int(year)+10 from inventory')

if __name__ == '__main__':
    db.sql("insert into inventory (year, kind, company, model) values (1, 'charriot', 'Rome', 'Quadriga')")

if __name__ == '__main__':
    db.db

if __name__ == '__main__':
    db.sql("delete from inventory where year < 1900")

### Fuzzing SQL

if __name__ == '__main__':
    print('\n### Fuzzing SQL')



import string

EXPR_GRAMMAR = {
    "<start>": ["<expr>"],
    "<expr>": ["<bexpr>", "<aexpr>", "(<expr>)", "<term>"],
    "<bexpr>": [
        "<aexpr><lt><aexpr>",
        "<aexpr><gt><aexpr>",
        "<expr>==<expr>",
        "<expr>!=<expr>",
    ],
    "<aexpr>": [
        "<aexpr>+<aexpr>", "<aexpr>-<aexpr>", "<aexpr>*<aexpr>",
        "<aexpr>/<aexpr>", "<word>(<exprs>)", "<expr>"
    ],
    "<exprs>": ["<expr>,<exprs>", "<expr>"],
    "<lt>": ["<"],
    "<gt>": [">"],
    "<term>": ["<number>", "<word>"],
    "<number>": ["<integer>.<integer>", "<integer>", "-<number>"],
    "<integer>": ["<digit><integer>", "<digit>"],
    "<word>": ["<word><letter>", "<word><digit>", "<letter>"],
    "<digit>":
    list(string.digits),
    "<letter>":
    list(string.ascii_letters + '_:.')
}

INVENTORY_GRAMMAR = dict(
    EXPR_GRAMMAR, **{
        '<start>': ['<query>'],
        '<query>': [
            'select <exprs> from <table>',
            'select <exprs> from <table> where <bexpr>',
            'insert into <table> (<names>) values (<literals>)',
            'update <table> set <assignments> where <bexpr>',
            'delete from <table> where <bexpr>',
        ],
        '<table>': ['<word>'],
        '<names>': ['<column>,<names>', '<column>'],
        '<column>': ['<word>'],
        '<literals>': ['<literal>', '<literal>,<literals>'],
        '<literal>': ['<number>', "'<chars>'"],
        '<assignments>': ['<kvp>,<assignments>', '<kvp>'],
        '<kvp>': ['<column>=<value>'],
        '<value>': ['<word>'],
        '<chars>': ['<char>', '<char><chars>'],
        '<char>':
        [i for i in string.printable if i not in "<>'\"\t\n\r\x0b\x0c\x00"
         ] + ['<lt>', '<gt>'],
    })

INVENTORY_GRAMMAR_F = dict(INVENTORY_GRAMMAR, **{'<table>': ['inventory']})

from .GrammarFuzzer import GrammarFuzzer

if __name__ == '__main__':
    gf = GrammarFuzzer(INVENTORY_GRAMMAR_F)
    for _ in range(10):
        query = gf.fuzz()
        print(repr(query))
        try:
            res = db.sql(query)
            print(repr(res))
        except SQLException as e:
            print("> ", e)
            pass
        except:
            traceback.print_exc()
            break
        print()

## The Evil of Eval
## ----------------

if __name__ == '__main__':
    print('\n## The Evil of Eval')



if __name__ == '__main__':
    db.sql('select year from inventory where year < 2000')

if __name__ == '__main__':
    db.sql('select year - 1900 if year < 2000 else year - 2000 from inventory')

if __name__ == '__main__':
    db.sql('select __import__("os").popen("pwd").read() from inventory')

## Tracking String Taints
## ----------------------

if __name__ == '__main__':
    print('\n## Tracking String Taints')



### A Class for Tainted Strings

if __name__ == '__main__':
    print('\n### A Class for Tainted Strings')



class tstr(str):
    def __new__(cls, value, *args, **kw):
        return str.__new__(cls, value)

    def __init__(self, value, taint=None, **kwargs):
        self.taint = taint

class tstr(tstr):
    def __repr__(self):
        return tstr(str.__repr__(self), taint=self.taint)

class tstr(tstr):
    def __str__(self):
        return str.__str__(self)

if __name__ == '__main__':
    thello = tstr('hello', taint='LOW')

if __name__ == '__main__':
    thello.taint

if __name__ == '__main__':
    repr(thello).taint

class tstr(tstr):
    def clear_taint(self):
        self.taint = None
        return self

    def has_taint(self):
        return self.taint is not None

### String Operators

if __name__ == '__main__':
    print('\n### String Operators')



class tstr(tstr):
    def create(self, s):
        return tstr(s, taint=self.taint)

def make_str_wrapper(fun):
    def proxy(self, *args, **kwargs):
        res = fun(self, *args, **kwargs)
        return self.create(res)
    return proxy

def informationflow_init_1():
    for name in ['__format__', '__mod__', '__rmod__', '__getitem__', '__add__', '__mul__', '__rmul__',
                 'capitalize', 'casefold', 'center', 'encode',
                 'expandtabs', 'format', 'format_map', 'join', 'ljust', 'lower', 'lstrip', 'replace',
                 'rjust', 'rstrip', 'strip', 'swapcase', 'title', 'translate', 'upper']:
        fun = getattr(str, name)
        setattr(tstr, name, make_str_wrapper(fun))

if __name__ == '__main__':
    informationflow_init_1()

INITIALIZER_LIST = [informationflow_init_1]

def initialize():
    for fn in INITIALIZER_LIST:
        fn()

class tstr(tstr):
    def __radd__(self, s):
        return self.create(s + str(self))

if __name__ == '__main__':
    thello = tstr('hello', taint='LOW')

if __name__ == '__main__':
    thello[0].taint

if __name__ == '__main__':
    thello[1:3].taint

if __name__ == '__main__':
    (tstr('foo', taint='HIGH') + 'bar').taint

if __name__ == '__main__':
    ('foo' + tstr('bar', taint='HIGH')).taint

if __name__ == '__main__':
    thello += ', world'

if __name__ == '__main__':
    thello.taint

if __name__ == '__main__':
    (thello * 5).taint

if __name__ == '__main__':
    ('hw %s' % thello).taint

if __name__ == '__main__':
    (tstr('hello %s', taint='HIGH') % 'world').taint

import string

## Tracking Untrusted Input
## ------------------------

if __name__ == '__main__':
    print('\n## Tracking Untrusted Input')



class TrustedDB(DB):
    def sql(self, s):
        assert isinstance(s, tstr), "Need a tainted string"
        assert s.taint == 'TRUSTED', "Need a string with trusted taint"
        return super().sql(s)

if __name__ == '__main__':
    bdb = TrustedDB(db.db)

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        bdb.sql("select year from INVENTORY")

if __name__ == '__main__':
    bad_user_input = tstr('__import__("os").popen("ls").read()', taint='UNTRUSTED')
    with ExpectError():
        bdb.sql(bad_user_input)

import re

def sanitize(user_input):
    assert isinstance(user_input, tstr)
    if re.match(
            r'^select +[-a-zA-Z0-9_, ()]+ from +[-a-zA-Z0-9_, ()]+$', user_input):
        return tstr(user_input, taint='TRUSTED')
    else:
        return tstr('', taint='UNTRUSTED')

if __name__ == '__main__':
    good_user_input = tstr("select year,model from inventory", taint='UNTRUSTED')
    sanitized_input = sanitize(good_user_input)
    sanitized_input

if __name__ == '__main__':
    sanitized_input.taint

if __name__ == '__main__':
    bdb.sql(sanitized_input)

if __name__ == '__main__':
    sanitized_input = sanitize(bad_user_input)
    sanitized_input

if __name__ == '__main__':
    sanitized_input.taint

if __name__ == '__main__':
    with ExpectError():
        bdb.sql(sanitized_input)

## Taint Aware Fuzzing
## -------------------

if __name__ == '__main__':
    print('\n## Taint Aware Fuzzing')



class Tainted(Exception):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return 'Tainted[%s]' % self.v

### TaintedDB

if __name__ == '__main__':
    print('\n### TaintedDB')



class TaintedDB(DB):
    def my_eval(self, statement, g, l):
        if statement.taint != 'TRUSTED':
            raise Tainted(statement)
        try:
            return eval(statement, g, l)
        except:
            raise SQLException('Invalid SQL (%s)' % repr(statement))

if __name__ == '__main__':
    tdb = TaintedDB()

if __name__ == '__main__':
    tdb.db = db.db

import traceback

if __name__ == '__main__':
    for _ in range(10):
        query = gf.fuzz()
        print(repr(query))
        try:
            res = tdb.sql(tstr(query, taint='UNTRUSTED'))
            print(repr(res))
        except SQLException as e:
            pass
        except Tainted as e:
            print("> ", e)
        except:
            traceback.print_exc()
            break
        print()

## Preventing Privacy Leaks
## ------------------------

if __name__ == '__main__':
    print('\n## Preventing Privacy Leaks')



if __name__ == '__main__':
    secrets = tstr('<Plenty of secret keys>', taint='SECRET')

if __name__ == '__main__':
    secrets[1:3].taint

if __name__ == '__main__':
    user_input = "hello"
    reply = user_input

if __name__ == '__main__':
    isinstance(reply, tstr)

if __name__ == '__main__':
    reply = user_input + secrets[0:5]

if __name__ == '__main__':
    reply

if __name__ == '__main__':
    reply.taint

def send_back(s):
    assert not isinstance(s, tstr) and not s.taint == 'SECRET'
    ...

if __name__ == '__main__':
    with ExpectError():
        send_back(reply)

### Tracking Character Origins

if __name__ == '__main__':
    print('\n### Tracking Character Origins')



from .Fuzzer import heartbeat

if __name__ == '__main__':
    reply = heartbeat('hello', 5, memory=secrets)

if __name__ == '__main__':
    reply.taint

if __name__ == '__main__':
    thilo = tstr("High", taint='HIGH') + tstr("Low", taint='LOW')

if __name__ == '__main__':
    thilo

if __name__ == '__main__':
    thilo.taint

### Tracking Individual Characters

if __name__ == '__main__':
    print('\n### Tracking Individual Characters')



### A Class for Tracking Character Origins

if __name__ == '__main__':
    print('\n### A Class for Tracking Character Origins')



class ostr(str):
    DEFAULT_ORIGIN = 0

    def __new__(cls, value, *args, **kw):
        return str.__new__(cls, value)

    def __init__(self, value, taint=None, origin=None, **kwargs):
        self.taint = taint

        if origin is None:
            origin = ostr.DEFAULT_ORIGIN
        if isinstance(origin, int):
            self.origin = list(range(origin, origin + len(self)))
        else:
            self.origin = origin
        assert len(self.origin) == len(self)

class ostr(ostr):
    def create(self, s):
        return ostr(s, taint=self.taint, origin=self.origin)

class ostr(ostr):
    UNKNOWN_ORIGIN = -1

    def __repr__(self):
        # handle escaped chars
        origin = [ostr.UNKNOWN_ORIGIN]
        for s, o in zip(str(self), self.origin):
            origin.extend([o] * (len(repr(s)) - 2))
        origin.append(ostr.UNKNOWN_ORIGIN)
        return ostr(str.__repr__(self), taint=self.taint, origin=origin)

class ostr(ostr):
    def __str__(self):
        return str.__str__(self)

if __name__ == '__main__':
    thello = ostr('hello')
    assert thello.origin == [0, 1, 2, 3, 4]

if __name__ == '__main__':
    tworld = ostr('world', origin=6)
    assert tworld.origin == [6, 7, 8, 9, 10]

if __name__ == '__main__':
    a = ostr("hello\tworld")

if __name__ == '__main__':
    repr(a).origin

if __name__ == '__main__':
    assert type(str(thello)) == str

if __name__ == '__main__':
    repr(thello)

if __name__ == '__main__':
    repr(thello).origin

class ostr(ostr):
    def clear_taint(self):
        self.taint = None
        return self

    def has_taint(self):
        return self.taint is not None

class ostr(ostr):
    def clear_origin(self):
        self.origin = [self.UNKNOWN_ORIGIN] * len(self)
        return self

    def has_origin(self):
        return any(origin != self.UNKNOWN_ORIGIN for origin in self.origin)

if __name__ == '__main__':
    thello = ostr('Hello')
    assert thello.has_origin()

if __name__ == '__main__':
    thello.clear_origin()
    assert not thello.has_origin()

#### Create

if __name__ == '__main__':
    print('\n#### Create')



class ostr(ostr):
    def create(self, res, origin=None):
        return ostr(res, taint=self.taint, origin=origin)

if __name__ == '__main__':
    thello = ostr('hello', taint='HIGH')
    tworld = thello.create('world', origin=6)

if __name__ == '__main__':
    tworld.origin

if __name__ == '__main__':
    tworld.taint

if __name__ == '__main__':
    assert (thello.origin, tworld.origin) == (
        [0, 1, 2, 3, 4], [6, 7, 8, 9, 10])

#### Index

if __name__ == '__main__':
    print('\n#### Index')



class ostr(ostr):
    def __getitem__(self, key):
        res = super().__getitem__(key)
        if isinstance(key, int):
            key = len(self) + key if key < 0 else key
            return self.create(res, [self.origin[key]])
        elif isinstance(key, slice):
            return self.create(res, self.origin[key])
        else:
            assert False

if __name__ == '__main__':
    hello = ostr('hello', taint='HIGH')
    assert (hello[0], hello[-1]) == ('h', 'o')
    hello[0].taint

#### Slices

if __name__ == '__main__':
    print('\n#### Slices')



class ostr(ostr):
    def __iter__(self):
        return ostr_iterator(self)

class ostr_iterator():
    def __init__(self, ostr):
        self._ostr = ostr
        self._str_idx = 0

    def __next__(self):
        if self._str_idx == len(self._ostr):
            raise StopIteration
        # calls ostr getitem should be ostr
        c = self._ostr[self._str_idx]
        assert isinstance(c, ostr)
        self._str_idx += 1
        return c

if __name__ == '__main__':
    thw = ostr('hello world', taint='HIGH')
    thw[0:5]

if __name__ == '__main__':
    assert thw[0:5].has_taint()
    assert thw[0:5].has_origin()

if __name__ == '__main__':
    thw[0:5].taint

if __name__ == '__main__':
    thw[0:5].origin

#### Splits

if __name__ == '__main__':
    print('\n#### Splits')



def make_split_wrapper(fun):
    def proxy(self, *args, **kwargs):
        lst = fun(self, *args, **kwargs)
        return [self.create(elem) for elem in lst]
    return proxy

if __name__ == '__main__':
    for name in ['split', 'rsplit', 'splitlines']:
        fun = getattr(str, name)
        setattr(ostr, name, make_split_wrapper(fun))

if __name__ == '__main__':
    thello = ostr('hello world', taint='LOW')
    thello == 'hello world'

if __name__ == '__main__':
    thello.split()[0].taint

#### Concatenation

if __name__ == '__main__':
    print('\n#### Concatenation')



class ostr(ostr):
    def __add__(self, other):
        if isinstance(other, ostr):
            return self.create(str.__add__(self, other),
                               (self.origin + other.origin))
        else:
            return self.create(str.__add__(self, other),
                               (self.origin + [self.UNKNOWN_ORIGIN for i in other]))

if __name__ == '__main__':
    thello = ostr("hello")
    tworld = ostr("world", origin=6)
    thw = thello + tworld
    assert thw.origin == [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]

if __name__ == '__main__':
    space = "  "
    th_w = thello + space + tworld
    assert th_w.origin == [
        0,
        1,
        2,
        3,
        4,
        ostr.UNKNOWN_ORIGIN,
        ostr.UNKNOWN_ORIGIN,
        6,
        7,
        8,
        9,
        10]

class ostr(ostr):
    def __radd__(self, other):
        origin = other.origin if isinstance(other, ostr) else [
            self.UNKNOWN_ORIGIN for i in other]
        return self.create(str.__add__(other, self), (origin + self.origin))

if __name__ == '__main__':
    shello = "hello"
    tworld = ostr("world")
    thw = shello + tworld
    assert thw.origin == [ostr.UNKNOWN_ORIGIN] * len(shello) + [0, 1, 2, 3, 4]

#### Extract Origin String

if __name__ == '__main__':
    print('\n#### Extract Origin String')



class ostr(ostr):
    class TaintException(Exception):
        pass

    def x(self, i=0):
        if not self.origin:
            raise origin.TaintException('Invalid request idx')
        if isinstance(i, int):
            return [self[p]
                    for p in [k for k, j in enumerate(self.origin) if j == i]]
        elif isinstance(i, slice):
            r = range(i.start or 0, i.stop or len(self), i.step or 1)
            return [self[p]
                    for p in [k for k, j in enumerate(self.origin) if j in r]]

if __name__ == '__main__':
    thw = ostr('hello world', origin=100)

if __name__ == '__main__':
    assert thw.x(101) == ['e']

if __name__ == '__main__':
    assert thw.x(slice(101, 105)) == ['e', 'l', 'l', 'o']

#### Replace

if __name__ == '__main__':
    print('\n#### Replace')



class ostr(ostr):
    def replace(self, a, b, n=None):
        old_origin = self.origin
        b_origin = b.origin if isinstance(
            b, ostr) else [self.UNKNOWN_ORIGIN] * len(b)
        mystr = str(self)
        i = 0
        while True:
            if n and i >= n:
                break
            idx = mystr.find(a)
            if idx == -1:
                break
            last = idx + len(a)
            mystr = mystr.replace(a, b, 1)
            partA, partB = old_origin[0:idx], old_origin[last:]
            old_origin = partA + b_origin + partB
            i += 1
        return self.create(mystr, old_origin)

if __name__ == '__main__':
    my_str = ostr("aa cde aa")
    res = my_str.replace('aa', 'bb')
    assert res, res.origin == ('bb', 'cde', 'bb',
                               [self.UNKNOWN_ORIGIN, self.UNKNOWN_ORIGIN,
                                2, 3, 4, 5, 6,
                                self.UNKNOWN_ORIGIN, self.UNKNOWN_ORIGIN])

if __name__ == '__main__':
    my_str = ostr("aa cde aa")
    res = my_str.replace('aa', ostr('bb', origin=100))
    assert (
        res, res.origin) == (
            ('bb cde bb'), [
                100, 101, 2, 3, 4, 5, 6, 100, 101])

#### Split

if __name__ == '__main__':
    print('\n#### Split')



class ostr(ostr):
    def _split_helper(self, sep, splitted):
        result_list = []
        last_idx = 0
        first_idx = 0
        sep_len = len(sep)

        for s in splitted:
            last_idx = first_idx + len(s)
            item = self[first_idx:last_idx]
            result_list.append(item)
            first_idx = last_idx + sep_len
        return result_list

    def _split_space(self, splitted):
        result_list = []
        last_idx = 0
        first_idx = 0
        sep_len = 0
        for s in splitted:
            last_idx = first_idx + len(s)
            item = self[first_idx:last_idx]
            result_list.append(item)
            v = str(self[last_idx:])
            sep_len = len(v) - len(v.lstrip(' '))
            first_idx = last_idx + sep_len
        return result_list

    def rsplit(self, sep=None, maxsplit=-1):
        splitted = super().rsplit(sep, maxsplit)
        if not sep:
            return self._split_space(splitted)
        return self._split_helper(sep, splitted)

    def split(self, sep=None, maxsplit=-1):
        splitted = super().split(sep, maxsplit)
        if not sep:
            return self._split_space(splitted)
        return self._split_helper(sep, splitted)

if __name__ == '__main__':
    my_str = ostr('ab cdef ghij kl')
    ab, cdef, ghij, kl = my_str.rsplit(sep=' ')
    assert (ab.origin, cdef.origin, ghij.origin,
            kl.origin) == ([0, 1], [3, 4, 5, 6], [8, 9, 10, 11], [13, 14])

    my_str = ostr('ab cdef ghij kl', origin=list(range(0, 15)))
    ab, cdef, ghij, kl = my_str.rsplit(sep=' ')
    assert(ab.origin, cdef.origin, kl.origin) == ([0, 1], [3, 4, 5, 6], [13, 14])

if __name__ == '__main__':
    my_str = ostr('ab   cdef ghij    kl', origin=100, taint='HIGH')
    ab, cdef, ghij, kl = my_str.rsplit()
    assert (ab.origin, cdef.origin, ghij.origin,
            kl.origin) == ([100, 101], [105, 106, 107, 108], [110, 111, 112, 113],
                           [118, 119])

    my_str = ostr('ab   cdef ghij    kl', origin=list(range(0, 20)), taint='HIGH')
    ab, cdef, ghij, kl = my_str.split()
    assert (ab.origin, cdef.origin, kl.origin) == ([0, 1], [5, 6, 7, 8], [18, 19])
    assert ab.taint == 'HIGH'

#### Strip

if __name__ == '__main__':
    print('\n#### Strip')



class ostr(ostr):
    def strip(self, cl=None):
        return self.lstrip(cl).rstrip(cl)

    def lstrip(self, cl=None):
        res = super().lstrip(cl)
        i = self.find(res)
        return self[i:]

    def rstrip(self, cl=None):
        res = super().rstrip(cl)
        return self[0:len(res)]

if __name__ == '__main__':
    my_str1 = ostr("  abc  ")
    v = my_str1.strip()
    assert v, v.origin == ('abc', [2, 3, 4])

if __name__ == '__main__':
    my_str1 = ostr("  abc  ")
    v = my_str1.lstrip()
    assert (v, v.origin) == ('abc  ', [2, 3, 4, 5, 6])

if __name__ == '__main__':
    my_str1 = ostr("  abc  ")
    v = my_str1.rstrip()
    assert (v, v.origin) == ('  abc', [0, 1, 2, 3, 4])

#### Expand Tabs

if __name__ == '__main__':
    print('\n#### Expand Tabs')



class ostr(ostr):
    def expandtabs(self, n=8):
        parts = self.split('\t')
        res = super().expandtabs(n)
        all_parts = []
        for i, p in enumerate(parts):
            all_parts.extend(p.origin)
            if i < len(parts) - 1:
                l = len(all_parts) % n
                all_parts.extend([p.origin[-1]] * l)
        return self.create(res, all_parts)

if __name__ == '__main__':
    my_str = str("ab\tcd")
    my_ostr = ostr("ab\tcd")
    v1 = my_str.expandtabs(4)
    v2 = my_ostr.expandtabs(4)

if __name__ == '__main__':
    assert str(v1) == str(v2)
    assert (len(v1), repr(v2), v2.origin) == (6, "'ab  cd'", [0, 1, 1, 1, 3, 4])

class ostr(ostr):
    def join(self, iterable):
        mystr = ''
        myorigin = []
        sep_origin = self.origin
        lst = list(iterable)
        for i, s in enumerate(lst):
            sorigin = s.origin if isinstance(s, ostr) else [
                self.UNKNOWN_ORIGIN] * len(s)
            myorigin.extend(sorigin)
            mystr += str(s)
            if i < len(lst) - 1:
                myorigin.extend(sep_origin)
                mystr += str(self)
        res = super().join(iterable)
        assert len(res) == len(mystr)
        return self.create(res, myorigin)

if __name__ == '__main__':
    my_str = ostr("ab cd", origin=100)
    (v1, v2), v3 = my_str.split(), 'ef'
    assert (v1.origin, v2.origin) == ([100, 101], [103, 104])

if __name__ == '__main__':
    v4 = ostr('').join([v2, v3, v1])
    assert (
        v4, v4.origin) == (
            'cdefab', [
                103, 104, ostr.UNKNOWN_ORIGIN, ostr.UNKNOWN_ORIGIN, 100, 101])

if __name__ == '__main__':
    my_str = ostr("ab cd", origin=100)
    (v1, v2), v3 = my_str.split(), 'ef'
    assert (v1.origin, v2.origin) == ([100, 101], [103, 104])

if __name__ == '__main__':
    v4 = ostr(',').join([v2, v3, v1])
    assert (v4, v4.origin) == ('cd,ef,ab',
                               [103, 104, 0, ostr.UNKNOWN_ORIGIN, ostr.UNKNOWN_ORIGIN, 0, 100, 101])

#### Partitions

if __name__ == '__main__':
    print('\n#### Partitions')



class ostr(ostr):
    def partition(self, sep):
        partA, sep, partB = super().partition(sep)
        return (self.create(partA, self.origin[0:len(partA)]),
                self.create(sep,
                            self.origin[len(partA):len(partA) + len(sep)]),
                self.create(partB, self.origin[len(partA) + len(sep):]))

    def rpartition(self, sep):
        partA, sep, partB = super().rpartition(sep)
        return (self.create(partA, self.origin[0:len(partA)]),
                self.create(sep,
                            self.origin[len(partA):len(partA) + len(sep)]),
                self.create(partB, self.origin[len(partA) + len(sep):]))

#### Justify

if __name__ == '__main__':
    print('\n#### Justify')



class ostr(ostr):
    def ljust(self, width, fillchar=' '):
        res = super().ljust(width, fillchar)
        initial = len(res) - len(self)
        if isinstance(fillchar, tstr):
            t = fillchar.x()
        else:
            t = self.UNKNOWN_ORIGIN
        return self.create(res, [t] * initial + self.origin)

class ostr(ostr):
    def rjust(self, width, fillchar=' '):
        res = super().rjust(width, fillchar)
        final = len(res) - len(self)
        if isinstance(fillchar, tstr):
            t = fillchar.x()
        else:
            t = self.UNKNOWN_ORIGIN
        return self.create(res, self.origin + [t] * final)

#### mod

if __name__ == '__main__':
    print('\n#### mod')



class ostr(ostr):
    def __mod__(self, s):
        # nothing else implemented for the time being
        assert isinstance(s, str)
        s_origin = s.origin if isinstance(
            s, ostr) else [self.UNKNOWN_ORIGIN] * len(s)
        i = self.find('%s')
        assert i >= 0
        res = super().__mod__(s)
        r_origin = self.origin[:]
        r_origin[i:i + 2] = s_origin
        return self.create(res, origin=r_origin)

class ostr(ostr):
    def __rmod__(self, s):
        # nothing else implemented for the time being
        assert isinstance(s, str)
        r_origin = s.origin if isinstance(
            s, ostr) else [self.UNKNOWN_ORIGIN] * len(s)
        i = s.find('%s')
        assert i >= 0
        res = super().__rmod__(s)
        s_origin = self.origin[:]
        r_origin[i:i + 2] = s_origin
        return self.create(res, origin=r_origin)

if __name__ == '__main__':
    a = ostr('hello %s world', origin=100)
    a

if __name__ == '__main__':
    (a % 'good').origin

if __name__ == '__main__':
    b = 'hello %s world'
    c = ostr('bad', origin=10)
    (b % c).origin

#### String methods that do not change origin

if __name__ == '__main__':
    print('\n#### String methods that do not change origin')



class ostr(ostr):
    def swapcase(self):
        return self.create(str(self).swapcase(), self.origin)

    def upper(self):
        return self.create(str(self).upper(), self.origin)

    def lower(self):
        return self.create(str(self).lower(), self.origin)

    def capitalize(self):
        return self.create(str(self).capitalize(), self.origin)

    def title(self):
        return self.create(str(self).title(), self.origin)

if __name__ == '__main__':
    a = ostr('aa', origin=100).upper()
    a, a.origin

#### General wrappers

if __name__ == '__main__':
    print('\n#### General wrappers')



def make_str_wrapper(fun):
    def proxy(*args, **kwargs):
        res = fun(*args, **kwargs)
        return res
    return proxy

import inspect

import types

def informationflow_init_2():
    ostr_members = [name for name, fn in inspect.getmembers(ostr, callable)
                    if isinstance(fn, types.FunctionType) and fn.__qualname__.startswith('ostr')]

    for name, fn in inspect.getmembers(str, callable):
        if name not in set(['__class__', '__new__', '__str__', '__init__',
                            '__repr__', '__getattribute__']) | set(ostr_members):
            setattr(ostr, name, make_str_wrapper(fn))

if __name__ == '__main__':
    informationflow_init_2()

INITIALIZER_LIST.append(informationflow_init_2)

#### Methods yet to be translated

if __name__ == '__main__':
    print('\n#### Methods yet to be translated')



def make_str_abort_wrapper(fun):
    def proxy(*args, **kwargs):
        raise ostr.TaintException(
            '%s Not implemented in `ostr`' %
            fun.__name__)
    return proxy

def informationflow_init_3():
    for name, fn in inspect.getmembers(str, callable):
        # Omitted 'splitlines' as this is needed for formatting output in
        # IPython/Jupyter
        if name in ['__format__', 'format_map', 'format',
                    '__mul__', '__rmul__', 'center', 'zfill', 'decode', 'encode']:
            setattr(ostr, name, make_str_abort_wrapper(fn))

if __name__ == '__main__':
    informationflow_init_3()

INITIALIZER_LIST.append(informationflow_init_3)

### Checking Origins

if __name__ == '__main__':
    print('\n### Checking Origins')



if __name__ == '__main__':
    s = ostr("hello", origin=100)
    s[1]

if __name__ == '__main__':
    s[1].origin

if __name__ == '__main__':
    set(s[1].origin) <= set(s.origin)

if __name__ == '__main__':
    t = ostr("world", origin=200)

if __name__ == '__main__':
    set(s.origin) <= set(t.origin)

if __name__ == '__main__':
    u = s + t + "!"

if __name__ == '__main__':
    u.origin

if __name__ == '__main__':
    ostr.UNKNOWN_ORIGIN in u.origin

### Privacy Leaks Revisited

if __name__ == '__main__':
    print('\n### Privacy Leaks Revisited')



SECRET_ORIGIN = 1000

if __name__ == '__main__':
    secret = ostr('<again, some super-secret input>', origin=SECRET_ORIGIN)

if __name__ == '__main__':
    print(secret.origin)

if __name__ == '__main__':
    s = heartbeat('hello', 5, memory=secret)
    s

if __name__ == '__main__':
    print(s.origin)

if __name__ == '__main__':
    assert s.origin == [ostr.UNKNOWN_ORIGIN] * len(s)

if __name__ == '__main__':
    assert all(origin == ostr.UNKNOWN_ORIGIN for origin in s.origin)

if __name__ == '__main__':
    assert not any(origin >= SECRET_ORIGIN for origin in s.origin)

if __name__ == '__main__':
    s = heartbeat('hello', 32, memory=secret)
    s

if __name__ == '__main__':
    print(s.origin)

if __name__ == '__main__':
    with ExpectError():
        assert s.origin == [ostr.UNKNOWN_ORIGIN] * len(s)

if __name__ == '__main__':
    with ExpectError():
        assert all(origin == ostr.UNKNOWN_ORIGIN for origin in s.origin)

if __name__ == '__main__':
    with ExpectError():
        assert not any(origin >= SECRET_ORIGIN for origin in s.origin)

## Taint-Directed Fuzzing
## ----------------------

if __name__ == '__main__':
    print('\n## Taint-Directed Fuzzing')



### TrackingDB

if __name__ == '__main__':
    print('\n### TrackingDB')



class TrackingDB(TaintedDB):
    def my_eval(self, statement, g, l):
        if statement.origin:
            raise Tainted(statement)
        try:
            return eval(statement, g, l)
        except:
            raise SQLException('Invalid SQL (%s)' % repr(statement))

### TaintedGrammarFuzzer

if __name__ == '__main__':
    print('\n### TaintedGrammarFuzzer')



import random

from .Grammars import START_SYMBOL

from .GrammarFuzzer import GrammarFuzzer

from .Parser import canonical

class TaintedGrammarFuzzer(GrammarFuzzer):
    def __init__(self,
                 grammar,
                 start_symbol=START_SYMBOL,
                 expansion_switch=1,
                 log=False):
        self.tainted_start_symbol = ostr(
            start_symbol, origin=[1] * len(start_symbol))
        self.expansion_switch = expansion_switch
        self.log = log
        self.grammar = grammar
        self.c_grammar = canonical(grammar)
        self.init_tainted_grammar()

    def expansion_cost(self, expansion, seen=set()):
        symbols = [e for e in expansion if e in self.c_grammar]
        if len(symbols) == 0:
            return 1

        if any(s in seen for s in symbols):
            return float('inf')

        return sum(self.symbol_cost(s, seen) for s in symbols) + 1

    def fuzz_tree(self):
        tree = (self.tainted_start_symbol, [])
        nt_leaves = [tree]
        expansion_trials = 0
        while nt_leaves:
            idx = random.randint(0, len(nt_leaves) - 1)
            key, children = nt_leaves[idx]
            expansions = self.ct_grammar[key]
            if expansion_trials < self.expansion_switch:
                expansion = random.choice(expansions)
            else:
                costs = [self.expansion_cost(e) for e in expansions]
                m = min(costs)
                all_min = [i for i, c in enumerate(costs) if c == m]
                expansion = expansions[random.choice(all_min)]

            new_leaves = [(token, []) for token in expansion]
            new_nt_leaves = [e for e in new_leaves if e[0] in self.ct_grammar]
            children[:] = new_leaves
            nt_leaves[idx:idx + 1] = new_nt_leaves
            if self.log:
                print("%-40s" % (key + " -> " + str(expansion)))
            expansion_trials += 1
        return tree

    def fuzz(self):
        self.derivation_tree = self.fuzz_tree()
        return self.tree_to_string(self.derivation_tree)

class TaintedGrammarFuzzer(TaintedGrammarFuzzer):
    def init_tainted_grammar(self):
        key_increment, alt_increment, token_increment = 1000, 100, 10
        key_origin = key_increment
        self.ct_grammar = {}
        for key, val in self.c_grammar.items():
            key_origin += key_increment
            os = []
            for v in val:
                ts = []
                key_origin += alt_increment
                for t in v:
                    nt = ostr(t, origin=key_origin)
                    key_origin += token_increment
                    ts.append(nt)
                os.append(ts)
            self.ct_grammar[key] = os

        # a use tracking grammar
        self.ctp_grammar = {}
        for key, val in self.ct_grammar.items():
            self.ctp_grammar[key] = [(v, dict(use=0)) for v in val]

if __name__ == '__main__':
    trdb = TrackingDB(db.db)

class TaintedGrammarFuzzer(TaintedGrammarFuzzer):
    def tree_to_string(self, tree):
        symbol, children, *_ = tree
        e = ostr('')
        if children:
            return e.join([self.tree_to_string(c) for c in children])
        else:
            return e if symbol in self.c_grammar else symbol

class TaintedGrammarFuzzer(TaintedGrammarFuzzer):
    def update_grammar(self, origin, dtree):
        def update_tree(dtree, origin):
            key, children = dtree
            if children:
                updated_children = [update_tree(c, origin) for c in children]
                corigin = set.union(
                    *[o for (key, children, o) in updated_children])
                corigin = corigin.union(set(key.origin))
                return (key, children, corigin)
            else:
                my_origin = set(key.origin).intersection(origin)
                return (key, [], my_origin)

        key, children, oset = update_tree(dtree, set(origin))
        for key, alts in self.ctp_grammar.items():
            for alt, o in alts:
                alt_origins = set([i for token in alt for i in token.origin])
                if alt_origins.intersection(oset):
                    o['use'] += 1

def tree_type(tree):
    key, children = tree
    return (type(key), key, [tree_type(c) for c in children])

if __name__ == '__main__':
    tgf = TaintedGrammarFuzzer(INVENTORY_GRAMMAR_F)
    x = None
    for _ in range(10):
        qtree = tgf.fuzz_tree()
        query = tgf.tree_to_string(qtree)
        assert isinstance(query, ostr)
        try:
            print(repr(query))
            res = trdb.sql(query)
            print(repr(res))
        except SQLException as e:
            print(e)
        except Tainted as e:
            print(e)
            origin = e.args[0].origin
            tgf.update_grammar(origin, qtree)
        except:
            traceback.print_exc()
            break
        print()

if __name__ == '__main__':
    tgf.ctp_grammar

### The Limits of Taint Tracking

if __name__ == '__main__':
    print('\n### The Limits of Taint Tracking')



#### Conversions

if __name__ == '__main__':
    print('\n#### Conversions')



def strip_all_info(s):
    t = ""
    for c in s:
        t += chr(ord(c))
    return t

if __name__ == '__main__':
    thello = ostr("Secret")
    thello

if __name__ == '__main__':
    thello.origin

if __name__ == '__main__':
    thello_stripped = strip_all_info(thello)
    thello_stripped

if __name__ == '__main__':
    with ExpectError():
        thello_stripped.origin

#### Internal C libraries

if __name__ == '__main__':
    print('\n#### Internal C libraries')



if __name__ == '__main__':
    hello = ostr('hello', origin=100)
    world = ostr('world', origin=200)
    (hello + ' ' + world).origin

if __name__ == '__main__':
    with ExpectError():
        ''.join([hello, ' ', world]).origin

#### Implicit Information Flow

if __name__ == '__main__':
    print('\n#### Implicit Information Flow')



def strip_all_info_again(s):
    t = ""
    for c in s:
        if c == 'a':
            t += 'a'
        elif c == 'b':
            t += 'b'
        elif c == 'c':
            t += 'c'
    ...

#### Enforcing Tainting

if __name__ == '__main__':
    print('\n#### Enforcing Tainting')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    thello = tstr('hello', taint='LOW')

if __name__ == '__main__':
    thello[1:2].taint

if __name__ == '__main__':
    ohw = ostr("hello\tworld", origin=100)

if __name__ == '__main__':
    (ohw[0:4] +"-"+ ohw[6:]).origin

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Tainted Numbers

if __name__ == '__main__':
    print('\n### Exercise 1: Tainted Numbers')



#### Part 1: Creation

if __name__ == '__main__':
    print('\n#### Part 1: Creation')



class tint(int):
    def __new__(cls, value, *args, **kw):
        return int.__new__(cls, value)

    def __init__(self, value, taint=None, **kwargs):
        self.taint = taint

if __name__ == '__main__':
    x = tint(42, taint='SECRET')
    assert x.taint == 'SECRET'

#### Part 2: Arithmetic expressions

if __name__ == '__main__':
    print('\n#### Part 2: Arithmetic expressions')



class tint(tint):
    def create(self, n):
        # print("New tint from", n)
        return tint(n, taint=self.taint)

def make_int_wrapper(fun):
    def proxy(self, *args, **kwargs):
        res = fun(self, *args, **kwargs)
        # print(fun, args, kwargs, "=", repr(res))
        return self.create(res)
    return proxy

if __name__ == '__main__':
    for name in ['__add__', '__radd__', '__mul__', '__rmul__', '__sub__',
                 '__floordiv__', '__truediv__']:
        fun = getattr(int, name)
        setattr(tint, name, make_int_wrapper(fun))

if __name__ == '__main__':
    x = tint(42, taint='SECRET')
    y = x + 1
    y.taint

#### Part 3: Passing taints from integers to strings

if __name__ == '__main__':
    print('\n#### Part 3: Passing taints from integers to strings')



class tint(tint):
    def __repr__(self):
        s = int.__repr__(self)
        return tstr(s, taint=self.taint)

class tint(tint):
    def __str__(self):
        return tstr(int.__str__(self), taint=self.taint)

if __name__ == '__main__':
    x = tint(42, taint='SECRET')
    s = repr(x)
    assert s.taint == 'SECRET'

#### Part 4: Passing taints from strings to integers

if __name__ == '__main__':
    print('\n#### Part 4: Passing taints from strings to integers')



class tint(tint):
    def __init__(self, value, taint=None, **kwargs):
        if taint is not None:
            self.taint = taint
        else:
            self.taint = getattr(value, 'taint', None)

if __name__ == '__main__':
    password = tstr('1234', taint='NOT_EXACTLY_SECRET')
    x = tint(password)

if __name__ == '__main__':
    assert x == 1234

if __name__ == '__main__':
    assert x.taint == 'NOT_EXACTLY_SECRET'

### Exercise 2: Information Flow Testing

if __name__ == '__main__':
    print('\n### Exercise 2: Information Flow Testing')


