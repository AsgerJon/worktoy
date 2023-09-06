"""WorkToy - Core
The core module provides the chain of default classes:
  'PrimitiveClass'
  'ParsingClass'
  'ExceptionClass'
  '...'
  'DefaultClass'
The final class should be called DefaultClass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._coretypes import Map, Keys, Values, Items, Bases, Type
from ._coretypes import Function, Method, WrapperDescriptor
from ._coretypes import WrapperMethod, BuiltinFunction, Functional
from ._coretypes import FunctionTuple, FunctionList
from ._coretypes import ARGS, KWARGS, RESULT, CALL
from ._constants import PI, factorial
from ._constants import loremSample
from ._function_decorator import FunctionDecorator
