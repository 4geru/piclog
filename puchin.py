import lib.image_analizer
import lib.translate
import lib.make_sentence
import lib.make_pdf
from lib.env import ENV
import sys,re

def run():
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数
    if argc != 2:
        print('ERROR : PLEASE INPUT URL')
        return False
    if not re.match(r"http", argvs[1]):
        print('ERROR : INPUT IS NOT URL')
        
    img = argvs[1]
    # analyze 単語(DescriptionのTags) -> words
    print('analyze image\t>> doing', end="")
    english_words = lib.image_analizer.analyze(img)
    # print(english_words)
    print(' >> finished')
    
    # translate 英単語 -> 日本語単語
    print('translate words\t>> doing', end="")
    japanese_words = lib.translate.translate_array(english_words)
    #print(japanese_words)
    print(' >> finished')
    
    # make_sentence00 日本語単語 -> 文
    print('make sentence\t>> doing', end="")
    sentence = lib.make_sentence.main(japanese_words)
    # print(sentence)
    print(' >> finished')
    
    # make_pdf 文 -> pdf
    print('make pdf\t>> doing', end="")
    lib.make_pdf.make(sentence,img)
    print(' >> finished')
run()
