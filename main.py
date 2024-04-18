import pyautogui
import ddddocr
import time
from datetime import datetime

ocr = ddddocr.DdddOcr()
init_time = time.time()


def get_screenshot(left_x, left_y, right_x, right_y, file_name='screenshot'):
    pyautogui.screenshot()

    region = pyautogui.screenshot(region=(left_x, left_y, right_x - left_x, right_y - left_y))
    region.save(file_name + '.png')


def get_sure_area():
    # 获取验证码区域的确定按钮，有的话说明验证码弹出来了
    get_screenshot(933, 552, 993, 586, "sure")
    with open("sure.png", 'rb') as f:
        img = f.read()
    sure = ocr.classification(img)
    return sure


sleep_second = 10
PROGRAM_TIMES = 2 * 60 * 60
count = 0
error_count = 0
while True:
    pyautogui.moveTo(1005, 541)
    pyautogui.vscroll(10)

    get_screenshot(1232, 258, 1280, 285, file_name="ok_position")
    with open("ok_position.png", 'rb') as f:
        img = f.read()
    res = ocr.classification(img)
    print("==== 执行时间" + str(datetime.now()) + " ====")
    if res == 'ok':
        pyautogui.click(1235, 271)
        print("点击长时间未操作按钮成功")
    sure = get_sure_area()
    if sure == "确定":
        out = False
        while not out:
            print("填写验证码结果")
            # 拿到验证码区域
            get_screenshot(999, 486, 1117, 523, "qrCode")
            with open("qrCode.png", 'rb') as f:
                img = f.read()
            res = ocr.classification(img)
            if res[0].isdigit() and res[2].isdigit():
                calculate = int(res[0]) + int(res[2])
            else:
                if error_count > 4:
                    print("====验证码识别错误次数超过四次，退出程序====")
                    exit(0)
                error_count += 1
                time.sleep(2)
                continue
            print("计算结果：" + str(calculate))
            pyautogui.click(885, 506)
            pyautogui.write(str(calculate))
            pyautogui.click(970, 572)
            time.sleep(1)
            out = get_sure_area() != '确定'

    if time.time() - init_time > PROGRAM_TIMES:
        break
    count += 1    
    if count % 20 == 0:
        pyautogui.vscroll(-190)   
    time.sleep(sleep_second)
