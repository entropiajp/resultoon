# -*- coding: utf-8 -*-

import datetime

import numpy as np
import cv2
import tesseract
import requests

import config


rightup_template = cv2.imread("./templates/result_upright_binary.bmp", cv2.IMREAD_GRAYSCALE)

numbers = []
for x in xrange(10):
    img = cv2.imread('./templates/numbers/binarized/' + str(x) + '.png', cv2.IMREAD_GRAYSCALE)
    ret, binary_img = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    numbers.append(binary_img)

rule_tpls = [cv2.imread('./templates/rules/area.png', cv2.IMREAD_GRAYSCALE),
             cv2.imread('./templates/rules/yagura.png', cv2.IMREAD_GRAYSCALE),
             cv2.imread('./templates/rules/hoko.png', cv2.IMREAD_GRAYSCALE)]

stage_names = ['dekaline', 'sionome', 'bbus', 'hakofugu', 'alowana',
               'hokke', 'mozuku', 'negitoro', 'tachiuo', 'mongara',
               'hirame', 'masaba', 'kinmedai', 'mahimahi', 'shotturu']
stage_tpls = [cv2.imread('./templates/stages/' + name + '.png', cv2.IMREAD_GRAYSCALE)
              for name in stage_names]

cap = cv2.VideoCapture(config.CAPTURE_BOARD_DEVICE_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

display_info = {}  # 画面に表示したい情報


def send_to_google_spreadsheet(payload):
    headers = {'content-type': 'application/json'}
    r = requests.post(config.GOOGLE_APPS_SCRIPT_URL, json=payload, headers=headers)
    print r.content


def get_all_kd(img):
    W = 12
    H = 18
    X = (1187, 1202)
    Y = [102, 167, 232, 297, 432, 497, 562, 627]
    kds = []
    for y in Y:
        kill = dict()
        death = dict()
        kill["10"] = get_digit(img[y:y+H, X[0]:X[0]+W])
        kill["1"] = get_digit(img[y:y+H, X[1]:X[1]+W])
        y2 = y + 21
        death["10"] = get_digit(img[y2:y2+H, X[0]:X[0]+W])
        death["1"] = get_digit(img[y2:y2+H, X[1]:X[1]+W])
        kds.append({"kill": kill["10"]*10 + kill["1"], "death": death["10"]*10 + death["1"]})
    return kds


def get_digit(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # 画面全体の輝度値合計がほとんど0なら数字なしとみなし、0を返す
    if binary_img.sum() < 10:
        return 0
    dist = [(binary_img - number).sum() for number in numbers]
    return dist.index(min(dist))


def get_coef_of_rightup_rect(img):
    """画面右上の特定領域を取得する"""
    cropped_gray_img = cv2.cvtColor(img[0:0+64, 1188:1188+64], cv2.COLOR_BGR2GRAY)
    # cv2.imshow('orig', cropped_gray_img)
    ret, temp = cv2.threshold(cropped_gray_img, 250, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow('rightup', temp)
    coef = cv2.matchTemplate(temp, rightup_template, cv2.TM_CCOEFF_NORMED)
    display_info["coef"] = np.array_str(coef[0])
    return coef[0]


def is_result(img):
    return get_coef_of_rightup_rect(img) > 0.95


def recognize_result_summary(img):
    W = 53
    H = 36
    X = 1027
    Y = [102, 167, 232, 297, 432, 497, 562, 627]
    imgs = [img[y:y+H, X:X+W] for y in Y]
    udemaes = [ocr_udemae(i) for i in imgs]
    kds = get_all_kd(img)
    player_index = identify_player(img)
    members = [{"udemae": udemae, "kill": kd["kill"], "death": kd["death"]} for udemae, kd in zip(udemaes, kds)]
    members[player_index]["isPlayer"] = True
    for i, m in enumerate(members):
        team = "win" if i < 4 else "lose"
        m.update({"team": team})
    return members


def identify_player(img):
    """リザルト画面のメンバーを上から順に0-7番として、プレイヤーに該当する番号を返す"""
    W = 36
    H = 36
    X = 616
    Y = [102, 167, 232, 297, 432, 497, 562, 627]
    imgs = [img[y:y+H, X:X+W] for y in Y]
    white_areas = [calc_white_area(img) for img in imgs]
    return white_areas.index(max(white_areas))


def calc_white_area(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    return binary_img.sum()


def is_opening(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if gray.sum() < 1000000:
        right_down_violet = img[590:690, 1140:1240]
        return right_down_violet.sum() > 100000


def recognize_stage_and_rule(img):
    # rule
    W = 300
    H = 60
    X = 489
    Y = 250
    gray = cv2.cvtColor(img[Y:Y+H, X:X+W], cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    dist = [(binary_img - tpl).sum() for tpl in rule_tpls]
    rule = config.RULES[dist.index(min(dist))]

    # stage
    W = 420
    H = 60
    X = 811
    Y = 582
    gray = cv2.cvtColor(img[Y:Y+H, X:X+W], cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    dist = [(binary_img - tpl).sum() for tpl in stage_tpls]
    stage = config.STAGES[dist.index(min(dist))]

    return {"stage": stage, "rule": rule}


def ocr_udemae(img):
    img = binarize(img)
    img = erode(img)
    # cv2.imshow('ocr_udemae', img)
    # cv2.waitKey(500)

    api = tesseract.TessBaseAPI()
    api.Init("C:\Program Files (x86)\Tesseract-OCR", "eng", tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist", "SABC+-")
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)

    cv_im = convert_to_IplImage(img)
    tesseract.SetCvImage(cv_im, api)
    return api.GetUTF8Text().split("\n")[0]  # OCR結果から余計な改行を取り除く


def ocr_number(img):
    api = tesseract.TessBaseAPI()
    api.Init("C:\Program Files (x86)\Tesseract-OCR", "eng", tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist", "0123456789+-")
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)

    cv_im = convert_to_IplImage(img)
    tesseract.SetCvImage(cv_im, api)
    return api.GetUTF8Text().split("\n")[0]  # OCR結果から余計な改行を取り除く


def recognize_result_udemae_point(img):
    cropped_img = img[206:206+64, 842:842+96]
    temp = binarize(cropped_img)
    temp = rotate_10_degree(temp)
    temp = erode(temp)
    # cv2.imshow('udemae', img)
    # cv2.waitKey(2000)
    udemae_diff = ocr_number(temp)

    cropped_img = img[382:382+64, 774:774+92]
    temp = binarize(cropped_img)
    temp = erode(temp)
    # cv2.imshow('udemae', temp)
    # cv2.waitKey(2000)
    udemae_point = ocr_number(temp)

    return {"udemae_diff": udemae_diff, "udemae_point": udemae_point}


def save_image(img):
    d = datetime.datetime.today()
    filename = "resultoon_" + d.strftime("%Y%m%d_%H%M%S") + ".png"
    cv2.imwrite(config.SAVE_IMAGE_PATH + filename, img)


def wait_and_display(frame_count):
    """指定フレームだけ画面描画のみ行う"""
    for x in xrange(frame_count):
        ret, frame = cap.read()
        frame = draw_info_on_display(frame)
        cv2.imshow('display', frame)
        k = cv2.waitKey(1)
        if k == 27:  # ESCキーで終了
            break
        if k == 32:  # spaceキーで画像保存
            save_image(frame)


def draw_info_on_display(frame):
    y = 1
    for item in display_info.items():
        cv2.putText(frame, item[0] + ": " + item[1], (10, y*50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 2, cv2.LINE_AA)
        y += 1
    return frame


def convert_to_IplImage(img):
    ipl_img = cv2.cv.CreateImageHeader((img.shape[1], img.shape[0]), cv2.cv.IPL_DEPTH_8U, 1)
    cv2.cv.SetData(ipl_img, img.tostring())
    return ipl_img


def binarize(img):
    if img.shape[2] != 1:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_image = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image


def erode(img):
    kernel = np.ones((4, 4), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    return erosion


def rotate_10_degree(img):
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 10, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))
    return dst


def main():

    result = dict()
    while cap.isOpened():
        ret, frame = cap.read()

        if is_opening(frame):
            wait_and_display(200)
            ret, frame = cap.read()
            result = recognize_stage_and_rule(frame)
            continue

        if is_result(frame):
            wait_and_display(30)
            ret, frame = cap.read()
            cv2.waitKey(1)
            cv2.imshow('summary', frame)
            save_image(frame)
            members = recognize_result_summary(frame)
            wait_and_display(380)
            ret, frame = cap.read()
            cv2.waitKey(1)
            cv2.imshow('udemae', frame)
            udemae_data = recognize_result_udemae_point(frame)
            result['udemae_point'] = udemae_data['udemae_point']
            result['udemae_diff'] = udemae_data['udemae_diff']
            result['members'] = members
            print result
            send_to_google_spreadsheet(result)
            result = dict()
            wait_and_display(60*20)
            continue

        frame = draw_info_on_display(frame)
        cv2.imshow('display', frame)
        k = cv2.waitKey(1)
        if k == 27:  # ESCキーで終了
            break
        if k == 32:  # spaceキーで画像保存
            save_image(frame)
        wait_and_display(10)

    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
