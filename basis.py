# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Venkatramanan Krishnamani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Basis():
    def __init__(self):
        self.donorExcitation = {'x': [], 'y': []}
        self.acceptorExcitation = {'x': [], 'y': []}
        self.donorEmission = {'x': [], 'y': []}
        self.acceptorEmission = {'x': [], 'y': []}
        self.lamp = {'x': [], 'y': []}
        self.background = {'x': [], 'y': []}
        self.lampIntensityRatio = 0.0
        self.correctionFactor = 0.0
        self.donorName = ''
        self.acceptorName = ''
        self.backgroundName = ''

    def setDonorEx(self, x, y):
        self.donorExcitation['x'] = x
        self.donorExcitation['y'] = y

    def setAcceptorEx(self, x, y):
        self.acceptorExcitation['x'] = x
        self.acceptorExcitation['y'] = y

    def setDonorEm(self, x, y, name):
        self.donorEmission['x'] = x
        self.donorEmission['y'] = y
        self.donorName = name

    def setAcceptorEm(self, x, y, name):
        self.acceptorEmission['x'] = x
        self.acceptorEmission['y'] = y
        self.acceptorName = name

    def setBackground(self, x, y, name):
        self.background['x'] = x
        self.background['y'] = y
        self.backgroundName = name
