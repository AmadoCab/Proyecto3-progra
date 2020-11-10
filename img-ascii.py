from PIL import Image, ImageColor, ImageDraw, ImageOps
import os
import numpy as np

chars = list('@NB#XV±IF*=~-:.·')

class ImgToAscii:
    # Properties
    def __init__(self, imgfile, scale=0.5):
        actual_dir = os.getcwd()
        self.imgpath = os.path.join(actual_dir, imgfile)
        self.input_img = Image.open(self.imgpath)
        self.width, self.height = self.input_img.size
        self.scale = scale
        print(self.width, self.height)

    # Methods
    def to_blackwhite(self):
        self.working_img = ImageOps.grayscale(self.input_img)
        self.working_img.save('salida_colores.jpg')
        print(type(self.working_img))

    def rescale(self):
        self.working_img = self.working_img.resize((int(self.width*17/11*self.scale), int(self.height*11/17*self.scale)))
        self.rewidth, self.reheight = self.working_img.size
        self.working_img.save('salida_resize.jpg')

    def imgmatrix(self):
        self.imgstr = ''
        self.matrix = np.asarray(self.working_img).transpose()
        for i in range(self.reheight):
            for j in range(self.rewidth):
                self.imgstr += chars[self.matrix[j, i]//16]
            self.imgstr += '\n'

    def to_print(self):
        print(self.imgstr)

    def to_doc(self):
        with open('salida.txt', 'w') as f:
            f.write(self.imgstr)

if __name__ == "__main__":
    imagen = ImgToAscii('Amadito.jpeg',0.3)
    imagen.to_blackwhite()
    imagen.rescale()
    imagen.imgmatrix()
    imagen.to_print()

#
