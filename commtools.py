#!/usr/bin/env python3
# coding: utf-8
import time

def dateFormat(strtime):
    x = time.localtime(strtime)
    return time.strftime('%Y-%m-%d %H:%M:%S', x)