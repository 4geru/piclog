import lib.image_analizer
import lib.translate
import lib.make_sentence
import lib.make_pdf
from lib.env import ENV

def run():
    img = 'http://farm1.staticflickr.com/91/215530530_df14c4fa87_z.jpg'
    # analyze 単語(DescriptionのTags) -> words
    english_words = lib.image_analizer.analyze(img)
    print(english_words)
    
    # translate 英単語 -> 日本語単語
    japanese_words = lib.translate.translate_array(english_words)
    #print(japanese_words)
    # make_sentence00 日本語単語 -> 文
    sentence = lib.make_sentence.main(japanese_words)
    print(sentence)
    
    # make_pdf 文 -> pdf
    lib.make_pdf.make(sentence,img)
# run()
