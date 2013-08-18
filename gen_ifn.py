#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
* Copyright (c) 2013 Jeremy Parks. All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software\n"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.

Author: Jeremy Parks
Purpose: Generate the index, faq and nav page for each language
Note: Requires Python 2.7.x
'''
import localen, localde, localfr, locales
import codecs, os
from ftplib import FTP
# FTP Login
from ftp_info import ftp_url, ftp_user, ftp_pass

# Generate a faq using local strings
def faq(localText):
    with codecs.open(localText.path+u'faq.html', 'wb', encoding='utf-8') as f:
        f.write(u"<!DOCTYPE html>\n")
        f.write(u"<html>\n")
        f.write(u"<head>\n")
        f.write(u"	<title>%s</title>\n"%(localText.about))
        f.write(u"	<meta name=\"description\" content=\"ACCG FAQ and Contact information\">\n")
        f.write(u"	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n")
        f.write(u"	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n")
        f.write(u"	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n")
        f.write(u"	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n")
        f.write(u"	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n")
        f.write(u"</head>\n")
        f.write(u"<body>\n")
        f.write(localText.header%(u'faq.html',u'faq.html',u'faq.html'))
        f.write(u"<section class=\"main\">\n")
        f.write(u"%s: <br />\n"%(localText.costs))
        f.write(u"<form action=\"https://www.paypal.com/cgi-bin/webscr\" method=\"post\">\n")
        f.write(u"<input type=\"hidden\" name=\"cmd\" value=\"_s-xclick\">\n")
        f.write(u"<input type=\"hidden\" name=\"encrypted\" value=\"-----BEGIN PKCS7-----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-----END PKCS7-----\">\n")
        f.write(u"<input type=\"image\" src=\"https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif\" border=\"0\" name=\"submit\" alt=\"PayPal - The safer, easier way to pay online!\">\n")
        f.write(u"<img alt=\"\" border=\"0\" src=\"https://www.paypalobjects.com/en_US/i/scr/pixel.gif\" width=\"1\" height=\"1\">\n")
        f.write(u"</form> \n")
        f.write(u"<br />\n")
        f.write(u"%s\n"%(localText.gw2spidy))
        f.write(u"<br /><hr>\n")
        f.write(u"<a href=\"https://forum-en.guildwars2.com/forum/community/links/Dynamic-crafting-guides-for-all-8-crafts\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.oThread))
        f.write(u"<br />\n")
        f.write(u"<a href=\"http://www.reddit.com/r/Guildwars2/comments/179me8/dynamic_crafting_guides_for_all_crafts/\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.rThread))
        f.write(u"<br />\n")
        f.write(u"<a href=\"http://www.guildwars2guru.com/topic/80318-dynamic-crafting-guides-for-all-crafts-httpgw2craftssaladonnet/\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.gThread))
        f.write(u"<br />\n")
        f.write(u"<a href=\"https://twitter.com/Xanthic42\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.twitter))
        f.write(u"<br />\n")
        f.write(u"<a href=\"mailto:gw2crafts@live.com\" style=\"line-height:150%%;\"><strong>%s</strong></a> \n"%(localText.email))
        f.write(u"<br /><br />\n")
        f.write(u"%s\n"%(localText.contact))
        f.write(u"<br /><br /><hr>\n")
        f.write(u"<h3 style=\"text-align:center;\">[%s]</h3>\n"%(localText.faq))
        f.write(u"<hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.source))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> <a href=\"https://github.com/xanthics/gw2craft\">Github</a>\n"%(localText.answer))
        f.write(u"<br /><hr> \n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q1))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a11))
        f.write(u"<br />%s\n"%(localText.a12))
        f.write(u"<br />%s\n"%(localText.a13))
        f.write(u"<br />%s\n"%(localText.a14))
        f.write(u"<br />%s\n"%(localText.a15))
        f.write(u"<br />%s\n"%(localText.a16))
        f.write(u"<br /><br />%s\n"%(localText.a17))
        f.write(u"<br />%s\n"%(localText.a18))
        f.write(u"<br /><hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q2))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a2))
        f.write(u"<br /><hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q3))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a31))
        f.write(u"<br /><br />%s\n"%(localText.a32))
        f.write(u"<br /><hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q4))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a4))
        f.write(u"<br /><hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q5))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a51))
        f.write(u"<br /><br />%s\n"%(localText.a52))
        f.write(u"<br /><hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q6))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a6))
        f.write(u"<br /><hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q7))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a7))
        f.write(u"<br /><hr>\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.question,localText.q8))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a8))
        f.write(u"<br /><hr>\n")
        f.write(u"%s\n"%(localText.thanks))
        f.write(u"<br /><br />\n")
        f.write(u"%s\n"%(localText.thanks2))
        f.write(u"</section>\n")
        f.write(localText.cright)
        f.write(u"</body>\n")
        f.write(u"</html>\n")


# Generate a nav using local strings
def nav(localText):
    with codecs.open(localText.path+u'nav.html', 'wb', encoding='utf-8') as f:
        f.write(u"<!DOCTYPE html>\n")
        f.write(u"<html>\n")
        f.write(u"<head>\n")
        f.write(u"	<title>Nav Page</title>\n")
        f.write(u"	<meta name=\"description\" content=\"ACCG nav page\">\n")
        f.write(u"	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n")
        f.write(u"	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n")
        f.write(u"	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n")
        f.write(u"	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n")
        f.write(u"	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n")
        f.write(u"</head>\n")
        f.write(u"<body>\n")
        f.write(localText.header%('nav.html','nav.html','nav.html'))
        f.write(u"<section class=\"main\">\n")
        f.write(u"%s\n"%(localText.navNotice))
        f.write(u"<br /><br />\n")
        f.write(u"<a href=\"/\">%s</a><br />\n"%(localText.home))
        f.write(u"<a href=\"total.html\">%s</a><br />\n"%(localText.totals))
        f.write(u"<a href=\"faq.html\">%s</a>\n"%(localText.about))
        f.write(u"<h3>%s</h3>\n"%(localText.nGuides))
        f.write(u"%s<br />\n"%(localText.cooking))
        f.write(u"<ul>\n")
        f.write(u"<li><a href=\"cooking.html\">%s</a><br /></li>\n"%(localText.nHearts))
        f.write(u"<li><a href=\"cooking_karma_light.html\">%s</a><br /></li>\n"%(localText.tHearts))
        f.write(u"<li><a href=\"cooking_karma.html\">%s</a><br /></li>\n"%(localText.aHearts))
        f.write(u"</ul>\n")
        f.write(u"<a href=\"jewelcraft.html\">%s</a><br />\n"%(localText.jc))
        f.write(u"<a href=\"artificing.html\">%s</a><br />\n"%(localText.art))
        f.write(u"<a href=\"huntsman.html\">%s</a><br />\n"%(localText.hunt))
        f.write(u"<a href=\"weaponcraft.html\">%s</a><br />\n"%(localText.wc))
        f.write(u"<a href=\"armorcraft.html\">%s</a><br />\n"%(localText.ac))
        f.write(u"<a href=\"leatherworking.html\">%s</a><br />\n"%(localText.lw))
        f.write(u"<a href=\"tailor.html\">%s</a><br />\n"%(localText.tailor))
        f.write(u"<h3>%s</h3>\n"%(localText.fGuides))
        f.write(u"%s<br />\n"%(localText.cooking))
        f.write(u"<ul>\n")
        f.write(u"<li><a href=\"cooking_fast.html\">%s</a><br /></li>\n"%(localText.nHearts))
        f.write(u"<li><a href=\"cooking_karma_fast_light.html\">%s</a><br /></li>\n"%(localText.tHearts))
        f.write(u"<li><a href=\"cooking_karma_fast.html\">%s</a><br /></li>\n"%(localText.aHearts))
        f.write(u"</ul>\n")
        f.write(u"<a href=\"jewelcraft_fast.html\">%s</a><br />\n"%(localText.jc))
        f.write(u"<a href=\"artificing_fast.html\">%s</a><br />\n"%(localText.art))
        f.write(u"<a href=\"huntsman_fast.html\">%s</a><br />\n"%(localText.hunt))
        f.write(u"<a href=\"weaponcraft_fast.html\">%s</a><br />\n"%(localText.wc))
        f.write(u"<a href=\"armorcraft_fast.html\">%s</a><br />\n"%(localText.ac))
        f.write(u"<a href=\"leatherworking_fast.html\">%s</a><br />\n"%(localText.lw))
        f.write(u"<a href=\"tailor_fast.html\">%s</a>\n"%(localText.tailor))
        f.write(u"<h3>%s</h3>\n"%(localText.tGuides))
        f.write(u"<a href=\"jewelcraft_craft_all.html\">%s</a><br />\n"%(localText.jc))
        f.write(u"<a href=\"artificing_craft_all.html\">%s</a><br />\n"%(localText.art))
        f.write(u"<a href=\"huntsman_craft_all.html\">%s</a><br />\n"%(localText.hunt))
        f.write(u"<a href=\"weaponcraft_craft_all.html\">%s</a><br />\n"%(localText.wc))
        f.write(u"<a href=\"armorcraft_craft_all.html\">%s</a><br />\n"%(localText.ac))
        f.write(u"<a href=\"leatherworking_craft_all.html\">%s</a><br />\n"%(localText.lw))
        f.write(u"<a href=\"tailor_craft_all.html\">%s</a>\n"%(localText.tailor))
        f.write(u"<h3>%s:%s</h3>\n"%(localText.navLang,localText.lang))
        f.write(u"<a href=\"/\" hreflang=\"en\">English</a><br />\n")
        f.write(u"<a href=\"/fr/nav.html\" hreflang=\"fr\">Français</a><br />\n")
        f.write(u"<a href=\"/de/nav.html\" hreflang=\"de\">Deutsch</a><br />\n")
        f.write(u"<a href=\"/es/nav.html\" hreflang=\"es\">Español</a><br />\n")
        f.write(u"</section>\n")
        f.write(localText.cright)
        f.write(u"</body>\n")
        f.write(u"</html>\n")

# Generate and index using local strings
def index(localText):
    with codecs.open(localText.path+u'index.html', 'wb', encoding='utf-8') as f:
        f.write(u"<!DOCTYPE html>\n")
        f.write(u"<html>\n")
        f.write(u"<head>\n")
        f.write(u"	<title>ACCGs for Guild Wars 2</title>\n")
        f.write(u"	<meta name=\"description\" content=\"Always Current Crafting Guides for Guild Wars 2 with guides that are updated every 30 minutes based on current TP prices.  Multiple styles.\">\n")
        f.write(u"	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n")
        f.write(u"	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n")
        f.write(u"	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n")
        f.write(u"	<link rel=\"image_src\" href=\"apple-touch-icon-precomposed.png\">\n")
        f.write(u"	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n")
        f.write(u"	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n")
        f.write(u"</head>\n")
        f.write(u"<body>\n")
        f.write(localText.header%('index.html','index.html','index.html'))
        f.write(u"<section class=\"main\">\n")
#        f.write(u"<strong>%s</strong>: <a href=\"/\" hreflang=\"en\">English</a>, <a href=\"/fr/\" hreflang=\"fr\">Français</a>, <a href=\"/de/\" hreflang=\"de\">Deutsch</a>, <a href=\"/es/\" hreflang=\"es\">Español</a> (temporary to draw attention)\n<br />"%(localText.navLang))
        f.write(u"<strong>%s:</strong>\n"%(localText.fThings))
        f.write(u"<ul>\n")
        f.write(u"<li>%s</li>\n"%(localText.t1))
        f.write(u"<li>%s</li>\n"%(localText.t2))
        f.write(u"<li>%s</li>\n"%(localText.t3))
        f.write(u"<li>%s</li>\n"%(localText.t4))
        f.write(u"</ul><br />\n")
        f.write(u"<strong>%s:</strong> %s\n"%(localText.nGuides,localText.nge))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s:</strong> %s\n"%(localText.fGuides,localText.fge))
        f.write(u"<br /><br />\n")
        f.write(u"<strong>%s:</strong> %s\n"%(localText.tGuides,localText.tge))
        f.write(u"<br /><br />\n")
        f.write(u"%s\n"%(localText.wit))
        f.write(u"<br /><br />\n")
        f.write(u"%s\n"%(localText.nWarn))
        f.write(u"<br /><br />\n")
        f.write(u"%s\n"%(localText.rCost))
        f.write(u"<br /><hr>\n")
        f.write(u"%s\n"%(localText.thanks2))
        f.write(u"</section>\n")
        f.write(localText.cright)
        f.write(u"</body>\n")
        f.write(u"</html>\n")

def main():

    for lang in [localen, localde, localfr, locales]:
        faq(lang)
        nav(lang)
        index(lang)

    print "Starting upload"
    myFtp = FTP(ftp_url)
    myFtp.login(ftp_user,ftp_pass)
    for lang in ['',u'de/',u'fr/',u'es/']:
        for item in [u"nav.html", u"index.html", u"faq.html"]:
            with codecs.open(lang+item,u'rb') as f:
                myFtp.storbinary(u'STOR /gw2crafts.net/'+lang+item,f)
            os.remove(lang+item)
    myFtp.close()

# If ran directly, call main
if __name__ == '__main__':
    main()
