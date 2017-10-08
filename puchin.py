import analyze
import translate
import make_sentence00
import make_pdf

img = 'http://farm1.staticflickr.com/91/215530530_df14c4fa87_z.jpg'
# analyze 単語(DescriptionのTags) -> words
english_words = analyze.analyze(img)
print(english_words)

# translate 英単語 -> 日本語単語
japanese_words = translate.translate_array(english_words)
#print(japanese_words)
# make_sentence00 日本語単語 -> 文
sentence = make_sentence00.make_sentence(japanese_words)
print(sentence)

# make_pdf 文 -> pdf
make_pdf.make(sentence,img)