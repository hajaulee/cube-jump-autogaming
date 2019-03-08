import numpy as np
import cv2
from PIL import ImageGrab as ig
import time
import pyautogui
import skvideo.io
import ffmpeg
last_time = time.time()
kernelOpen=np.ones((5,5))
kernelClose=np.ones((200,200))

deltaX = 60
deltaY = 5
size = 10
start = False
step = 0
gameDelay = 0.2
wait = False
oldX = 0
des_pixel = np.array([119, 152, 209])
thresold = np.array([10, 10, 10])
# lower_red = np.array([95, 40, 140])
# upper_red = np.array([180, 255, 255])

lower = des_pixel - thresold
upper = des_pixel + (thresold / 2)
# print(skvideo._FFMPEG_SUPPORTED_ENCODERS)
# writer = skvideo.io.FFmpegWriter("outputvideo.mp4")

while(True):
    screen = ig.grab(bbox=(0,30,390,730))
    # screen = ig.grab(bbox=(40, 300, 400, 330))
    img_np = np.array(screen)


    screen = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    mask = cv2.inRange(screen, lower.astype(int), upper.astype(int))

    # print(mask.shape)
    light = np.nonzero(mask)
    # print(light)
    if len(light[0]) > 0:
        x_array = light[1]
        x_array_less, x_array_great = x_array[x_array < np.mean(x_array)], x_array[x_array >= np.mean(x_array)]
        print("Array split", len(x_array_less), ":", len(x_array_great))
        x_r = np.mean(x_array_less) if len(x_array_less) > len(x_array_great) else np.mean(x_array_great)
        # Test find x by std and mean
        # ltf =  x_array[(x_array > np.mean(x_array) - np.std(x_array)/2) & (x_array < np.mean(x_array) + np.std(x_array)/2)]
        # x_r = np.mean(ltf)

        y_array = light[0]
        y_array_less, y_array_great = y_array[y_array < np.mean(y_array)], y_array[y_array >= np.mean(y_array)]
        y_r = np.mean(y_array_less) if len(y_array_less) > len(y_array_great) else np.mean(y_array_great)

        x_r, y_r = int(x_r), int(y_r)
        # cv2.rectangle(screen, (x_r - 10, y_r - 10), (x_r + 10, y_r + 10), (0, 0, 255), 2)
        x, y, w, h = x_r - 30, y_r - 20, 50, 30


        # Drawing a arrow
        # if h > w:
        #     h = w//2 # Replace h by w//2 for beautiful
        #     # Arrow to right
        #     cv2.arrowedLine(screen, (x + w//2, y + h//2), (x + w*2, y - h*2), (0, 255, 0), 2)
        # else:
        #     # Arrow to left
        #     cv2.arrowedLine(screen, (x + w // 2, y + h // 2), (x - w * 2, y - h * 2), (0, 255, 0), 2)


        # Draw box
        cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), 2)
        rightBox = (x + deltaX, y - deltaY)
        leftBox = (x - deltaX + size, y - deltaY)
        cv2.rectangle(screen, rightBox, (rightBox[0] + size, rightBox[1] + size), (255, 0, 0), 1)
        cv2.rectangle(screen, leftBox, (leftBox[0] + size, leftBox[1] + size), (255, 0, 0), 1)

        try:

            if x < 70 or y < 40 or x > 260:
                wait = True
                cv2.putText(screen, 'Wait', (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 3, cv2.LINE_AA)
            else:
                wait = False
            # if (oldX != 0) and np.abs(oldX - x) > 40:
            #     wait = True

            print(oldX, "---", x)
            oldX = x
            colorRight = np.sum(screen[rightBox[1]:rightBox[1] + size, rightBox[0]:rightBox[0] + size])
            colorLeft = np.sum(screen[leftBox[1]:leftBox[1] + size, leftBox[0]:leftBox[0] + size])
            print("Left color", colorLeft)
            print("Right color", colorRight)
            if colorLeft > colorRight:
                # Arrow to right
                cv2.arrowedLine(screen, (x + w // 2, y + h // 2), (x + w * 2, y - h * 2), (255, 0, 0), 2)
                if start and not wait:
                    pyautogui.click(300, 400)
                    print("Jump --------------    to    -----------------    RIGHT")
            else:
                # Arrow to left
                cv2.arrowedLine(screen, (x + w // 2, y + h // 2), (x - w * 2, y - h * 2), (255, 0, 0), 2)
                if start and not wait:
                    pyautogui.click(100, 400)
                    print("Jump ---------------   to   -----------------     LEFT")
            # Increase Game step
            step += 1
            # Update game speed for new step
            if step % 30 == 0:
                gameDelay = gameDelay / 1.122
            time.sleep(gameDelay)
        except IndexError:
            wait = True
            cv2.putText(screen, 'Wait', (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 3, cv2.LINE_AA)

        try:
            if cv2.waitKey(25) & 0xFF == ord('s'):  # if key 's' is pressed
                start = True
            elif  cv2.waitKey(25) & 0xFF == ord('e'):
                start = False

            if not start and not wait:
                cv2.putText(screen, 'End', (40, 300), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 3,
                                      cv2.LINE_AA)
        except:
            pass
        print(x, y, w, h)
    else:
       pass

    # print('Loop took {} seconds'.format(time.time()-last_time))

    cv2.imshow("ori", np.array(screen))
    # writer.writeFrame(screen)
    cv2.imshow('mask', mask)
    cv2.moveWindow("ori", 900, 0);
    cv2.moveWindow('mask', 500, 0)
    last_time = time.time()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
# writer.close()