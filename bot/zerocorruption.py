#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from calendar import monthrange
import mysql.connector
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


TIL,HOLAT,TASHKILOT,XABAR,MUROJAT,ENDMUROJAT = range(6)


def start(update, context):
    reply_keyboard = [['🇺🇿 O`zbekcha','🇷🇺 Русский']]
    update.message.reply_text(
        'Assalamu alaykum.Korrupsiya haqida xabar beruvchi telegram botiga Xush kelibsiz.'
        '\n\nIltimos, Tilni tanlang:\nВыберите язык:\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True,one_time_keyboard=True))

    return TIL

def til(update, context):
    reply_keyboard_uz = [['Korrupsiyaga duch keldim va pora berishga majbur bo`ldim'],['Korrupsiyaga duch keldim va pora bermadim'],['Pora bilan bog`liq bo`lmagan korrupsiyaga duch keldim'],['Halol ishlaydigan davlat xizmatchisini uchratdim'],['Orqaga']]
    user = update.message.from_user
    text1 = update.message.text 
    logger.info("%sning tanlagan tili: %s", user.first_name, update.message.text)
    if text1 == '🇺🇿 O`zbekcha' or text1 == 'Yangi murojaat qoldirish':
        update.message.reply_text(
            'Siz korrupsiya bo`yicha qanday holatga duch keldingiz?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_uz,resize_keyboard=True, one_time_keyboard=True))

    return HOLAT

#HOLAT
def holat(update, context):
    reply_keyboard = [['Vazirliklar','Mahalliy davlat hokimiyati organlari'],['Banklar','Davlat qo`mitalari'],['Orqaga']]
    if update.message.text == 'Orqaga':
        reply_keyboard = [['🇺🇿 O`zbekcha','🇷🇺 Русский']]
        update.message.reply_text(
            'Iltimos, Tilni tanlang:\nВыберите язык:\n',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True,one_time_keyboard=True))
        return TIL
    user = update.message.from_user
    logger.info("%sning tanlov turi: %s", user.first_name, update.message.text)
    context.user_data['holat'] = update.message.text
    update.message.reply_text(
        'Organni tanlang:',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True,one_time_keyboard=True))
    return TASHKILOT


#TASHKILOT
def tashkilot(update, context):
    reply_keyboard = []
    if update.message.text == 'Orqaga':
        reply_keyboard = [['Korrupsiyaga duch keldim va pora berishga majbur bo`ldim'],['Korrupsiyaga duch keldim va pora bermadim'],['Pora bilan bog`liq bo`lmagan korrupsiyaga duch keldim'],['Halol ishlaydigan davlat xizmatchisini uchratdim'],['Orqaga']]
        update.message.reply_text(
            'Siz korrupsiya bo`yicha qanday holatga duch keldingiz?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
        return HOLAT
    context.user_data['organ'] = update.message.text
    if update.message.text == 'Vazirliklar':
        file1 = open('list.txt', 'r',encoding="utf8")
        Lines = file1.readlines()
        for line in Lines:
            test1 = []
            test1.append(line.strip())
            reply_keyboard.append(test1)
        update.message.reply_text(
            'Tashkilotni tanlang:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))  

        return XABAR

    if update.message.text == 'Mahalliy davlat hokimiyati organlari':
        file1 = open('list1.txt', 'r',encoding="utf8")
        Lines = file1.readlines()
        for line in Lines:
            test1 = []
            test1.append(line.strip())
            reply_keyboard.append(test1)
        update.message.reply_text(
            'Tashkilotni tanlang:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))    
    
        return XABAR

    if update.message.text == 'Banklar':
        file1 = open('list2.txt', 'r',encoding="utf8")
        Lines = file1.readlines()
        for line in Lines:
            test1 = []
            test1.append(line.strip())
            reply_keyboard.append(test1)
        update.message.reply_text(
            'Tashkilotni tanlang:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
    
        return XABAR

    if update.message.text == 'Davlat qo`mitalari':
        file1 = open('list3.txt', 'r',encoding="utf8")
        Lines = file1.readlines()
        for line in Lines:
            test1 = []
            test1.append(line.strip())
            reply_keyboard.append(test1)
        update.message.reply_text(
            'Tashkilotni tanlang:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))

        return XABAR

#XABAR
def xabar(update, context):
    reply_keyboard = [['Orqaga']]
    if update.message.text == 'Orqaga':
        reply_keyboard = [['Vazirliklar','Mahalliy davlat hokimiyati organlari'],['Banklar','Davlat qo`mitalari'],['Orqaga']]
        update.message.reply_text(
            'Organni tanlang:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
        return TASHKILOT
    context.user_data['tashkilot'] = update.message.text

    update.message.reply_text(
            'Hodisa haqida ma`lumot bering (qanday,kim tomonidan,kimlar ishtirokida):',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
    return MUROJAT


#MUROJAT
def murojat(update,context):
    if update.message.text == 'Orqaga':
        reply_keyboard = [['Vazirliklar','Mahalliy davlat hokimiyati organlari'],['Banklar','Davlat qo`mitalari'],['Orqaga']]
        update.message.reply_text(
            'Organni tanlang:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
        return TASHKILOT
    reply_keyboard = [['Yangi murojaat qoldirish']]
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="zerocorruption")
    mycursor = mydb.cursor()
    sql = "INSERT INTO murojat (murojatchi, holat,organ,tashkilot,murojat_matni) VALUES (%s, %s,%s,%s,%s)"
    val = (update.message.from_user.first_name,context.user_data['holat'],context.user_data['organ'],context.user_data['tashkilot'],update.message.text)
    mycursor.execute(sql,val)
    mydb.commit()
    murojat_id = mycursor.lastrowid
    update.message.reply_text(
            'Murojaat raqami:'+str(murojat_id)+'\nMurojaatingiz qabul qilindi!',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
    return ENDMUROJAT
    

#ENDMUROJAT
def endmurojat(update,context):
    if update.message.text == 'Orqaga':
        reply_keyboard = [['Vazirliklar','Mahalliy davlat hokimiyati organlari'],['Banklar','Davlat qo`mitalari'],['Orqaga']]
        update.message.reply_text(
            'Organni tanlang:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
        return TASHKILOT

    if update.message.text == 'Yangi murojaat qoldirish':
        reply_keyboard = [['Korrupsiyaga duch keldim va pora berishga majbur bo`ldim'],['Korrupsiyaga duch keldim va pora bermadim'],['Pora bilan bog`liq bo`lmagan korrupsiyaga duch keldim'],['Halol ishlaydigan davlat xizmatchisini uchratdim'],['Orqaga']]
        update.message.reply_text(
            'Siz korrupsiya bo`yicha qanday holatga duch keldingiz?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True))
        return HOLAT

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Telegram botimizda ko`rishguncha, Xayr!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("5066747231:AAHixapdIV_8qjtt52drb-9_OKfLpQ_135Y", use_context=True)


    dp = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            TIL: [MessageHandler(Filters.regex('^(🇺🇿 O`zbekcha|🇷🇺 Русский)$'), til)],
            HOLAT: [MessageHandler(Filters.regex('^(Korrupsiyaga duch keldim va pora berishga majbur bo`ldim|Korrupsiyaga duch keldim va pora bermadim|Pora bilan bog`liq bo`lmagan korrupsiyaga duch keldim|Halol ishlaydigan davlat xizmatchisini uchratdim|Orqaga|Yangi murojaat qoldirish)$'), holat)],
            TASHKILOT: [MessageHandler(Filters.regex('^(Vazirliklar|Mahalliy davlat hokimiyati organlari|Banklar|Davlat qo`mitalari|Orqaga)$'), tashkilot)],
            XABAR: [MessageHandler(Filters.text, xabar)], 
            MUROJAT: [MessageHandler(Filters.text, murojat)],
            ENDMUROJAT:[MessageHandler(Filters.text, endmurojat)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)


    dp.add_error_handler(error)

 
    updater.start_polling()


    updater.idle()


if __name__ == '__main__':
    main()