from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
import cv2
#import evaluate
from PIL import ImageTk,Image
import os
import urllib
import Main_demo
window = Tk()
window.title('Sign Language Helper')
window.geometry('1224x800')
window.configure(background='whitesmoke')
firstTime = True
modelPath = StringVar()
userPath = StringVar()
modelVideoPath = StringVar()
userVideoPath = StringVar()
setultTextbox = StringVar()


resultString = ''
GTV_PATH='D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\sample\\fly'
USERV_PATH='D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\sample\\zebra'


def selectModelPath():
    # path_ = askopenfilename()
    path_ = askdirectory()
    modelPath.set(path_)


def selectUserPath():
    # path_ = askopenfilename()
    path_ = askdirectory()
    userPath.set(path_)


def selectModelVideoPath():
    # path_ = askopenfilename()
    path_ = askopenfilename()
    modelVideoPath.set(path_)


def selectUserVideoPath():
    # path_ = askopenfilename()
    path_ = askopenfilename()
    userVideoPath.set(path_)



def showVideo1():
    videoCapture = cv2.VideoCapture(modelVideoPath.get())
    sucess, frame = videoCapture.read()
    while (sucess):
        sucess, frame = videoCapture.read()
        displayImg = cv2.resize(frame, (1024, 768))  # resize it to (1024,768)
        cv2.namedWindow('test Video')
        cv2.imshow("test Video", displayImg)
        keycode = cv2.waitKey(1)
        if keycode == 27:
            cv2.destroyWindow('test Video')
            videoCapture.release()
            break


def showVideo2():
    videoCapture = cv2.VideoCapture(userVideoPath.get())
    sucess, frame = videoCapture.read()
    while (sucess):
        sucess, frame = videoCapture.read()
        displayImg = cv2.resize(frame, (1024, 768))  # resize it to (1024,768)
        cv2.namedWindow('test Video')
        cv2.imshow("test Video", displayImg)
        keycode = cv2.waitKey(1)
        if keycode == 27:
            cv2.destroyWindow('test Video')
            videoCapture.release()
            break
def inputCurrentVideo():
    print(userVideoPath.get())
    Main_demo.inputVideo(userVideoPath.get())


def getResult():
    #
    # print(modelPath.get())
    # print(userPath.get())
    # eva = evaluate.start(modelPath.get(), userPath.get())
    # resultString = eva
    # print(resultString)
    frmn = Frame(frm_m)
    eva = Main_demo.start(modelPath.get(), userPath.get(), modelVideoPath.get(), userVideoPath.get())
    print('done1')
    resultString = eva
    print(resultString)
    modelPicDir = modelVideoPath.get()[0:modelVideoPath.get().rfind('.')]
    modelPicDir = modelPicDir + '/'
    print(modelPicDir)

    userPicDir = userVideoPath.get()[0:userVideoPath.get().rfind('.')] + '/'
    frmn1 = Frame(frm_m)
    # if firstTime==False:
    #     Label.destroy()
    for index in range(len(resultString)):
        if index % 24 == 0:
            time = int(index / 24)
            timeString = str(time) + 's'
            Label(frmn1, text=timeString, bg='LightGrey', width=1).pack(side=LEFT, anchor=W)
        else:
            Label(frmn1, text=".", bg='LightGrey', width=1).pack(side=LEFT, anchor=W)
    frmn1.pack(side=TOP, pady=2, anchor=N)
    frmn2 = Frame(frm_m)

    # if firstTime==False:
    #     Label.destroy()
    #     Label.forget()
    for index in range(len(resultString)):
        # Label(frm_b, bg='pink',width=2).pack(side=LEFT,anchor=W)
        if resultString[index] == 'x':
            Label(frmn2, text="x", bg='Tomato', width=1).pack(side=LEFT, anchor=W)
        if resultString[index] == '=':
            Label(frmn2, text="=", bg='PaleGreen', width=1).pack(side=LEFT, anchor=W)
        if resultString[index] == '?':
            Label(frmn2, text="?", bg='yellow', width=1).pack(side=LEFT, anchor=W)
    frmn2.pack(side=TOP, pady=2, anchor=N)
    setultTextbox.set(resultString)
    i = 1
    print('done2')
    videoLength = len(eva)
    print('done3')
    while i <= videoLength:
        # print(videoLength)
        lb.insert('end', i)
        i = i + 1
        # print(i)


canvas0 = Canvas(window, width=1024, height=20)
Label(canvas0, text='Sign Language Helper', font=('Google',20)).pack(anchor=CENTER, pady=4)

canvas0.pack()

canvas1 = Canvas(window,bg="whitesmoke", width=1024, height=164)
frm_top = Frame(canvas1)
frm_top.place(width=1024, height=180)  # frame的长宽，和canvas差不多的

# frm1=Frame(frm_top,bg="pink")
Label(canvas1, text="Model Directory:", width=16, relief=RAISED).grid(row=0, column=0, pady=6, sticky=W)
Label(canvas1, text="Your Directory:", width=16, relief=RAISED).grid(row=1, column=0, pady=6, sticky=W)
Label(canvas1, text="Model video:", width=16, relief=RAISED).grid(row=2, column=0, pady=6, sticky=W)
Label(canvas1, text="Your video:", width=16, relief=RAISED).grid(row=3, column=0, pady=6, sticky=W)
# frm1.pack(side=LEFT,anchor=W,padx=4,fill=Y)

# frm2=Frame(frm_top)

eva =''
Entry(canvas1, textvariable = modelPath, bg='whitesmoke',relief=RAISED).grid(row = 0, column = 1,pady=6,columnspan=15,ipadx=10)
Entry(canvas1, textvariable = userPath, bg='whitesmoke',relief=RAISED).grid(row = 1, column = 1,pady=6,columnspan=15,ipadx=10)
Entry(canvas1, textvariable = modelVideoPath, bg='whitesmoke',relief=RAISED).grid(row = 2, column = 1,pady=6,columnspan=15,ipadx=10)
Entry(canvas1, textvariable = userVideoPath, bg='whitesmoke',relief=RAISED).grid(row = 3, column = 1,pady=6,columnspan=15,ipadx=10)

# frm2.pack(side=LEFT,expand=YES,fill=BOTH,padx=4)

# frm3=Frame(frm_top)
Button(canvas1, text = "choose file", command = selectModelPath, bg='whitesmoke',width=10,relief=RAISED).grid(row = 0, column = 16)
Button(canvas1, text = "choose file", command = selectUserPath, bg='whitesmoke',width=10,relief=RAISED).grid(row = 1, column = 16)
Button(canvas1, text = "choose file", command = selectModelVideoPath, bg='whitesmoke',width=10,relief=RAISED).grid(row = 2, column = 16)
Button(canvas1, text = "choose file", command = selectUserVideoPath, bg='whitesmoke',width=10,relief=RAISED).grid(row = 3, column = 16)
# frm3.pack(side=LEFT,anchor=E,padx=4,fill=BOTH)

# frm4=Frame(frm_top)
btn_view1 = Button(canvas1, text='view',command=showVideo1, bg='whitesmoke',width=10,relief=RAISED).grid(row = 2, column = 17)
btn_view2 = Button(canvas1, text='view',command=showVideo2, bg='whitesmoke',width=10,relief=RAISED).grid(row = 3, column = 17)
# frm4.pack(side=LEFT,anchor=E,padx=4,fill=BOTH)

canvas1.pack() #放置canvas的位置

canvas4=Canvas(window,bg="whitesmoke",width=1024,height=20)
btn_inputVideo = Button(canvas4, text='inputVideo',command=lambda: inputCurrentVideo(),relief=RAISED).pack(anchor=CENTER,pady=4)
btn_sign_up = Button(canvas4, text='submit',command=getResult,relief=RAISED).pack(anchor=CENTER,pady=4)

canvas4.pack() #放置canvas的位置



canvas2=Canvas(window,width=1024,height=58) #创建canvas
frm_m=Frame(canvas2,bg='whitesmoke') #把frame放在canvas里
frm_m.place(x=3,y=3,width=1024, height=58) #frame的长宽，和canvas差不多的
canvas2.pack() #放置canvas的位置

def changePic(label_img, newPicAddress):
    new_img_open = Image.open(newPicAddress).resize((440, 260))
    new_img_png = ImageTk.PhotoImage(new_img_open)
    label_img.config(image=new_img_png)
    label_img.image = new_img_png


def print_selection():
    print("print_selection")
    value = lb.get(lb.curselection())
    picIndexArry = []
    print(picIndexArry)

    currentModelImgAddr = os.getcwd()+'/model/' + str(value) +'.jpg'
    print("aft")
    print(currentModelImgAddr)
    # GTV_PATH = 'D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\\right\'
    # USERV_PATH = 'D:\study\hand_gesture\-++n\openpose-1.4.0-win64-gpu-binaries\openpose-1.4.0-win64-gpu-binaries\compare\\wrong'
    currentUserImgAddr = os.getcwd()+'/user/' + str(value) + '.jpg'
    changePic(label_img1, currentModelImgAddr)
    changePic(label_img2, currentUserImgAddr)
canvas3=Canvas(window,width=1024,height=280)
frm_bu = Frame(canvas3,bg="whitesmoke")
imgPath= os.getcwd()
img1=imgPath+'/1.png'
img2=imgPath+'/2.png'



img_open1 = Image.open(img1).resize((440, 260))
img_png1 = ImageTk.PhotoImage(img_open1)
label_img1 = Label(frm_bu, image = img_png1)
label_img1.pack(side=LEFT)
#changePic(label_img1)
img_open2 = Image.open(img2).resize((440, 260))
img_png2 = ImageTk.PhotoImage(img_open2)
label_img2 = Label(frm_bu, image = img_png2)
label_img2.pack(side=LEFT)
frm_bu.pack()
frm_b = Frame(canvas3,bg="whitesmoke",width=1024)
# frm_b.pack(fill=X, side=TOP)
frm_b.pack(side=LEFT,fill=BOTH)
b1 = Button(frm_b, text='see images', command=print_selection)
b1.pack(anchor=CENTER)
lb = Listbox(frm_b,width=1000)
#scrollbar
sc = Scrollbar(frm_b)
sc.pack(side=RIGHT,fill=Y)
lb.pack(side=LEFT,fill=BOTH)
lb.config(yscrollcommand=sc.set)
sc['command']=lb.yview

canvas3.pack() #放置canvas的位置

window.mainloop()