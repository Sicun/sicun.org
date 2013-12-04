#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import models
import handlers

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(models.suite())
    runner.run(handlers.suite())
