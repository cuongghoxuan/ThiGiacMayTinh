import cv2 as cv       
import numpy as np
import urllib.request
# _________________________________________________________________________________________________________________________________
# def read_img_url(url):
#     req = urllib.request.urlopen(url)
#     img =np.array(bytearray(req.read()), dtype=np.uint8)
#     return img

# if "__main__" == __name__:
#     url = "https://raw.githubusercontent.com/opencv/opencv/refs/heads/4.x/samples/data/lena.jpg"
#     print(read_img_url(url))

# _______________________________________________________________________________________________________________________________________
# hiển thị ảnh từ URL
# def read_img_url(url):
#     req = urllib.request.urlopen(url)
#     img_rw=np.array(bytearray(req.read()), dtype=np.uint8)
#     img = cv.imdecode(img_rw, 3)
#     return img

# if "__main__" == __name__:
#     url = "https://raw.githubusercontent.com/opencv/opencv/refs/heads/4.x/samples/data/lena.jpg"
#     img = read_img_url(url)
#     cv.imshow("img", img)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
# _______________________________________________________________________________________________________________________________
# def read_img_url(url):
#     req = urllib.request.urlopen(url)
#     img_rw=np.array(bytearray(req.read()), dtype=np.uint8)
#     img = cv.imdecode(img_rw, 3)
#     return img

# def add_noise(img):
#     mean = 0
#     sigma = 50 
#     noisy = np.random.normal(mean, sigma, img.shape)
#     new_img = np.clip(noisy, 0, 255).astype(np.uint8)
#     return new_img

# def add_muoi_tieu(img, ratio=0.02):
#     nosy = img.copy()
#     soluong = int(ratio * img.size)
#     #cho muoi
#     toado = [np.random.randint(0, i - 1, soluong) for i in img.shape]
#     nosy[toado[0], toado[1], :] = 255
#     # cho tieu
#     toado = [np.random.randint(0, i - 1, soluong) for i in img.shape]
#     nosy[toado[0], toado[1], :] = 0

#     return nosy



# if "__main__" == __name__:
#     url = "https://raw.githubusercontent.com/opencv/opencv/refs/heads/4.x/samples/data/lena.jpg"
#     img = read_img_url(url)
#     cv.imshow("img", img)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     n_ = add_noise(img)
#     cv.imshow("noisy img", n_)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     imt = img.copy()

#     img2 =np.clip(imt + n_, 0, 255)
#     cv.imshow("img + noisy img", img2.astype(np.uint8))
#     cv.waitKey(0)
#     cv.destroyAllWindows()

#     img3 = np.concatenate((img, img2.astype(np.uint8)), axis=1)
#     cv.imshow("img3", img3)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
    
#     anh_muoi_tieu = add_muoi_tieu(img, 0.01)
#     cv.imshow("img4", anh_muoi_tieu)
#     cv.waitKey(0)  
#     cv.destroyAllWindows()

#     img5 =np.concatenate((img, anh_muoi_tieu), axis=1)
#     cv.imshow("img5", img5)
#     cv.waitKey()
#     cv.destroyAllWindows()
#______________________________________________________________________________________________________________________________
