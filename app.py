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
STANDARD_NODE = ''
LATEST_BLOCK = {}

def get_block(node, main=False, write=True):
    try:
        block = requests.get(node + '/v1/chain/get_info')
    except Exception as e:
        print(e)
    else:
        if write:
            if main:
                LATEST_BLOCK['main'] = block.json()['head_block_num']
            else:
                LATEST_BLOCK['standard'] = block.json()['head_block_num']
        return block.json()['head_block_num']


def get_acceleration(node, main=False):
    block = get_block(node, write=False) if not main else get_block(node, main=True, write=False)

    return block - LATEST_BLOCK['main'] if main else block - LATEST_BLOCK['standard']

def get_data():
    standard_node_blocks = get_block(STANDARD_NODE)
    main_node_blocks = get_block(MAIN_NODE, main=True)
    time.sleep(PAUSE)
    # TODO make for more than 1 node
    standard_acceleration = get_acceleration(STANDARD_NODE)
    main_acceleration = get_acceleration(MAIN_NODE, main=True)

    return standard_node_blocks, main_node_blocks, round(main_node_blocks/standard_node_blocks*100, 5), standard_acceleration, main_acceleration

def refresh(std_node_blocks, main_node_blocks, ratio, std_acceleration, main_acceleration):
    screen.addstr(0,0, "%s node head block: %s (acceleration: %s new blocks per %s seconds)" % (STANDARD_NODE, std_node_blocks, std_acceleration, PAUSE))
    screen.addstr(1, 0, "%s node head block: %s (acceleration: %s new blocks per %s seconds)" % (MAIN_NODE, main_node_blocks, main_acceleration, PAUSE))
    screen.addstr(2, 0, "%s node status: %s %%" % (MAIN_NODE, ratio))
    screen.refresh()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    try:
        config.read('config')
    except Exception as e:
        print(e)
    else:
        default = config['DEFAULT']
        PAUSE = int(default.get('PAUSE')) or 5
        TIMEOUT = int(default.get('TIMEOUT')) or 30
        MAIN_NODE = default.get('MAIN_NODE') or 'http://35.183.49.71:8888'
        STANDARD_NODE = default.get('STANDARD_NODE') or 'https://api.eostitan.com'
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    try:
        while True:
            std_node_blocks, main_node_blocks, ratio, std_acceleration, main_acceleration = get_data()
            refresh(std_node_blocks, main_node_blocks, ratio, std_acceleration, main_acceleration)
            time.sleep(1)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
