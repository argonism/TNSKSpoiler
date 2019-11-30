import cv2
import os
import numpy as np
from natsort import natsorted
from tqdm import tqdm

# def detection(target, compare):

#     IMG_SIZE = (1000, 1000)

#     target_img = cv2.resize(target, IMG_SIZE)

#     bf = cv2.BFMatcher(cv2.NORM_HAMMING)
#     # detector = cv2.ORB_create()
#     detector = cv2.AKAZE_create()
#     (target_kp, target_des) = detector.detectAndCompute(target_img, None)
#     try:
#         comparing_img = cv2.resize(compare, IMG_SIZE)
#         (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
#         matches = bf.match(target_des, comparing_des)
#         dist = [m.distance for m in matches]
#         ret = sum(dist) / len(dist)
#     except cv2.error:
#         ret = 100000

#     return ret

# target_dir: hoge/fuge/
def save_selected_imgs(target_dir, paths):

    for i, path in enumerate(paths):
        print(path)
        img = cv2.imread(path)
        cv2.imwrite(target_dir + str(i) + ".png", img)


def background_subtranction(diffs, paths):
    remove_path = []
    for i in range(len(diffs)):
        if i == 0:
            continue
        back = cv2.absdiff(diffs[i], diffs[i-1])
        print(paths[i], np.linalg.norm(back))
        if np.linalg.norm(back) <= 13000:
            remove_path.append(paths[i-1])

    print("remove_path:", remove_path)
    return natsorted(set(paths) ^ set(remove_path))


def select_carefully(target_dir):
    IMG_SIZE = (500, 500)
    IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/' + target_dir + "/"
    files = natsorted(os.listdir(IMG_DIR))
    files = [file for file in files if file != ".DS_Store"]
    print(files)

    selected_imgs = []
    diffs = []
    for i in range(len(files)):
        if i == 0:
            continue
        else:
            pre_img_path = IMG_DIR + files[i - 1]
            pre_img = cv2.imread(pre_img_path)
            pre_img_resized = cv2.resize(pre_img, IMG_SIZE)

            img_path = IMG_DIR + files[i]
            img = cv2.imread(img_path)
            img_resized = cv2.resize(img, IMG_SIZE)

            diff = cv2.absdiff(pre_img_resized, img_resized)
            norm = np.linalg.norm(diff)
            # print(norm)
            if norm >= 10000:
                selected_imgs.append(files[i])
                diffs.append(diff)

    # スライドの切り替わりで、前後が透けてる画像の除外
    selected_img_paths = background_subtranction(diffs, selected_imgs)
    prefixec_paths = [IMG_DIR + path for path in selected_img_paths]

    save_selected_imgs(os.path.abspath(os.path.dirname(__file__)) + "/slides/", prefixec_paths)

def main_proccess(target_path):

    first_time = True
    cap = cv2.VideoCapture(target_path)

    pre_frame = None
    frame_sum = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(frame_sum)
    i = 0
    n = 0
    for i in tqdm(range(int(frame_sum))):
        ret, frame = cap.read()
        if not ret:
            break

        # 最初はpre_frameに入れてスキップ
        if first_time:
            pre_frame = frame
            first_time = False
            continue

        diff = cv2.absdiff(frame, pre_frame)
        norm = np.linalg.norm(diff)
        # print(norm)
        if(norm >= 14000):
        # if(norm <= 0.6):
            n += 1
            cv2.imwrite('result/out' + str(n) + ".png", frame)
            # print(str(n) + " saved!")

        pre_frame = frame

    cap.release()
    cv2.destroyAllWindows()

# main_proccess('img/Skyflow.MOV')
# select_carefully('result')