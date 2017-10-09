# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import letter, landscape
import reportlab.lib.colors as color
from PIL import Image
import io
import urllib.request
def make(sentence, img_url):
    pdf_canvas = set_info('絵日記')
    print_title(pdf_canvas,'title')
    print_image(pdf_canvas, img_url)
    print_box(pdf_canvas)
    print_word(pdf_canvas, sentence)
    pdf_canvas.save()

# 初期設定
def set_info(filename):
    # print(letter) # height, width
    pdf_canvas = canvas.Canvas("./{0}.pdf".format(filename), bottomup=False, pagesize=letter)  # 原点は左上
        
    pdf_canvas.setAuthor("しげる")
    pdf_canvas.setTitle("絵日記")
    pdf_canvas.setSubject("reportlab")
    
    return pdf_canvas

def print_title(pdf_canvas,word):
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
    pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
    pdf_canvas.drawString(30, 45, "絵日記 2017/10/06(金) 名前 : さきさか しげる")

# 文字
def print_string(pdf_canvas):
    # フォントを登録する
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

    # ゴシック体をサイズ15で
    pdf_canvas.setFont("HeiseiKakuGo-W5", 15)
    pdf_canvas.drawString(50, 50, "ゴシック体をサイズ15で")

    # 明朝体をサイズ30で
    pdf_canvas.setFont("HeiseiMin-W3", 30)
    pdf_canvas.drawString(300, 100, "明朝体をサイズ30で")

def print_word(pdf_canvas, sentence):
    # フォントを登録する
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

    # ゴシック体をサイズ15で
    pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
    step = 40
    idx = 0
    arr = sentence
    for i in range(586-step,26-step,-step):
      for j in range(360,760,step):
        if len(arr) > idx:
            pdf_canvas.drawString(i+10, j+10+19, str(arr[idx]))
        else:
            break
        idx += 1

def print_box(pdf_canvas):
  # 普通の線
  step = 40
  pdf_canvas.setStrokeColor(color.blue)
  for i in range(26,586+step,step):
  # for i in range(6,606+step,step):
    pdf_canvas.line(i, 360, i, 760)
  for i in range(360,760+step,step):
    # pdf_canvas.line(6, i, 606, i)
    pdf_canvas.line(26, i, 586, i)

# 画像
def print_image(pdf_canvas, img_url):
    f = io.BytesIO(urllib.request.urlopen(img_url).read())
    image = Image.open(f)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    print(letter)
    # x,y,width,height
    width = 552
    height = 276
    title_space = 40
    height_margin = title_space+(360-title_space)/2 - height/2

    print(image.size)
    pdf_canvas.drawInlineImage(image,letter[0]/2-width/2,height_margin-height, width, height)
