#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Generate the index, faq and nav page for each language
Note: Requires Python 2.7.x
'''
import output
from translations import Localcz, Localde, Localen, Locales, Localfr, Localptbr, Localzh


# Generate a faq using local strings
def faq(localText):
	page = u"<!DOCTYPE html>\n"
	page += u"<html>\n"
	page += u"<head>\n"
	page += u'''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->'''
	page += u"	<title>%s</title>\n"%(localText.about)
	page += u"	<meta name=\"description\" content=\"ACCG FAQ and Contact information\">\n"
	page += u'	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n'
	page += u"	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n"
	page += u"	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n"
	page += u"	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n"
	page += u"	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n"
	page += u"	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n"
	page += u"</head>\n"
	page += u"<body>\n"
	page += u"""<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
	page += localText.header%(u'faq.html',u'faq.html',u'faq.html',u'faq.html',u'faq.html',u'faq.html')
	page += u"<section class=\"main\">\n"
#	page += u"<a href=\"https://forum-en.guildwars2.com/forum/community/links/Dynamic-crafting-guides-for-all-8-crafts\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.oThread)
#	page += u"<br />\n"
#	page += u"<a href=\"http://www.reddit.com/r/Guildwars2/comments/179me8/dynamic_crafting_guides_for_all_crafts/\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.rThread)
#	page += u"<br />\n"
#	page += u"<a href=\"http://www.guildwars2guru.com/topic/80318-dynamic-crafting-guides-for-all-crafts-httpgw2craftssaladonnet/\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.gThread)
#	page += u"<br />\n"
	page += u"<a href=\"https://twitter.com/gw2crafts\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.twitter)
	page += u"<br />\n"
	page += u"<a href=\"mailto:gw2crafts@live.com\" style=\"line-height:150%%;\"><strong>%s</strong></a></br/> \n"%(localText.email)
#	page += u"<a href=\"http://gw2crafts.net/analytics/\" style=\"line-height:150%%;\"><strong>Analytics</strong></a>\n"
	page += u"<br /><br />\n"
	page += u"%s\n"%(localText.contact)
	page += u"<br /><br /><hr>\n"
	page += u"<h3 style=\"text-align:center;\">[%s]</h3>\n"%(localText.faq)
	page += u"<hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.source)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> <a href=\"https://github.com/xanthics/gw2craft\">Github</a>\n"%(localText.answer)
#	page += u"<br /><hr> \n"
#	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q1))
#	page += u"<br /><br />\n"
#	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a11))
#	page += u"<br />%s\n"%(localText.a12))
#	page += u"<br />%s\n"%(localText.a13))
#	page += u"<br />%s\n"%(localText.a14))
#	page += u"<br />%s\n"%(localText.a15))
#	page += u"<br />%s\n"%(localText.a16))
#	page += u"<br /><br />%s\n"%(localText.a17))
#	page += u"<br />%s\n"%(localText.a18))
	page += u"<br /><hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q2)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a2)
	page += u"<br /><hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q3)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a31)
	page += u"<br /><br />%s\n"%(localText.a32)
	page += u"<br /><hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q4)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a4)
	page += u"<br /><hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q5)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a51)
	page += u"<br /><br />%s\n"%(localText.a52)
	page += u"<br /><hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q6)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a6)
	page += u"<br /><hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q7)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a7)
	page += u"<br /><hr>\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.question,localText.q8)
	page += u"<br /><br />\n"
	page += u"<strong>%s)</strong> %s\n"%(localText.answer,localText.a8)
#	page += u"<br /><hr>\n"
#	page += u"%s\n"%(localText.thanks)
#	page += u"<br /><br />\n"
#	page += u"%s\n"%(localText.thanks2)
#	page += u"<hr>%s: <br />\n"%(localText.costs)
#	page += u"<br />YTD: $217 USD <form action=\"https://www.paypal.com/cgi-bin/webscr\" method=\"post\" >\n"
#	page += u"<input type=\"hidden\" name=\"cmd\" value=\"_s-xclick\">\n"
#	page += u"<input type=\"hidden\" name=\"encrypted\" value=\"-----BEGIN PKCS7-----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-----END PKCS7-----\">\n"
#	page += u"<input type=\"image\" src=\"https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif\" border=\"0\" name=\"submit\" alt=\"PayPal - The safer, easier way to pay online!\">\n"
#	page += u"<img alt=\"\" border=\"0\" src=\"https://www.paypalobjects.com/en_US/i/scr/pixel.gif\" width=\"1\" height=\"1\">\n"
#	page += u"</form> \n"
#	page += u"<br /><br /><script src=\"http://coinwidget.com/widget/coin.js\"></script><script>CoinWidgetCom.go({wallet_address: \"18Muvgz2zYeUYcAwrqM24awXkv2WqsLukt\", currency: \"bitcoin\", counter: \"amount\", alignment: \"al\", qrcode: true, auto_show: false, lbl_button: \"Donate\", lbl_address: \"My Bitcoin Address:\", lbl_count: \"donations\", lbl_amount: \"BTC\"});</script>"
	page += u"</section>\n"
	page += localText.cright
	page += u"</body>\n"
	page += u"</html>\n"

	output.write_file(localText.path,u'faq.html',page)
	return



# Generate a nav using local strings
def nav(localText):
	page = u"<!DOCTYPE html>\n"
	page += u"<html>\n"
	page += u"<head>\n"
	# Ezoic adwords
	page += u'''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->'''
	page += u"	<title>Nav Page</title>\n"
	page += u"	<meta name=\"description\" content=\"ACCG nav page\">\n"
	page += u'	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n'
	page += u"	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n"
	page += u"	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n"
	page += u"	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n"
	page += u"	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n"
	page += u"	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n"
	page += u"</head>\n"
	page += u"<body>\n"
	page += u"""<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
	page += localText.header%('nav.html','nav.html','nav.html','nav.html','nav.html','nav.html')
	page += u"<section class=\"main\">\n"
	page += u"%s\n"%(localText.navNotice)
	page += u"<br /><br />\n"
	page += u"<a href=\"/\">%s</a><br />\n"%(localText.home)
	page += u"<a href=\"total.html\">%s</a><br />\n"%(localText.totals)
	page += u"<a href=\"faq.html\">%s</a>\n"%(localText.about)
	page += u"<h3>%s</h3>\n"%(localText.nGuides)
	page += u"%s<br />\n"%(localText.cooking)
	page += u"<ul>\n"
	page += u"<li><a href=\"cooking.html\">%s</a><br /></li>\n"%(localText.nHearts)
	page += u"<li><a href=\"cooking_karma_light.html\">%s</a><br /></li>\n"%(localText.tHearts)
	page += u"<li><a href=\"cooking_karma.html\">%s</a><br /></li>\n"%(localText.aHearts)
	page += u"</ul>\n"
	page += u"<a href=\"jewelcraft.html\">%s</a><br />\n"%(localText.jc)
	page += u"<a href=\"artificing.html\">%s</a><br />\n"%(localText.art)
	page += u"<a href=\"huntsman.html\">%s</a><br />\n"%(localText.hunt)
	page += u"<a href=\"weaponcraft.html\">%s</a><br />\n"%(localText.wc)
	page += u"<a href=\"armorcraft.html\">%s</a><br />\n"%(localText.ac)
	page += u"<a href=\"leatherworking.html\">%s</a><br />\n"%(localText.lw)
	page += u"<a href=\"tailor.html\">%s</a><br />\n"%(localText.tailor)
	page += u"<a href=\"scribe.html\">%s</a><br />\n"%(localText.scribe)
	page += u"<h3>%s</h3>\n"%(localText.fGuides)
	page += u"%s<br />\n"%(localText.cooking)
	page += u"<ul>\n"
	page += u"<li><a href=\"cooking_fast.html\">%s</a><br /></li>\n"%(localText.nHearts)
	page += u"<li><a href=\"cooking_karma_fast_light.html\">%s</a><br /></li>\n"%(localText.tHearts)
	page += u"<li><a href=\"cooking_karma_fast.html\">%s</a><br /></li>\n"%(localText.aHearts)
	page += u"</ul>\n"
	page += u"<a href=\"jewelcraft_fast.html\">%s</a><br />\n"%(localText.jc)
	page += u"<a href=\"artificing_fast.html\">%s</a><br />\n"%(localText.art)
	page += u"<a href=\"huntsman_fast.html\">%s</a><br />\n"%(localText.hunt)
	page += u"<a href=\"weaponcraft_fast.html\">%s</a><br />\n"%(localText.wc)
	page += u"<a href=\"armorcraft_fast.html\">%s</a><br />\n"%(localText.ac)
	page += u"<a href=\"leatherworking_fast.html\">%s</a><br />\n"%(localText.lw)
	page += u"<a href=\"tailor_fast.html\">%s</a>\n"%(localText.tailor)
	page += u"<h3>400-500</h3>\n"
	page += u"<a href=\"artificing_400.html\">{}</a><br />\n".format(localText.art)
	page += u"<a href=\"huntsman_400.html\">{}</a><br />\n".format(localText.hunt)
	page += u"<a href=\"weaponcraft_400.html\">{}</a><br />\n".format(localText.wc)
	page += u"<a href=\"armorcraft_400.html\">{}</a><br />\n".format(localText.ac)
	page += u"<a href=\"leatherworking_400.html\">{}</a><br />\n".format(localText.lw)
	page += u"<a href=\"tailor_400.html\">{}</a><br />\n".format(localText.tailor)
	page += u"<h3>{}</h3>\n".format(localText.special)
	page += u"%s 1-200<br />\n"%(localText.cooking)
	page += u"<ul>\n"
	page += u"<li><a href=\"cooking_fast_200.html\">{}</a><br /></li>\n".format(localText.nHearts)
	page += u"<li><a href=\"cooking_karma_fast_200.html\">{}</a><br /></li>\n".format(localText.aHearts)
	page += u"</ul>\n"
	page += u"400-450<br />\n"
	page += u"<ul>\n"
	page += u"<li><a href=\"artificing_450.html\">{}</a><br /></li>\n".format(localText.art)
	page += u"<li><a href=\"huntsman_450.html\">{}</a><br /></li>\n".format(localText.hunt)
	page += u"<li><a href=\"weaponcraft_450.html\">{}</a><br /></li>\n".format(localText.wc)
	page += u"<li><a href=\"armorcraft_450.html\">{}</a><br /></li>\n".format(localText.ac)
	page += u"<li><a href=\"leatherworking_450.html\">{}</a><br /></li>\n".format(localText.lw)
	page += u"<li><a href=\"tailor_450.html\">{}</a><br /></li>\n".format(localText.tailor)
	page += u"</ul>\n"
	page += u"<h3>%s:%s</h3>\n"%(localText.navLang,localText.lang)
	page += u"<a href=\"/nav.html\" hreflang=\"en\">English</a><br />\n"
	page += u"<a href=\"/fr/nav.html\" hreflang=\"fr\">Français</a><br />\n"
	page += u"<a href=\"/cz/nav.html\" hreflang=\"cz\">Čeština</a><br />\n"
	page += u"<a href=\"/de/nav.html\" hreflang=\"de\">Deutsch</a><br />\n"
	page += u"<a href=\"/es/nav.html\" hreflang=\"es\">Español</a><br />\n"
	page += u"</section>\n"
	page += localText.cright
	page += u"</body>\n"
	page += u"</html>\n"

	output.write_file(localText.path,u'nav.html',page)
	return

# Generate and index using local strings
def index(localText):
	page = u"<!DOCTYPE html>\n"
	page += u"<html>\n"
	page += u"<head>\n"
	# Ezoic adwords
	page += u'''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->'''
	page += u"	<title>ACCGs for Guild Wars 2</title>\n"
	page += u"	<meta name=\"description\" content=\"Always Current Crafting Guides for Guild Wars 2 with guides that are updated every 30 minutes based on current TP prices.  Multiple styles.\">\n"
	page += u'	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n'
	page += u"	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n"
	page += u"	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n"
	page += u"	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n"
	page += u"	<link rel=\"image_src\" href=\"apple-touch-icon-precomposed.png\">\n"
	page += u"	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n"
	page += u"	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n"
	page += u"</head>\n"
	page += u"<body>\n"
	page += u"""<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
#	page += u"<div id=\"fb-root\"></div><script>(function(d, s, id) {var js, fjs = d.getElementsByTagName(s)[0];if (d.getElementById(id)) return;js = d.createElement(s); js.id = id;js.src = \"//connect.facebook.net/en_US/all.js#xfbml=1\";fjs.parentNode.insertBefore(js, fjs);}(document, 'script', 'facebook-jssdk'));</script>"
	page += localText.header%(u'index.html',u'index.html',u'index.html',u'index.html',u'index.html',u'index.html')
	page += u"<section class=\"main\">\n"
	page += u"<a href=\"https://twitter.com/gw2crafts\" class=\"twitter-follow-button\" data-show-count=\"true\" data-dnt=\"true\">Follow @gw2crafts</a>\n<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>"
#	page += u"\t<div class=\"g-plusone\" data-size=\"medium\" data-href=\"http://gw2crafts.net\"></div><script type=\"text/javascript\">(function() {var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;po.src = 'https://apis.google.com/js/plusone.js';var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);})();</script>\n"
#	page += u"\t<div class=\"fb-like\" data-href=\"http://gw2crafts.net\" data-width=\"150\" data-layout=\"button_count\" data-show-faces=\"false\" data-send=\"false\"></div>"
	page += u"<hr>"
#	page += u"<strong>%s</strong>: <a href=\"/\" hreflang=\"en\">English</a>, <a href=\"/fr/\" hreflang=\"fr\">Français</a>, <a href=\"/de/\" hreflang=\"de\">Deutsch</a>, <a href=\"/es/\" hreflang=\"es\">Español</a> (temporary to draw attention)\n<br />"%(localText.navLang)
	page += u"<strong>%s</strong><br /><br />\n"%(localText.region)
	page += u"<strong>%s:</strong>\n"%(localText.fThings)
	page += u"<ul>\n"
	page += u"<li>%s</li>\n"%(localText.t1)
	page += u"<li>%s</li>\n"%(localText.t2)
	page += u"<li>%s</li>\n"%(localText.t3)
	page += u"<li>%s</li>\n"%(localText.t4)
	page += u"</ul><br />\n"
	page += u"<strong>%s:</strong> %s\n"%(localText.nGuides,localText.nge)
	page += u"<br /><br />\n"
	page += u"<strong>%s:</strong> %s\n"%(localText.fGuides,localText.fge)
	page += u"<br /><br />\n"
	page += u"%s\n"%(localText.wit)
	page += u"<br /><br />\n"
	page += u"%s\n"%(localText.nWarn)
	page += u"<br /><br />\n"
	page += u"%s\n"%(localText.rCost)
#	page += u"<br /><hr>\n"
#	page += u"%s\n<br />"%(localText.thanks2)
	# adword adaptive
	page += u'<br /><hr><br /><div style="width: 100%;display:block;">\n \
<!-- Ezoic - Tail - bottom_of_page -->\n \
<div id="ezoic-pub-ad-placeholder-102"></div>\n \
<!-- End Ezoic - Tail - bottom_of_page --></div>\n'
	page += u"</section>\n"
	page += localText.cright
	page += u"</body>\n"
	page += u"</html>\n"

	output.write_file(localText.path,u'index.html',page)
	return


def main():
	for lang in [Localen, Localde, Localfr, Locales, Localcz, Localptbr, Localzh]:
		print lang
		faq(lang)
		nav(lang)
		index(lang)


# If ran directly, call main
if __name__ == '__main__':
	main()
