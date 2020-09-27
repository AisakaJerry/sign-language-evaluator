import os

command1='D:'
command2='cd D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose'
command3='rmdir /s/q D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output'
command4='bin\OpenPoseDemo.exe --video D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\examples\media\cabbage_gt.mp4 --face --hand --write_json ./output'
command='D: &\
cd D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose &\
rmdir /s/q D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output &\
bin\OpenPoseDemo.exe --video D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\examples\media\cabbage_gt.mp4 --face --hand --write_json ./output  '

#os.system(command)

#命令拼接
testPath='D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\examples\media\kangaroo.mp4'
# cmd='D: &\
# cd D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose &\
# rmdir /s/q D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output &\
# bin\OpenPoseDemo.exe --video ' + videoPath + ' --face --hand --write_json ./output'

# print(cmd)
# os.system(cmd)

def inputVideo(videoPath):
    cmd = 'D: &\
    cd D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose &\
    rmdir /s/q D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output &\
    bin\OpenPoseDemo.exe --video ' + videoPath + ' --face --hand --write_json ./output'
    print(cmd)
    os.system(cmd)
    outadd='D:\study\\6221\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\openpose\output'
    return outadd #返回处理完成后的文件夹


inputVideo(testPath)