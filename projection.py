import cv2


class Projection():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.Tx =  x + w/2
        self.Ty = y + h/2

    # Take coordinates of collision location compare to Projection area's location.
    def collision(self, x, y):
        wBound = self.w/2
        hBound = self.h/2
        print(wBound)
        print(hBound)
        if(x < (self.x + wBound) and x > (self.x - wBound) and y < (self.y + hBound) and y > (self.y - hBound)):
            print("Projection hit!")
            return True
        else:
            print("Miss!")
            return False
