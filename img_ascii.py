from PIL import Image, ImageColor, ImageDraw, ImageOps, ImageFont
from decouple import config
import numpy as np
import webbrowser
import datetime
import tweepy
import os

### Global variables ###
consumer_key = config('API_KEY')
consumer_secret = config('API_SECRET_KEY')

### List of characters to generate an image ###
chars = {
    '4ch' : list('@XF-'),
    '8ch' : list('@BX±F=-.'),
    '16ch' : list('@NB#XV±IF*=~-:.·'),
}

### Class to generate the images and text ###
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
        self.name = datetime.datetime.now()
        print(self.width, self.height)

    # Methods
    def to_blackwhite(self):
        """
        Converts the image to black and white
        """
        self.working_img = ImageOps.grayscale(self.input_img)
        self.working_img.save('salida_colores.jpg')
        print(type(self.working_img))

    def rescale(self):
        """
        Rescales the image to a size that when the pixels get changed by characters it conserves its original appearence
        """
        self.working_img = self.working_img.resize((int(self.width*17/10.9*self.scale), int(self.height*10.9/17*self.scale)))
        self.rewidth, self.reheight = self.working_img.size
        self.working_img.save('salida_resize.jpg')

    def imgmatrix(self):
        """
        Transfor the image to a matrix and replace the pixels to characters
        """
        self.imgstr = ''
        self.matrix = np.asarray(self.working_img).transpose()
        for i in range(self.reheight):
            for j in range(self.rewidth):
                self.imgstr += chars.get(self.quality)\
                    [self.matrix[j, i]//self.divide]
            self.imgstr += '\n'

    def to_print(self):
        """
        Print in terminal the image
        """
        print(self.imgstr)

    def to_doc(self):
        """
        Write in a document the image
        """
        with open(f'{self.name}.txt', 'w') as f:
            f.write(self.imgstr)

    def to_pic(self):
        """
        Transfor the text on an image
        """
        imgwidth, imgheight = self.matrix.shape
        txtimg = Image.new('L', (imgwidth*7,imgheight*17), color=2**8)
        draw = ImageDraw.Draw(txtimg)
        fnt = ImageFont.truetype('/Users/Macbook/Desktop/Python/PrograM/Proyecto 3/Font/IBMPlexMono-Medium.ttf',12)
        draw.multiline_text((0,0), self.imgstr, fill=0, font=fnt)
        txtimg.save(f'{self.name}.jpg')

    def tweet(self):
        """
        This method has to be preced by "to_pic" method to tweet the image produced by that method
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        if not is_logged():
            webbrowser.open(auth.get_authorization_url())
            pin = input('Verification pin number from twitter.com: ').strip()
            token = auth.get_access_token(verifier=pin)
            access_token = token[0]
            access_token_secret = token[1]
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            login(api.me()._json.get('name'), token[0], token[1])
        else:
            access_token, access_token_secret = get_credentials()
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
        loqeusea = api.media_upload(f'{self.name}.jpg')
        api.update_status(f'#ASCIIArtPM1',media_ids=[loqeusea.media_id])

def is_logged():
    """
    The method returns True or False if the program has the credentials of a user or not respectively
    """
    with open('credentials.txt', 'r') as f:
        if f.readline() == 'NOCREDENTIALS':
            return False
        else:
            return True

def get_credentials():
    """
    Takes the credentials of the user and returns it on a tuple
    """
    with open('credentials.txt', 'r') as f:
        linea = f.readline().strip().split(',')
    return linea[1], linea[2]

def get_logged():
    if not is_logged():
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        webbrowser.open(auth.get_authorization_url())
        pin = input('Verification pin number from twitter.com: ').strip()
        token = auth.get_access_token(verifier=pin)
        access_token = token[0]
        access_token_secret = token[1]
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        login(api.me()._json.get('name'), token[0], token[1])
    else:
        print("You are already logged")

def login(nombre, key, skey):
    """
    Save the credentials
    """
    cadena = f'{nombre},{key},{skey}'
    with open('credentials.txt', 'w') as f:
        f.write(cadena)

def logout():
    """
    Erase the credentials
    """
    with open('credentials.txt', 'w') as f:
        f.write('NOCREDENTIALS')

if __name__ == "__main__":
    imagen = ImgToAscii('Images/Marianita.jpeg',0.3,'16ch')
    imagen.to_blackwhite()
    imagen.rescale()
    imagen.imgmatrix()
    # imagen.to_print()
    imagen.to_pic()
    # imagen.tweet()

#