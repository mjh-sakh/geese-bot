#!/usr/bin/env python3
import logging

from bot.bot_core import run


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting bot.')
    run()


if __name__ == '__main__':
    main()
