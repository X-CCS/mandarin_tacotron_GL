# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals
import sys
import re
from pypinyin import pinyin, Style, load_phrases_dict
import jieba

consonant_list = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k',
                  'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z',
                  'c', 's', 'y', 'w']

TRANSFORM_DICT = {'ju':'jv', 'qu':'qv', 'xu':'xv', 'zi':'zic',
                  'ci':'cic', 'si':'sic', 'zhi':'zhih', 
                  'chi':'chih', 'shi':'shih', 'ri':'rih',
                  'yuan':'yvan', 'yue':'yve', 'yun':'yvn',
                  'quan':'qvan','xuan':'xvan','juan':'jvan',
                  'qun':'qvn','xun':'xvn', 'jun':'jvn',
                  'iu':'iou', 'ui':'uei', 'un':'uen',
                  'ya':'yia', 'ye':'yie', 'yao':'yiao',
                  'you':'yiou', 'yan':'yian', 'yin':'yin',
                  'yang':'yiang', 'ying':'ying', 'yong':'yiong',
                  'wa':'wua', 'wo':'wuo', 'wai':'wuai',
                  'wei':'wuei', 'wan':'wuan', 'wen':'wuen',
                  'weng':'wueng', 'wang':'wuang'}

translate_dict = {'ju':'jv', 'qu':'qv', 'xu':'xv', 'zi':'zic',
                  'ci':'cic', 'si':'sic', 'zhi':'zhih', 
                  'chi':'chih', 'shi':'shih', 'ri':'rih',
                  'yuan':'yvan', 'yue':'yve', 'yun':'yvn',
                  'quan':'qvan','xuan':'xvan','juan':'jvan',
                  'qun':'qvn','xun':'xvn', 'jun':'jvn',
                  'iu':'iou', 'ui':'uei', 'un':'uen'}
# phone-set with y w, this is the default phone set
translate_dict_more = {'ya':'yia', 'ye':'yie', 'yao':'yiao',
                       'you':'yiou', 'yan':'yian', 'yin':'yin',
                       'yang':'yiang', 'ying':'ying', 'yong':'yiong',
                       'wa':'wua', 'wo':'wuo', 'wai':'wuai',
                       'wei':'wuei', 'wan':'wuan', 'wen':'wuen',
                       'weng':'wueng', 'wang':'wuang'}
# phone-set without y w 
translate_dict_less = {'ya':'ia', 'ye':'ie', 'yao':'iao',
                       'you':'iou', 'yan':'ian', 'yin':'in',
                       'yang':'iang', 'ying':'ing', 'yong':'iong',
                       'yvan':'van', 'yve':'ve', 'yvn':'vn',
                       'wa':'ua', 'wo':'uo', 'wai':'uai',
                       'wei':'uei', 'wan':'uan', 'wen':'uen',
                       'weng':'ueng', 'wang':'uang'}

def _pre_pinyin_setting():
    ''' fix pinyin error'''
    load_phrases_dict({'嗯':[['ēn']]})

_pre_pinyin_setting()

def pinyinformat(syllable):
    '''format pinyin to mtts's format''' 
    if not syllable[-1].isdigit():
        syllable = syllable + '5'
    assert syllable[-1].isdigit()
    syl_no_tone = syllable[:-1]
    if syl_no_tone in TRANSFORM_DICT:
        syllable = syllable.replace(syl_no_tone, TRANSFORM_DICT[syl_no_tone])
    return syllable
 
    """
    for key, value in translate_dict.items():
        syllable = syllable.replace(key, value)
    for key, value in translate_dict_more.items():
        syllable = syllable.replace(key, value)
    if not syllable[-1].isdigit():
        syllable = syllable + '5'
    return syllable
    """
def seprate_syllable(syllable):
    '''seprate syllable to consonant + ' ' + vowel '''
    assert syllable[-1].isdigit()
    if syllable[0:2] in consonant_list:
        #return syllable[0:2].encode('utf-8'),syllable[2:].encode('utf-8')
        return syllable[0:2], syllable[2:]
    elif syllable[0] in consonant_list:
        #return syllable[0].encode('utf-8'),syllable[1:].encode('utf-8')
        return syllable[0], syllable[1:]
    else:
        #return (syllable.encode('utf-8'),)
        return (syllable,)


def txt2pinyin(txt):
    phone_list = []
    '''
    if isinstance(txt, str):
        pinyin_list = pinyin(unicode(txt,'utf-8'), style = Style.TONE3)
    elif isinstance(txt, unicode):
        pinyin_list = pinyin(txt, style = Style.TONE3)
    else:
        print('error: unsupport coding form')
    '''

    pinyin_list = pinyin(txt, style = Style.TONE3)
    for item in pinyin_list:
        phone_list.append(seprate_syllable(pinyinformat(item[0])))
    return phone_list

"""
objective: 去除句子中的标点符号
input:
      text:输入有标点符号的句子。例如："想做/ 兼_职/学生_/ 的 、加,我Q：  1 5.  8 0. ！！？？  8 6 。0.  2。 3     有,惊,喜,哦"
output: 转换为去除标点顾浩的字符串。例如："想做兼职学生的加我Q：158086023有惊喜哦"
status: done
author: changshu
"""
def removal_punctuation(text):
    # text = "想做/ 兼_职/学生_/ 的 、加,我Q：  1 5.  8 0. ！！？？  8 6 。0.  2。 3     有,惊,喜,哦"
    # temp = temp.encode()
    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+","", text)
    # print(string)
    return string

"""
objective: 将文字转化为拼音加韵律的的形式
input:
      text:输入的中文文本
output: 转换为拼音加音律的字符串。例如：xiao3 ming2   shuo4 shi4
status: done
author: changshu
"""
def text_to_pinyin(text):
    text=removal_punctuation(text)
    # print("text:",text)
    # seg_list = jieba.cut(txt, cut_all=True) # 会切出重复的部分
    # print("Full Mode: " + " ".join(seg_list))  # 全模式
    # print("Full Mode: " + " ".join(seg_list))  # 全模式
    seg_list = jieba.cut(text, cut_all=False)  # 无重复的部分
    # print("Default Mode: " + " ".join(seg_list))  # 精确模式
    seg_list = " ".join(seg_list)
    result = pinyin(seg_list, style=Style.TONE3)
    result = [i for lst in result for i in lst]
    # print("result的结果",result)
    pinyin_str = [x.strip() for x in result]
    # print("x的结果", pinyin_str)
    pinyin_str = ' '.join(pinyin_str)
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~”“。！，、…—～﹏￥]+'
    pinyin_str = re.sub(r, '', pinyin_str)
    return pinyin_str

if __name__ == '__main__':
    # txt='你好看啊'
    # txt='中华人民共和国论居然'
    txt='小明硕士毕业于中国科学院计算所，后在日本京都大学深造'
    # print(txt2pinyin(txt))
    print(text_to_pinyin(txt))



'''
用法举例
print(txt2pinyin('中华人民共和国论居然'))
['zh ong1', 'h ua2', 'r en2', 'm in2', 'g ong4', 'h e2', 'g uo2', 'l uen4', 'j
v1', 'r an2']
'''
'''
seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))
'''

