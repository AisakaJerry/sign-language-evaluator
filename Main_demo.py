import json
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import shutil

# Ground Truth video path
# GT_PATH = './keypoint_gt'
# input1 模板路径

# User input video path
# USER_PATH = './keypoint_maple_gt'
# input2 #输入路径

tmpa = './keypoint_gt'
tmpb = './keypoint_maple_gt'
gtv='D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\sample\\fly.mp4'
usev='D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\sample\zebra.mp4'

#GTV_PATH='D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\sample\\fly'
#USERV_PATH='D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\sample\\zebra'
# Define your block window's size here
BLOCK_SIZE = [100, 200]
# For debugging: Show which joint in the output image
DEMO_JOINT_NUM = 12
# Threshold value with which you decide if the difference of number of samples between two blocks are too much
SAMPLE_DIFF = 20
# Threshold value, with this you can decide the mismatch keypoint ratio among 21 keypoints, e.g. 5 mismatches in 21 means overall mismatch
CORRECT_THRESHOLD = 5
plot1 = []
plot2 = []
gt_left, gt_right = [], []
usr_left, usr_right = [], []


def get_json_name(file_path):
    lis = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                lis.append(file_path + '/' + file)
    return lis


'''
UNUSED FUNCTION

def isClose(user_curr, gt_grad, num):
    # judge if the two direction vectors are in the range of the threshold
    # user_curr:     current user keypoint direction vector
    # gt_grad:  ground truth direction list
    # num:      the number of gt direction list
    if num >= len(gt_grad):
        return 2
    gt_curr = gt_grad[num]
    return 1
'''


def get_hand_path(hand_series):
    # In this function, input hand series list, output the block info of each defined windows and the info of zero frames.
    # the block_info is formed like this:
    # e.g. [+1, 0, 12],
    # +1 means the block moving 1 unit along x axis,
    # 0 means the block moving 0 unit among y axis,
    # 12 means the number of sample in this block

    block_info = []
    # remove all the zero frame in hand_series
    zeros = [0] * 42
    zero_log = []
    if zeros in hand_series:
        for i in range(len(hand_series)):
            if hand_series[i] == zeros:
                zero_log.append(i)
        hand_series.remove(zeros)
    # create hand_path to store all 21 joint paths
    hand_path = []
    for joint in range(0, 21):
        joint_path = []
        first_flag = True
        for i in range(len(hand_series)):
            hand_joint = [hand_series[i][2 * joint],
                          hand_series[i][2 * joint + 1]]  # the 2-D coordinate of each hand joint
            if first_flag:
                first_flag = False
                block_info = [0, 0, 1]
                last_hand_joint = hand_joint
            else:
                differ_x = hand_joint[0] - last_hand_joint[0]
                differ_y = hand_joint[1] - last_hand_joint[1]
                if (abs(differ_x) > BLOCK_SIZE[0]) or (abs(differ_y) > BLOCK_SIZE[1]):
                    joint_path.append(block_info)  # save old block_info
                    last_hand_joint = hand_joint
                    if abs(differ_x) > BLOCK_SIZE[0]:
                        if differ_x > 0:
                            sign_x = 1
                        else:
                            sign_x = -1
                    else:
                        sign_x = 0
                    if abs(differ_y) > BLOCK_SIZE[1]:
                        if differ_y > 0:
                            sign_y = 1
                        else:
                            sign_y = -1
                    else:
                        sign_y = 0
                    block_info = [sign_x, sign_y, 1]
                else:
                    block_info[2] += 1
        if joint_path == []:
            joint_path.append(block_info)

        hand_path.append(joint_path)

    return hand_path, zero_log


def evaluate(gt_hand_series, usr_hand_series):
    # evaluate the difference between ground truth moving path and the user input
    # PRE-REQIEMENT:
    # Start frame of user input should be aligned with ground truth.
    # output 'x' means not fit
    # output '=' means fit
    # output '?' means no keypoint found

    gt_hand_path, zero_log_gt = get_hand_path(gt_hand_series)
    usr_hand_path, zero_log_usr = get_hand_path(usr_hand_series)

    result = [""] * 21

    print(gt_hand_path[11])
    print("--------")
    print(usr_hand_path[11])
    # compare user_hand_path with gt_hand_path
    for joint_num in range(len(usr_hand_path)):
        ptr = 0
        finish_flag = False
        cp_block = gt_hand_path[joint_num][ptr]  # current_pointer_block
        for block in usr_hand_path[joint_num]:
            if finish_flag == True:
                result[joint_num] = result[joint_num] + 'x' * block[2]
                continue
            if (block[0] == cp_block[0]) and (block[1] == cp_block[1]):
                if 0 < (cp_block[2] - block[2]) < SAMPLE_DIFF:  # user sample too little
                    result[joint_num] = result[joint_num] + 'x' * block[2]
                    continue
                else:
                    result[joint_num] = result[joint_num] + '=' * block[2]
            else:
                result[joint_num] = result[joint_num] + 'x' * block[2]
            ptr += 1
            if len(gt_hand_path[joint_num]) > ptr:
                cp_block = gt_hand_path[joint_num][ptr]
            else:
                finish_flag = True

    # combine 21 joint results
    final_result = ""

    min_l = 600  # just set a large number
    for i in range(len(result)):
        if len(result[i]) < min_l:
            min_l = len(result[i])
    for i in range(min_l):
        counter = 0
        for each in result:
            if each[i] == '=':
                counter += 1
        if counter >= CORRECT_THRESHOLD:
            final_result += '='
        else:
            final_result += 'x'

    # recover zero frames
    for pos in zero_log_usr:
        final_result = final_result[:pos] + '?' + final_result[pos:]  # insert '?' in zero frames output
    return final_result, result


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print
        "---  new folder...  ---"
        print
        "---  OK  ---"

    else:
        print
        "---  There is this folder!  ---"



def writeimage(Video_Path,Save_Path):
    # temp = Video_Path.rfind('.')
    #
    # Save_Path = Video_Path[0:temp]
    # mkdir(Save_Path)
    # Save_Path =Save_Path  + '\\'
    print("check point writeimage rot")
    print(Save_Path)
    print(Video_Path)
    print("check point writeimage rot done done done")

    vc = cv2.VideoCapture(Video_Path)  # 读入视频文件
    c = 0
    rval = vc.isOpened()

    while rval:  # 循环读取视频帧
        c = c + 1
        rval, frame = vc.read()
        #print(type(rval))
        #print(type(frame))
        #pic_path = 'D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\pic/'
        if rval:
            cv2.imwrite(Save_Path + str(c) + '.jpg', frame)  # 存储为图像,保存名为 文件夹名_数字（第几个文件）.jpg
            cv2.waitKey(1)
        else:
            break

    vc.release()
    return Save_Path

def start(GT_PATH, USER_PATH,GTV_PATH,USERV_PATH):
    print(os.getcwd())
    Gwrite_PATH  =os.getcwd()+'/model/'
    shutil.rmtree(Gwrite_PATH)
    mkdir(Gwrite_PATH)
    print("check 1")
    print(Gwrite_PATH)

    Uwrite_PATH  =os.getcwd()+'/user/'
    shutil.rmtree(Uwrite_PATH)
    mkdir(Uwrite_PATH)
    print(Uwrite_PATH)
    # print(GTV_PATH)
    # print(USERV_PATH)

    print("check3")
    writeimage(USERV_PATH,Uwrite_PATH)
    print("user chop done")
    writeimage(GTV_PATH,Gwrite_PATH)
    print("model chop done")

    print("check 2")
    # GTV_PATH = 'D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\\right'
    # USERV_PATH = 'D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\\wrong'
    # get ground_truth pose keypoints
    gt_name = get_json_name(GT_PATH)
    # print(gt_name)


    ###
    for file in gt_name:
        with open(file) as json_file:
            data = json.load(json_file)
        left = data['people'][0]['hand_left_keypoints_2d']
        right = data['people'][0]['hand_right_keypoints_2d']
        # remove z axis data
        gt_left_l = []
        gt_right_l = []
        for i in range(len(left)):
            if i not in range(2, 63, 3):
                gt_left_l.append(left[i])
                gt_right_l.append(right[i])
        # remove the z-axis info
        gt_left.append(gt_left_l)
        gt_right.append(gt_right_l)
        plot1.append(
            [gt_right_l[DEMO_JOINT_NUM * 2], gt_right_l[DEMO_JOINT_NUM * 2 + 1]])  # save the midfinfer path for test

    #####
    # get user pose keypoints
    #####

    user_name = get_json_name(USER_PATH)
    # print(user_name)
    for file in user_name:
        with open(file) as json_file:
            data = json.load(json_file)
        left = data['people'][0]['hand_left_keypoints_2d']
        right = data['people'][0]['hand_right_keypoints_2d']
        # remove z axis data
        usr_left_l = []
        usr_right_l = []
        for i in range(len(left)):
            if i not in range(2, 63, 3):
                usr_left_l.append(left[i])
                usr_right_l.append(right[i])
        # remove the z-axis info
        usr_left.append(usr_left_l)
        usr_right.append(usr_right_l)
        plot2.append([usr_right_l[DEMO_JOINT_NUM * 2], usr_right_l[DEMO_JOINT_NUM * 2 + 1]])

    right_out, part_right_out = evaluate(gt_right, usr_right)


    # print("check3")
    # writeimage(USERV_PATH,Uwrite_PATH)
    # print("user chop done")
    # writeimage(GTV_PATH,Gwrite_PATH)
    # print("model chop done")

    print(right_out)
    return right_out

# def start(GT_PATH, USER_PATH):
#     print(GT_PATH)
#     print(USER_PATH)
#     result = "xxxxxxx=======???????====="
#     return result

#start(tmpa, tmpb,gtv,usev)


# a='D:\gwu\hg\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare/user/'
# b='D:\gwu\hg\openpose-1.4.0-win64-gpu-binaries/openpose-1.4.0-win64-gpu-binaries/compare/cabbage_user.mp4'
# writeimage(b,a)


#1125
# D:
# cd D:\study\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose
# #清空output
# bin\OpenPoseDemo.exe --video D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\examples\media\cabbage_gt.mp4 --face --hand --write_json ./output

def inputVideo(videoPath):
    cmd = 'D: &\
    cd D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose &\
    rmdir /s/q D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output &\
    bin\OpenPoseDemo.exe --video ' + videoPath + ' --face --hand --write_json ./output'
    print(cmd)
    os.system(cmd)
    outadd='D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output'
    return outadd #返回处理完成后的文件夹