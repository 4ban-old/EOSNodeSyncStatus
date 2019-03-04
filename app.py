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
    if not main:
        blocks = []
        for x in node:
            try:
                block = requests.get(x + '/v1/chain/get_info')
            except Exception as e:
                print(e)
            else:
                blocks.append(block.json()['head_block_num'])
        if write:
            LATEST_BLOCK['standard'] = blocks
        return blocks
    else:
        try:
            block = requests.get(node + '/v1/chain/get_info')
        except Exception as e:
            print(e)
        else:
            if write:
                LATEST_BLOCK['main'] = block.json()['head_block_num']
            return block.json()['head_block_num']


def get_acceleration(node, main=False):
    if main:
        block = get_block(node, main=True, write=False)
        return block - LATEST_BLOCK['main']
    else:
        blocks = get_block(node, write=False)
        accelerations = []
        if len(LATEST_BLOCK['standard']) == len(blocks):
            for i, x in enumerate(blocks):
                accelerations.append(x - LATEST_BLOCK['standard'][i])
        return accelerations

def get_data():
    standard_node_blocks = get_block(STANDARD_NODE)
    main_node_blocks = get_block(MAIN_NODE, main=True)
    time.sleep(PAUSE)

    standard_acceleration = get_acceleration(STANDARD_NODE)
    main_acceleration = get_acceleration(MAIN_NODE, main=True)

    return standard_node_blocks, main_node_blocks, round(main_node_blocks/standard_node_blocks[0]*100, 5), standard_acceleration, main_acceleration

def refresh(std_node_blocks, main_node_blocks, ratio, std_acceleration, main_acceleration):
    for index, node in enumerate(std_node_blocks):
        screen.addstr(index,0, "Head block: %s (acceleration: %s new blocks per %s seconds) for %s" % (node, std_acceleration[index], PAUSE, STANDARD_NODE[index]))
    screen.addstr(len(std_node_blocks)+1, 0, "#####################################################")
    screen.addstr(len(std_node_blocks)+2, 0, "Head block: %s (acceleration: %s new blocks per %s seconds) for %s" % (main_node_blocks, main_acceleration, PAUSE, MAIN_NODE))
    screen.addstr(len(std_node_blocks)+3, 0, "Node status: %s %% for %s" % (ratio, MAIN_NODE))
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
        STANDARD_NODE = default.get('STANDARD_NODE').split(',') or 'https://api.eostitan.com'
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    try:
        while True:
            std_node_blocks, main_node_blocks, ratio, std_acceleration, main_acceleration = get_data()
            refresh(std_node_blocks, main_node_blocks, ratio, std_acceleration, main_acceleration)
            time.sleep(1)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
