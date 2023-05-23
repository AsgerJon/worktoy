"""The billions2one function generates random objects"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from random import randint, uniform, choice
import string

from worktoy.core import maybe, CallMeMaybe, plenty


def randStr(n: int = None) -> str:
  """From ascii_letters random choice"""
  n = 16 if n is None else n
  base = [char for char in string.ascii_uppercase]
  base += [char for char in string.digits]
  out = []
  while len(out) < n:
    out.append(choice(base))
  return ''.join(out)


def randKeys(*keys, ) -> list[str]:
  """Random keyword arguments. Add strings to definitely include those
  keys"""
  n = None
  out = []
  for key in keys:
    if isinstance(key, int) and n is None:
      n = key
    else:
      out.append(key)
  n = maybe(n, 16)
  while len(out) < n:
    out.append(randStr(randint(8, 16)))
  return out


def randList(*args, **kwargs) -> list:
  """Returns a list n instances of type_"""
  type_ = kwargs.get('type', None)
  n = kwargs.get('n', None)
  for arg in args:
    if isinstance(arg, type) and type_ is None:
      type_ = arg
    if isinstance(arg, int) and n is None:
      n = arg
    if plenty(type_, n):
      break
  if type_ is not None:
    if not isinstance(type_, type):
      pass


def randDict(*keys) -> dict:
  """Creates a random dictionary at a given length and with a particular
  type. Include strings that will be used as keys. Otherwise, random keys
  are chosen."""
  type_, n = None, None
  for key in keys:
    if isinstance(key, type) and type_ is None:
      type_ = key
    if isinstance(key, int) and n is None:
      n = key
    if plenty(type_, n):
      break
  if not isinstance(type_, type) and type_ is not None:
    msg = """Expected type to be of type type (lol), but received : %s"""
    raise TypeError(msg % type_)
  if not isinstance(n, int) and n is not None:
    msg = """Expected n to be of type int, but received : %s"""
    raise TypeError(msg % n)
  n = 16 if n is None else n
  type_ = int if type_ is None else type_
  rng = getData(type_, )
  keys = randKeys(n, *keys)
  out = {}
  if rng is None:
    raise ValueError('Expected a type but received %s' % (type_))
  for key in keys:
    out |= {key: rng()}
  return out


builtin_types = {
  int  : {"__name__": "int", "sampleGen": lambda: randint(-100, 100)},
  float: {
    "__name__" : "float",
    "sampleGen": lambda: uniform(-100.0, 100.0)},
  bool : {
    "__name__" : "bool",
    "sampleGen": lambda: choice([True, False])},
  str  : {"__name__": "str", "sampleGen": randStr},
  list : {"__name__": "list", "sampleGen": lambda: []},
  tuple: {"__name__": "tuple", "sampleGen": lambda: ()},
  dict : {"__name__": "dict", "sampleGen": lambda: {}},
}


def getData(type_: type) -> CallMeMaybe:
  """Getter for the data"""
  if not isinstance(type_, type):
    msg = """Expected type to be of type type (lol), but received : %s"""
    raise TypeError(msg % type_)
  for (key, val) in builtin_types.items():
    name = val.get('__name__', None)
    if name is not None:
      if name == type_.__name__:
        rng = val.get('sampleGen', None)
        if rng is None:
          raise ValueError('Did not find random generator')
        return rng
  raise NameError('Did not find a type matching: %s' % type_)