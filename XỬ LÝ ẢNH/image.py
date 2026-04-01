import matplotlib.pyplot as plt
import numpy as np  
import cv2 as cv
from datetime import datetime
import math    

# # M=1024
# # N=768

# # # img =np.zeros((M,N), dtype=np.uint8) 
# # # plt.imshow(img, cmap='gray')
# # # plt.show()
# # img = np.zeros((M, N), dtype=np.uint8)

# # #vẽ đường chéo
# # cv.line(img, (0, 0), (N-1, M-1), 255)

# # # vẽ đường tròn
# # cv.circle(img, (N//2, M//2), 400, 255, 15)

# # cv.imshow('image', img)
# # if cv.waitKey(0) == 27:
# #     cv.destroyAllWindows()
# ---------------------------------------------------------------------------------------------------------------
# #vẽ chồng line màu
# # m = 1000
# # n = 1000
# # c = 3
# # cl_img = np.zeros((m, n, c), dtype=np.uint8)
# # cl_img[10:300,:, 0] = 255 
# # cl_img[255:500, :, 1] = 255    
# # cl_img[450:700, :, 2] = 255   
# # cv.imshow('color image', cl_img)
# # cv.waitKey(0)
# # cv.destroyAllWindows()
# ------------------------------------------------------------------------------------------------------------
# # vẽ bàn cờ vua đen trắng 8x8, mỗi ô 100x100px
# chessboard = np.zeros((800, 800, 3), dtype=np.uint8)

# # chessboard[0:99, 0:99] = [128,0,128]
# # chessboard[100:199, 100:199] = [255,255,0]

# # cv.rectangle(chessboard, (200,0), (299,99), (128,0,128), -1)
# # cv.rectangle(chessboard, (0,200), (99,299), (255,255,0), -1)

# for i in range(8):
#     for j in range(8):
#         if (i + j) % 2 == 0:
#             cv.rectangle(chessboard, (j*100, i*100), (j*100+99, i*100+99), (255, 255, 255), -1)
#         else:
#             cv.rectangle(chessboard, (j*100, i*100), (j*100+99, i*100+99), (0, 0, 0), -1)

# cv.imshow('chessboard', chessboard)
# cv.waitKey(0)
# cv.destroyAllWindows()
# -------------------------------------------------------------------------------------------------------------
#Vẽ mặt đồng hồ hình tròn, nền màu tím, có các số dạng la mã màu sắc khác nhau. 
#Có 3 kim đồng hồ: Giờ, phút, giây.
#Kim giờ màu xanh dương, kim phút màu xanh lá cây, kim giây màu đỏ.
#level 2: Vẽ kim giây chuyển động.
#level 3: Vẽ kim phút chuyển động.
#level 4: Vẽ kim giờ chuyển động.   
#level 5: Vẽ thêm các vạch chỉ phút trên mặt đồng hồ. Và kim giây, kim giờ, kim phút, hoạt động theo logic

# Chuyển đổi số từ 1-12 sang chữ số La Mã
def to_roman(num):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num

def draw_clock(show_animation=True):
    """Vẽ đồng hồ với các kim chuyển động"""
    
    # Tạo ảnh 600x600 pixels
    img_size = 600
    center = (img_size // 2, img_size // 2)
    radius = 250
    
    # Màu sắc
    purple_bg = (128, 0, 128)  # Tím (BGR)
    white = (255, 255, 255)
    blue_hand = (255, 0, 0)      # Xanh dương (BGR)
    green_hand = (0, 255, 0)     # Xanh lá cây
    red_hand = (0, 0, 255)       # Đỏ
    
    # Danh sách màu cho số La Mã
    colors = [
        (255, 0, 0),      # Đỏ
        (0, 255, 0),      # Xanh lá
        (0, 0, 255),      # Xanh dương
        (255, 255, 0),    # Cyan
        (255, 0, 255),    # Magenta
        (0, 255, 255),    # Yellow
        (255, 128, 0),    # Orange
        (0, 255, 128),    # Spring Green
        (128, 0, 255),    # Violet
        (255, 0, 128),    # Rose
        (128, 255, 0),    # Chartreuse
        (0, 128, 255),    # Sky Blue
    ]
    
    while True:
        # Tạo ảnh nền tím
        img = np.full((img_size, img_size, 3), purple_bg, dtype=np.uint8)
        
        # Vẽ vòng tròn mặt đồng hồ
        cv.circle(img, center, radius, white, 3)
        cv.circle(img, center, radius - 10, white, 2)
        
        # Vẽ các vạch chỉ phút (Level 5)
        for i in range(60):
            angle = i * 6  # 360 / 60 = 6 độ
            rad = math.radians(angle)
            x1 = int(center[0] + (radius - 25) * math.sin(rad))
            y1 = int(center[1] - (radius - 25) * math.cos(rad))
            x2 = int(center[0] + (radius - 10) * math.sin(rad))
            y2 = int(center[1] - (radius - 10) * math.cos(rad))
            
            if i % 5 == 0:  # Vạch dài cho giờ
                cv.line(img, (int(center[0] + (radius - 30) * math.sin(rad)), 
                             int(center[1] - (radius - 30) * math.cos(rad))), (x2, y2), white, 3)
            else:  # Vạch ngắn cho phút
                cv.line(img, (x1, y1), (x2, y2), white, 1)
        
        # Vẽ các số La Mã
        for i in range(1, 13):
            angle = (i - 3) * 30  # Bắt đầu từ 3 (0 độ ở bên phải)
            rad = math.radians(angle)
            x = int(center[0] + (radius - 50) * math.cos(rad))
            y = int(center[1] + (radius - 50) * math.sin(rad))
            
            roman = to_roman(i)
            color = colors[i - 1]
            cv.putText(img, roman, (x - 15, y + 10), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Lấy thời gian hiện tại
        now = datetime.now()
        hours = now.hour % 12
        minutes = now.minute
        seconds = now.second
        
        # Tính góc cho từng kim (Level 5: hoạt động theo logic)
        second_angle = seconds * 6  # 360 / 60 = 6 độ/giây
        minute_angle = (minutes + seconds / 60) * 6  # 360 / 60 = 6 độ/phút
        hour_angle = (hours + minutes / 60) * 30  # 360 / 12 = 30 độ/giờ
        
        # Kim giây (đỏ) - Level 2
        second_end_x = int(center[0] + (radius - 80) * math.sin(math.radians(second_angle)))
        second_end_y = int(center[1] - (radius - 80) * math.cos(math.radians(second_angle)))
        cv.line(img, center, (second_end_x, second_end_y), red_hand, 2)
        
        # Kim phút (xanh lá cây) - Level 3
        minute_end_x = int(center[0] + (radius - 100) * math.sin(math.radians(minute_angle)))
        minute_end_y = int(center[1] - (radius - 100) * math.cos(math.radians(minute_angle)))
        cv.line(img, center, (minute_end_x, minute_end_y), green_hand, 4)
        
        # Kim giờ (xanh dương) - Level 4
        hour_end_x = int(center[0] + (radius - 140) * math.sin(math.radians(hour_angle)))
        hour_end_y = int(center[1] - (radius - 140) * math.cos(math.radians(hour_angle)))
        cv.line(img, center, (hour_end_x, hour_end_y), blue_hand, 5)
        
        # Vẽ tâm đồng hồ
        cv.circle(img, center, 8, white, -1)
        
        # Hiển thị giờ dưới đồng hồ
        time_str = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        cv.putText(img, time_str, (center[0] - 60, center[1] + radius + 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 1, white, 2)
        
        # Hiển thị ảnh
        cv.imshow('Analog Clock', img)
        
        # Nhấn ESC để thoát
        if cv.waitKey(1000) == 27:  # Cập nhật mỗi 1 giây
            cv.destroyAllWindows()
            break

# Chạy đồng hồ
draw_clock()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------