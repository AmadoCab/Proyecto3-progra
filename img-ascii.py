from PIL import Image, ImageColor, ImageDraw, ImageOps, ImageFont
import os
import numpy as np
import datetime
from decouple import config
import tweepy
import webbrowser

chars = {
    '4ch' : list('@XF-'),
    '8ch' : list('@BX±F=-.'),
    '16ch' : list('@NB#XV±IF*=~-:.·'),
}

class ImgToAscii:
    # Properties
    def __init__(self, imgfile, scale=0.5, quality='16ch'):
        actual_dir = os.getcwd()
        self.quality = quality
        self.divide = 2**8//len(chars.get(quality))
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
        self.working_img = self.working_img.resize((int(self.width*17/10.9*self.scale), int(self.height*10.9/17*self.scale)))
        self.rewidth, self.reheight = self.working_img.size
        self.working_img.save('salida_resize.jpg')

    def imgmatrix(self):
        self.imgstr = ''
        self.matrix = np.asarray(self.working_img).transpose()
        for i in range(self.reheight):
            for j in range(self.rewidth):
                self.imgstr += chars.get(self.quality)\
                    [self.matrix[j, i]//self.divide]
            self.imgstr += '\n'

    def to_print(self):
        print(self.imgstr)

    def to_doc(self):
        with open(f'{datetime.datetime.now()}.txt', 'w') as f:
            f.write(self.imgstr)

    def to_pic(self):
        imgwidth, imgheight = self.matrix.shape
        txtimg = Image.new('L', (imgwidth*7,imgheight*17), color=2**8)
        draw = ImageDraw.Draw(txtimg)
        fnt = ImageFont.truetype('/Users/Macbook/Desktop/Python/PrograM/Proyecto 3/Font/IBMPlexMono-Medium.ttf',12)
        draw.multiline_text((0,0), self.imgstr, fill=0, font=fnt)
        txtimg.save('dibujoletras.jpg')

    def tweet(self):
        consumer_key = config('API_KEY')
        consumer_secret = config('API_SECRET_KEY')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        webbrowser.open(auth.get_authorization_url())
        pin = input('Verification pin number from twitter.com: ').strip()
        token = auth.get_access_token(verifier=pin)
        access_token = token[0]
        access_token_secret = token[1]
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        loqeusea = api.media_upload('dibujoletras.jpg')
        api.update_status('',media_ids=[loqeusea.media_id])

if __name__ == "__main__":
    imagen = ImgToAscii('Images/Kanis.jpeg',0.3,'16ch')
    imagen.to_blackwhite()
    imagen.rescale()
    imagen.imgmatrix()
    # imagen.to_print()
    imagen.to_pic()
    imagen.tweet()

#
