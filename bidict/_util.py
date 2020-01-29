# -*- coding: utf-8 -*-
# Copyright 2009-2020 Joshua Bronson. All Rights Reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


"""Useful functions for working with bidirectional mappings and related data."""

from itertools import chain, repeat
from typing import Iterable, Mapping, Tuple, Union

from ._abc import KT, VT


_NULL_IT = repeat(None, 0)  # repeat 0 times -> raise StopIteration from the start


IterPair = Iterable[Tuple[KT, VT]]
MapOrIterPair = Union[Mapping[KT, VT], IterPair]


def _iteritems_mapping_or_iterable(arg: MapOrIterPair) -> IterPair:
    """Yield the items in *arg*.

    If *arg* is a :class:`~collections.abc.Mapping`, return an iterator over its items.
    Otherwise return an iterator over *arg* itself.
    """
    return iter(arg.items() if isinstance(arg, Mapping) else arg)


def _iteritems_args_kw(*args: MapOrIterPair, **kw) -> IterPair:
    """Yield the items from the positional argument (if given) and then any from *kw*.

    :raises TypeError: if more than one positional argument is given.
    """
    args_len = len(args)
    if args_len > 1:
        raise TypeError(f'Expected at most 1 positional argument, got {args_len}')
    itemchain = None
    if args:
        arg = args[0]
        if arg:
            itemchain = _iteritems_mapping_or_iterable(arg)
    if kw:
        iterkw = iter(kw.items())
        itemchain = chain(itemchain, iterkw) if itemchain else iterkw
    return itemchain or _NULL_IT  # type: ignore


def inverted(arg: MapOrIterPair) -> IterPair:
    """Yield the inverse items of the provided object.

    If *arg* has a :func:`callable` ``__inverted__`` attribute,
    return the result of calling it.

    Otherwise, return an iterator over the items in `arg`,
    inverting each item on the fly.

    *See also* :attr:`bidict.BidirectionalMapping.__inverted__`
    """
    inv = getattr(arg, '__inverted__', None)
    if callable(inv):
        return inv()
    return ((val, key) for (key, val) in _iteritems_mapping_or_iterable(arg))
