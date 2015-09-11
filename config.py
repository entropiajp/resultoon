# -*- coding: utf-8 -*-

import ConfigParser


ini = ConfigParser.SafeConfigParser()
ini.read('resultoon.ini')

CAPTURE_BOARD_DEVICE_ID = int(ini.get('resultoon', 'capture_board_device_id'))
GOOGLE_APPS_SCRIPT_URL = ini.get('resultoon', 'google_apps_script_url')
SAVE_IMAGE_PATH = ini.get('resultoon', 'save_image_path')

RULES = ['ガチエリア', 'ガチヤグラ', 'ガチホコ']
STAGES = ['デカライン高架下', 'シオノメ油田', 'Bバスパーク', 'ハコフグ倉庫', 'アロワナモール',
          'ホッケふ頭', 'モズク農園', 'ネギトロ炭鉱', 'タチウオパーキング', 'モンガラキャンプ場', 'ヒラメが丘団地']
