import cv2 as cv
import numpy as np
import urllib.request

def read_img_url(url):
    req = urllib.request.urlopen(url)
    img_rw = np.asarray( bytearray(req.read()), dtype=np.uint8)
    img = cv.imdecode(img_rw, cv.IMREAD_COLOR)
    return img 

def add_noise(img):
    mean = 0
    sigma = 50
    noisy = np.random.normal(mean, sigma, img.shape)
    new_img = np.clip( img + noisy, 0, 255 ).astype(np.uint8)
    return new_img

def add_muoi_tieu(img, ratio=0.02):
    nosy = img.copy()
    soluong = int(ratio*img.size)

    #thêm muối
    toado = [np.random.randint(0, i-1 ,soluong) for i in img.shape]
    nosy[ toado[0], toado[1] ] = 255
    # thêm tiêu
    toado = [np.random.randint(0, i-1 ,soluong) for i in img.shape]
    nosy[ toado[0], toado[1] ] = 0

    return nosy

if __name__=="__main__":

    url = "https://raw.githubusercontent.com/udacity/CarND-LaneLines-P1/master/test_images/solidWhiteCurve.jpg"
    img = read_img_url(url)
    img2 = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # cv.line(img2, (0,500), (200,500),2)
    cv.imshow("img", img2)
    cv.waitKey(0)
    cv.destroyAllWindows()


    edge = cv.Canny(img2, 50, 150)
    cv.imshow("edge", edge)
    cv.waitKey(0)
    cv.destroyAllWindows()
    h,w = edge.shape
    mask = np.zeros_like(edge)
    polygon = np.array([[ (0,h), (w,h), (w//2 - 50, h//2), (w//2 + 50, h//2) ]], 
                       dtype=np.int32)
    cv.fillPoly(mask, polygon, 255)
    roi = cv.bitwise_and(edge, mask)
    cv.imshow("ROI",roi)
    cv.waitKey(0)
    cv.destroyAllWindows()
    lines = cv.HoughLinesP(
        roi,
        rho=1.0,
        theta=np.pi/180,
        threshold=50,
        minLineLength=50,
        maxLineGap=100
    )
    img_line = img.copy()
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv.line(img_line, (x1,y1), (x2,y2), (0,0,255),1)
    cv.imshow("detected_lane", img_line)
    cv.waitKey()
    cv.destroyAllWindows()