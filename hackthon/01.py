# 影像修復互動式案例——通過水流填充演算法來修復被破壞的影像區域；
# 使用倆種方法進行修復
# cv2.INPAINT_TELEA （Fast Marching Method 快速行進演算法），對位于點附近、邊界法線附近和邊界輪廓上的像素賦予更多權重，一旦一個像素被修復，它將使用快速行進的方法移動到下一個最近的像素，
# cv2.INPAINT_NS 流體力學演算法，使用了流體力學的一些方法，基本原則是啟發式的，首先沿著邊從已知區域移動到未知區域（因為邊是連續的），它在匹配修復區域邊界處的漸變向量的同時，繼續等高線（連接具有相同強度的點的線，就像等高線連接具有相同高程的點一樣），

# USAGE 
# python inpaint.py D:/deepLearning/py-demo/20210808/images/ml.jpg

# 按下滑鼠左鍵,添加點、線，按下滑鼠右鍵，添加矩形框，以制作被污染的需要修復影像
# 按下空格鍵：執行修復功能
# 按下r鍵：重置待修復的mask
# 按下esc鍵，退出
from unittest import skip
import cv2
import numpy as np


class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None  # 線起始點
        self.drag_start = None  # 矩形起點
        self.drag_rect = None  # 矩形（左上角，右下角）坐標
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.drawing = False
        self.mode = False
        self.show()
        cv2.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname, self.dests[0])

    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
            self.drawing = True
        elif event == cv2.EVENT_RBUTTONDOWN:
            # 第一次初始化時設定pt，往后保留上一個點作為矩形起點
            if self.drag_start == None:
                self.drag_start = pt

        if self.prev_pt and flags & cv2.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv2.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()

        if self.drag_start and flags & cv2.EVENT_FLAG_RBUTTON:
            xo, yo = self.drag_start
            x0, y0 = np.minimum([xo, yo], [x, y])
            x1, y1 = np.maximum([xo, yo], [x, y])
            self.drag_rect = None
            if x1 - x0 > 0 and y1 - y0 > 0:
                self.drag_rect = (x0, y0, x1, y1)
                for dst, color in zip(self.dests, self.colors_func()):
                    cv2.rectangle(dst, (x0, y0), (x1, y1), color, -1)
                self.dirty = True
                self.drag_start = None
                self.drag_rect = None
                self.show()
            else:
                self.drag_start = pt
    def remove(fn):
        import sys
        # try:
        #     fn = sys.argv[1]
        # except:
        #     fn = "../hackthon/1.jpg"

        img = cv2.imread(fn)
        print(type(img))
        # img = cv2.resize(img, (1000, 1000*img.shape[0]/img.shape[1]))
        img = cv2.resize(img, (1000,int(img.shape[0]/img.shape[1]*1000)))
        
        if img is None:
            print('Failed to load image file:', fn)
            sys.exit(1)

        img_mark = img.copy()
        mark = np.zeros(img.shape[:2], np.uint8)
        sketch = Sketcher('原圖', [img_mark, mark], lambda: ((255, 255, 255), 255))

        while True:
            ch = cv2.waitKey()
            if ch == 27:
                break
            if ch == ord(' '):
                # cv2.imshow('mask', mark)
                fmmres = cv2.inpaint(img_mark, mark, 3, cv2.INPAINT_TELEA)
                # nsres = cv2.inpaint(img_mark, mark, 3, cv2.INPAINT_NS)
                cv2.imshow('inpaint fmm res', fmmres)
                cv2.imwrite("savedImage.jpg",fmmres)
                # cv2.imshow('inpaint ns res', nsres)
            if ch == ord('r'):
                img_mark[:] = img
                mark[:] = 0
                sketch.show()

        print('Done')

    @property
    def dragging(self):
        return self.drag_rect is not None


def main():
    Sketcher.remove("../hackthon/2.jpg")
    # import sys
    # try:
    #     fn = sys.argv[1]
    # except:
    #     fn = "../hackthon/1.jpg"

    # img = cv2.imread(fn)
    # print(type(img))
    # # img = cv2.resize(img, (1000, 1000*img.shape[0]/img.shape[1]))
    # img = cv2.resize(img, (1000,int(img.shape[0]/img.shape[1]*1000)))
    
    # if img is None:
    #     print('Failed to load image file:', fn)
    #     sys.exit(1)

    # img_mark = img.copy()
    # mark = np.zeros(img.shape[:2], np.uint8)
    # sketch = Sketcher('原圖', [img_mark, mark], lambda: ((255, 255, 255), 255))

    # while True:
    #     ch = cv2.waitKey()
    #     if ch == 27:
    #         break
    #     if ch == ord(' '):
    #         # cv2.imshow('mask', mark)
    #         fmmres = cv2.inpaint(img_mark, mark, 3, cv2.INPAINT_TELEA)
    #         # nsres = cv2.inpaint(img_mark, mark, 3, cv2.INPAINT_NS)
    #         cv2.imshow('inpaint fmm res', fmmres)
    #         # cv2.imshow('inpaint ns res', nsres)
    #     if ch == ord('r'):
    #         img_mark[:] = img
    #         mark[:] = 0
    #         sketch.show()

    # print('Done')


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
    

# def remove(fn):
#     import sys
#     # try:
#     #     fn = sys.argv[1]
#     # except:
#     #     fn = "../hackthon/1.jpg"

#     img = cv2.imread(fn)
#     print(type(img))
#     # img = cv2.resize(img, (1000, 1000*img.shape[0]/img.shape[1]))
#     img = cv2.resize(img, (1000,int(img.shape[0]/img.shape[1]*1000)))
    
#     if img is None:
#         print('Failed to load image file:', fn)
#         sys.exit(1)

#     img_mark = img.copy()
#     mark = np.zeros(img.shape[:2], np.uint8)
#     sketch = Sketcher('原圖', [img_mark, mark], lambda: ((255, 255, 255), 255))

#     while True:
#         ch = cv2.waitKey()
#         if ch == 27:
#             break
#         if ch == ord(' '):
#             # cv2.imshow('mask', mark)
#             fmmres = cv2.inpaint(img_mark, mark, 3, cv2.INPAINT_TELEA)
#             # nsres = cv2.inpaint(img_mark, mark, 3, cv2.INPAINT_NS)
#             cv2.imshow('inpaint fmm res', fmmres)
#             # cv2.imshow('inpaint ns res', nsres)
#         if ch == ord('r'):
#             img_mark[:] = img
#             mark[:] = 0
#             sketch.show()

#     print('Done')