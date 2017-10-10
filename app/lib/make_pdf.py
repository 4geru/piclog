# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import letter, landscape
from datetime import datetime
from urllib.request import urlopen
from PIL import Image
import reportlab.lib.colors as color
import io
class make_pdf:
    def __init__(self, sentence, img_url):
        """ pdfを自動生成 
         >> sentence -> 文章
         >> image_url -> 画像のURL
         << /piclog.pdf が生成されます
        """
        self.pdf_canvas = self.set_info('piclog')
        self.print_title('piclog')
        self.print_image(img_url)
        self.print_box()
        self.print_word(sentence)
        self.pdf_canvas.save()
    
    # 初期設定
    def set_info(self, filename):
        """ 初期設定 """
        pdf_canvas = canvas.Canvas("./{0}.pdf".format(filename), bottomup=False, pagesize=letter)  # 原点は左上
        # [TODO] 考える
        pdf_canvas.setAuthor("しげる")
        pdf_canvas.setTitle("PicLog")
        pdf_canvas.setSubject("PicLog")
        
        return pdf_canvas
    
    def print_title(self,word):
        """ 見出しを描画 """
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
        self.pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
        
        weekdays = ["月","火","水","木","金","土","日"]
        now = datetime.now()
        date = now.strftime("%Y/%m/%d")
        self.pdf_canvas.drawString(30, 45, "{0}({1}) 名前 : さきさか しげる".format(date, weekdays[now.weekday()]))
    
    def print_word(self, sentence):
        """ 文字を描画 """
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
        self.pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
        step = 40
        idx = 0
        for i in range(586-step,26-step,-step):
          for j in range(360,760,step):
            if len(sentence) > idx:
                self.pdf_canvas.drawString(i+10, j+10+19, sentence[idx])
            else:
                break
            idx += 1
        return idx
    
    def print_box(self):
      """ 罫線を描画 """
      step = 40
      self.pdf_canvas.setStrokeColor(color.black)
      for i in range(26,586+step,step):
        self.pdf_canvas.line(i, 360, i, 760)
      for i in range(360,760+step,step):
        self.pdf_canvas.line(26, i, 586, i)
    
    # 画像
    def print_image(self, img_url):
        """ 画像を描画 """
        f = io.BytesIO(urlopen(img_url).read())
        image = Image.open(f).transpose(Image.FLIP_TOP_BOTTOM)
        
        width = 552
        height = 276
        title_space = 40
        
        self.pdf_canvas.drawInlineImage(image,letter[0]/2-width/2,62-height, width, height)

if __name__ == "__main__":
    """ ファイルを実行に動作 """
    sentence = 'a'*140
    make_pdf(sentence, 'http://img.mcdonalds.co.jp/index/graphic/main_170920a.jpg')