#!/usr/bin/env python
# coding: utf-8

import os
import json
import curses
import time
import requests
import configparser

PAUSE = ''
TIMEOUT = ''
MAIN_NODE = ''
STANDARD_NODES = ''
LATEST_BLOCK = {}

def get_data():
    return('s')

def refresh():
    pass

if __name__ == "__main__":
    config = configparser.ConfigParser()
    try:
        config.read('config')
    except Exception as e:
        print(e)
    else:
        default = config['DEFAULT']
        PAUSE = default.get('PAUSE') or 5
        TIMEOUT = default.get('TIMEOUT') or 30
        MAIN_NODE = default.get('MAIN_NODE') or 'http://35.183.49.71:8888'
        STANDARD_NODES = default.get('STANDARD_NODES').split(',') or ['https://api.eostitan.com']
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    try:
        print(get_data())
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
