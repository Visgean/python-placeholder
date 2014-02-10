#!/usr/bin/python
# -*- coding: utf-8 -*-

# placeholder.py --- short description
#
# Copyright  (C)  2010  Martin Marcher <martin@marcher.name>
#
# Version:
# Keywords:
# Author: Martin Marcher <martin@marcher.name>
# Maintainer: Martin Marcher <martin@marcher.name>
# URL: http://
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Commentary:

__author__ = u'Martin Marcher'
__version__ = u''
__docformat__ = u'restructuredtext en'


import os
import sys
import logging
import unittest

from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont
from PIL import ImageOps

class Size(Base):
    u"""Simple wrapper to hold a size.
    """

    def __init__(self, width, height):
        u"""Creates a new size object which holds the given ``width`` and ``height``.

        :Arguments:
        - `width`:
        - `height`:
        """
        Base.__init__(self)

        # make sure the parameters actually are integers
        self._width = int(width)
        self._height = int(height)
        
    @property
    def width():
        def fget(self):
            return self._width
        return locals()
    @property
    def height():
        def fget(self):
            return self._height
        return locals()
    def __repr__(self):
        u"""Simple Identifier for the Size instance.
        """
        return u"<%s Object (%dx%d)>" % (self._name,
                                         self._width,
                                         self._height, )
    def __iter__(self):
        u"""Part of the implementation of the iterator protocol.
        """
        yield self._width
        yield self._height
    def __getitem__(self, key):
        u"""Part of the implementation of the sequence protocol.
        """
        if key == 0:
            return self._width
        if key == 1:
            return self._height
        else:
            raise IndexError(u'list index out of range')
    def __len__(self):
        u"""Part of the implementation of the sequence protocol.
        """
        return len((self._width, self._height, ))
    def __min__(self):
        u"""Part of the implementation of the sequence protocol.
        """
        return min(self._width, self._height)
    def __max__(self):
        u"""Part of the implementation of the sequence protocol.
        """
        return max(self._width, self._height)


class TestSize(unittest.TestCase):
    u"""Tests the ``Size`` class.
    """
    def test_width(self):
        s = Size(1, 2)
        self.failUnlessEqual(s.width, 1)
    def test_height(self):
        s = Size(1, 2)
        self.failUnlessEqual(s.height, 2)
    def test_iter(self):
        self.assertEqual(list(Size(1, 2)), [1, 2, ])
    def test_slice0(self):
        Size(1, 2)[0]
    def test_slice1(self):
        Size(1, 2)[1]
    def test_IndexError(self):
        def slice():
            return Size(1, 2)[2]
        self.assertRaises(IndexError, slice)
    def test_min(self):
        self.assertEqual(min(Size(1, 2)), 1)
    def test_max(self):
        self.assertEqual(max(Size(1, 2)), 2)


class Color(Base):

    COLORMAP = ImageColor.colormap
    MODE = u'RGBA'

    BLACK = ImageColor.getrgb(u'black')
    WHITE = ImageColor.getrgb(u'white')

    RED = ImageColor.getrgb(u'red')
    GREEN = ImageColor.getrgb(u'green')
    BLUE = ImageColor.getrgb(u'blue')

    def __getattribute__(self, name):
        try:
            return Color.COLORMAP[name]
        except (KeyError, ) as error:
            return Base.__getattribute__(self, name)

    # def __get__(self, instance, owner):
    #     try:
    #         return ImageColor.colormap[name]
    #     except (KeyError, ) as error:
    #         return Base.__get__(self, instance, owner)


class TestColor(unittest.TestCase):
    u"""Test the ``Color`` class.
    """

    def test_black(self):
        self.assertEqual(Color.BLACK, ImageColor.getrgb(u'black'))
    def test_white(self):
        self.assertEqual(Color.WHITE, ImageColor.getrgb(u'white'))
    def test_red(self):
        self.assertEqual(Color.RED, ImageColor.getrgb(u'red'))
    def test_green(self):
        self.assertEqual(Color.GREEN, ImageColor.getrgb(u'green'))
    def test_blue(self):
        self.assertEqual(Color.BLUE, ImageColor.getrgb(u'blue'))
    def test_all_colors(self):
        u"""Test all defined colors from PIL
        """
        c = Color()
        for elem in ImageColor.colormap:
            self.assertEqual(ImageColor.colormap[elem], getattr(c, elem))

class PlaceHolderImage(Base):
    u"""Create an image useable for wireframing webistes.
    """

    def __init__(self, width, height,
                 fg_color=Color.BLACK,
                 bg_color=Color.WHITE,
                 text=None,
                 font=u'Verdana.ttf',
                 fontsize=24,
                 encoding=u'unic',
                 mode=Color.MODE,
                 fmt=u'PNG'):
        u"""Creates a new Placeholder Image
        """
        Base.__init__(self)
        self._width = width
        self._height = height
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._text = text
        self._font = font
        self._fontsize = fontsize
        self._encoding = encoding

        self._size = Size(self._width, self._height)
        self._mode = mode
        self._fmt = fmt

    def save(self):

        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(delete=False) as target:
            result_img = Image.new(self._mode, self._size, self._bg_color)
            img_width, img_height = result_img.size

            self.log.debug(u'result_img.size: %r, self._size: %r',
                           result_img.size, self._size)

            if self._text is None:
                self._text = "x".join([str(n) for n in self._size])
            if self._text is not None:
                try:
                    font = ImageFont.truetype(
                        self._font,
                        size=self._fontsize,
                        encoding=self._encoding)
                except (IOError, ) as error:
                    font = ImageFont.load_default()

                self.log.debug(u'The text is: %r', self._text)
                txt_size = Size(*font.getsize(self._text))
                self.log.debug(u'Text Size: %r', txt_size)
                txt_img = Image.new("RGBA", self._size, self._bg_color)
                self.log.debug(u'Size of txt_img: %r', txt_size)

                drawing = ImageDraw.Draw(txt_img)
                left = self._size.width/2 - txt_size.width/2
                top = self._size.height/2 - txt_size.height/2
                drawing.text((left, top, ),
                             self._text,
                             font=font,
                             fill=self._fg_color)



                txt_img = ImageOps.fit(txt_img,
                                       result_img.size,
                                       method=Image.BICUBIC,
                                       centering=(0.5, 0.5)
                                   )
                result_img.paste(txt_img)
            # result_img.show()
            # sys.exit(1)
            txt_img.save(target, self._fmt)
            self.log.debug(u'Wrote Image to: %r', target.name)
            del(result_img)
        return target.name


class TestPlaceHolderImage(unittest.TestCase):
    u"""Tests the ``PlaceHolderImage`` class.
    """
    def test_save(self):
        i = PlaceHolderImage(640, 480)
        i.save()
    def test__txt_img(self):
        # c = Color()
        # i = PlaceHolderImage(640, 480, c.gray)
        # i._txt_img()
        pass

