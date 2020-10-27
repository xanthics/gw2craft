#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Generate the index, faq and nav page for each language
Note: Requires Python 3.7.x
'''
import output
import Globals
from translations import Localcz, Localde, Localen, Locales, Localfr, Localptbr, Localzh


# Generate a faq using local strings
def faq(localText, free):
	page = "<!DOCTYPE html>\n"
	page += "<html>\n"
	page += "<head>\n"
	page += '''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->'''
	page += "	<title>%s</title>\n"%(localText.about)
	page += "	<meta name=\"description\" content=\"ACCG FAQ, Contact information, and Privacy Policy\">\n"
	page += '	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n'
	page += "	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n"
	page += '	<meta http-equiv="Cache-Control" content="public, max-age=7776000">\n'
	page += "	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n"
	page += "	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n"
	page += "	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n"
	page += "	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n"
	page += "</head>\n"
	page += "<body>\n"
	page += """<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
	page += Globals.header.format(localText.path, localText.home, localText.nGuides, localText.fGuides, localText.special, localText.cooking, localText.nHearts, localText.tHearts, localText.aHearts, localText.jc, localText.art, localText.hunt, localText.wc, localText.ac, localText.lw, localText.tailor, localText.scribe, localText.totals, localText.about, localText.lang, localText.lang_code, 'faq.html', 'free/' if free else '')
	page += "<section class=\"main\">\n"
	page += f"<strong>Notice:</strong> you are following a {'F2P' if free else 'Core'} guide.  <a href=\"{'/' if free else '/free/'}{localText.path}faq.html\">Click here for a {'Core' if free else 'F2P'} account guide</a>.<br />"

#	page += u"<a href=\"https://forum-en.guildwars2.com/forum/community/links/Dynamic-crafting-guides-for-all-8-crafts\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.oThread)
#	page += u"<br />\n"
#	page += u"<a href=\"http://www.reddit.com/r/Guildwars2/comments/179me8/dynamic_crafting_guides_for_all_crafts/\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.rThread)
#	page += u"<br />\n"
#	page += u"<a href=\"http://www.guildwars2guru.com/topic/80318-dynamic-crafting-guides-for-all-crafts-httpgw2craftssaladonnet/\" style=\"line-height:150%%;\"><strong>%s</strong></a>\n"%(localText.gThread)
#	page += u"<br />\n"
	page += "<a href=\"https://www.patreon.com/bePatron?u=33775051\" data-patreon-widget-type=\"become-patron-button\">Become a Patron!</a><script async src=\"https://c6.patreon.com/becomePatronButton.bundle.js\"></script>\n"
	page += "<br />\n"
	page += "<a href=\"mailto:gw2crafts@live.com\" style=\"line-height:150%%;\"><strong>%s</strong></a></br/> \n"%(localText.email)
#	page += u"<a href=\"http://gw2crafts.net/analytics/\" style=\"line-height:150%%;\"><strong>Analytics</strong></a>\n"
	page += "<br /><br />\n"
	page += "%s\n"%(localText.contact)
	page += "<br /><br /><hr>\n"
	page += "<h3 style=\"text-align:center;\">[%s]</h3>\n"%(localText.faq)
	page += "<hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.source)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> <a href=\"https://github.com/xanthics/gw2craft\">Github</a>\n"%(localText.answer)
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
	page += "<br /><hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.q2)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> %s\n"%(localText.answer,localText.a2)
	page += "<br /><hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.q3)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> %s\n"%(localText.answer,localText.a31)
	page += "<br /><br />%s\n"%(localText.a32)
	page += "<br /><hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.q4)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> %s\n"%(localText.answer,localText.a4)
	page += "<br /><hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.q5)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> %s\n"%(localText.answer,localText.a51)
	page += "<br /><br />%s\n"%(localText.a52)
	page += "<br /><hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.q6)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> %s\n"%(localText.answer,localText.a6)
	page += "<br /><hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.q7)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> %s\n"%(localText.answer,localText.a7)
	page += "<br /><hr>\n"
	page += "<strong>%s)</strong> %s\n"%(localText.question,localText.q8)
	page += "<br /><br />\n"
	page += "<strong>%s)</strong> %s\n"%(localText.answer,localText.a8)
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
	page += "<h3 style=\"text-align:center;\">[Privacy Policy]</h3>\n"
	page += "<p>This site makes use of default Google Analytics settings to evaluate usage over time which has an opt out option <a href=\"https://tools.google.com/dlpage/gaoptout/\" target=\"_blank\">here.</a>  Google Analytic's privacy policy can be found <a href=\"https://support.google.com/analytics/answer/6004245\" target=\"_blank\">here.</a></p>"
	page += "<p>Ezoic privacy policy should be embedded below but it can also be found <a href=\"https://g.ezoic.net/privacy/gw2crafts.net\" target=\"_blank\">here.</a></p>"
	page += "<p>No other data should be collected as this site does not use any local storage or cookies except as needed for Google Analytics and Ezoic.</p>"
	page += "<br /><br /><span id=\"ezoic-privacy-policy-embed\"></span>"

	page += "</section>\n"
	page += localText.cright
	page += "</body>\n"
	page += "</html>\n"

	output.write_file(f"{'free/' if free else ''}{localText.path}",'faq.html',page)
	return



# Generate a nav using local strings
def nav(localText, free):
	page = "<!DOCTYPE html>\n"
	page += "<html>\n"
	page += "<head>\n"
	# Ezoic adwords
	page += '''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->'''
	page += "	<title>Nav Page</title>\n"
	page += "	<meta name=\"description\" content=\"ACCG nav page\">\n"
	page += '	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n'
	page += "	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n"
	page += '	<meta http-equiv="Cache-Control" content="public, max-age=7776000">\n'
	page += "	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n"
	page += "	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n"
	page += "	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n"
	page += "	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n"
	page += "</head>\n"
	page += "<body>\n"
	page += """<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
	page += Globals.header.format(localText.path, localText.home, localText.nGuides, localText.fGuides, localText.special, localText.cooking, localText.nHearts, localText.tHearts, localText.aHearts, localText.jc, localText.art, localText.hunt, localText.wc, localText.ac, localText.lw, localText.tailor, localText.scribe, localText.totals, localText.about, localText.lang, localText.lang_code, 'nav.html', 'free/' if free else '')
	page += "<section class=\"main\">\n"
	page += f"<strong>Notice:</strong> you are following a {'F2P' if free else 'Core'} guide.  <a href=\"{'/' if free else '/free/'}{localText.path}nav.html\">Click here for a {'Core' if free else 'F2P'} account guide</a>.<br />"
	page += "%s\n"%(localText.navNotice)
	page += "<br /><br />\n"
	page += "<a href=\"/\">%s</a><br />\n"%(localText.home)
	page += "<a href=\"total.html\">%s</a><br />\n"%(localText.totals)
	page += "<a href=\"faq.html\">%s</a>\n"%(localText.about)
	page += "<h3>%s</h3>\n"%(localText.nGuides)
	page += "%s<br />\n"%(localText.cooking)
	page += "<ul>\n"
	page += "<li><a href=\"cooking.html\">%s</a><br /></li>\n"%(localText.nHearts)
	page += "<li><a href=\"cooking_karma_light.html\">%s</a><br /></li>\n"%(localText.tHearts)
	page += "<li><a href=\"cooking_karma.html\">%s</a><br /></li>\n"%(localText.aHearts)
	page += "</ul>\n"
	page += "<a href=\"jewelcraft.html\">%s</a><br />\n"%(localText.jc)
	page += "<a href=\"artificing.html\">%s</a><br />\n"%(localText.art)
	page += "<a href=\"huntsman.html\">%s</a><br />\n"%(localText.hunt)
	page += "<a href=\"weaponcraft.html\">%s</a><br />\n"%(localText.wc)
	page += "<a href=\"armorcraft.html\">%s</a><br />\n"%(localText.ac)
	page += "<a href=\"leatherworking.html\">%s</a><br />\n"%(localText.lw)
	page += "<a href=\"tailor.html\">%s</a><br />\n"%(localText.tailor)
	page += "<a href=\"scribe.html\">%s</a><br />\n"%(localText.scribe)
	page += "<h3>%s</h3>\n"%(localText.fGuides)
	page += "%s<br />\n"%(localText.cooking)
	page += "<ul>\n"
	page += "<li><a href=\"cooking_fast.html\">%s</a><br /></li>\n"%(localText.nHearts)
	page += "<li><a href=\"cooking_karma_fast_light.html\">%s</a><br /></li>\n"%(localText.tHearts)
	page += "<li><a href=\"cooking_karma_fast.html\">%s</a><br /></li>\n"%(localText.aHearts)
	page += "</ul>\n"
	page += "<a href=\"jewelcraft_fast.html\">%s</a><br />\n"%(localText.jc)
	page += "<a href=\"artificing_fast.html\">%s</a><br />\n"%(localText.art)
	page += "<a href=\"huntsman_fast.html\">%s</a><br />\n"%(localText.hunt)
	page += "<a href=\"weaponcraft_fast.html\">%s</a><br />\n"%(localText.wc)
	page += "<a href=\"armorcraft_fast.html\">%s</a><br />\n"%(localText.ac)
	page += "<a href=\"leatherworking_fast.html\">%s</a><br />\n"%(localText.lw)
	page += "<a href=\"tailor_fast.html\">%s</a>\n"%(localText.tailor)
	page += "<h3>400-500</h3>\n"
	page += "<a href=\"artificing_400.html\">{}</a><br />\n".format(localText.art)
	page += "<a href=\"huntsman_400.html\">{}</a><br />\n".format(localText.hunt)
	page += "<a href=\"weaponcraft_400.html\">{}</a><br />\n".format(localText.wc)
	page += "<a href=\"armorcraft_400.html\">{}</a><br />\n".format(localText.ac)
	page += "<a href=\"leatherworking_400.html\">{}</a><br />\n".format(localText.lw)
	page += "<a href=\"tailor_400.html\">{}</a><br />\n".format(localText.tailor)
	page += "<h3>{}</h3>\n".format(localText.special)
	page += "%s 1-200<br />\n"%(localText.cooking)
	page += "<ul>\n"
	page += "<li><a href=\"cooking_fast_200.html\">{}</a><br /></li>\n".format(localText.nHearts)
	page += "<li><a href=\"cooking_karma_fast_200.html\">{}</a><br /></li>\n".format(localText.aHearts)
	page += "</ul>\n"
	page += "400-450<br />\n"
	page += "<ul>\n"
	page += "<li><a href=\"cooking_450.html\">%s</a><br /></li>\n"%(localText.nHearts)
	page += "<li><a href=\"cooking_karma_450.html\">%s</a><br /></li>\n"%(localText.aHearts)
	page += "<li><a href=\"artificing_450.html\">{}</a><br /></li>\n".format(localText.art)
	page += "<li><a href=\"huntsman_450.html\">{}</a><br /></li>\n".format(localText.hunt)
	page += "<li><a href=\"weaponcraft_450.html\">{}</a><br /></li>\n".format(localText.wc)
	page += "<li><a href=\"armorcraft_450.html\">{}</a><br /></li>\n".format(localText.ac)
	page += "<li><a href=\"leatherworking_450.html\">{}</a><br /></li>\n".format(localText.lw)
	page += "<li><a href=\"tailor_450.html\">{}</a><br /></li>\n".format(localText.tailor)
	page += "</ul>\n"
	page += "<h3>%s:%s</h3>\n"%(localText.navLang,localText.lang)
	page += "<a href=\"/nav.html\" hreflang=\"en\">English</a><br />\n"
	page += "<a href=\"/fr/nav.html\" hreflang=\"fr\">Français</a><br />\n"
	page += "<a href=\"/cz/nav.html\" hreflang=\"cz\">Čeština</a><br />\n"
	page += "<a href=\"/de/nav.html\" hreflang=\"de\">Deutsch</a><br />\n"
	page += "<a href=\"/es/nav.html\" hreflang=\"es\">Español</a><br />\n"
	page += "</section>\n"
	page += localText.cright
	page += "</body>\n"
	page += "</html>\n"

	output.write_file(f"{'free/' if free else ''}{localText.path}",'nav.html',page)
	return


# Generate and index using local strings
def index(localText, free):
	page = "<!DOCTYPE html>\n"
	page += "<html>\n"
	page += "<head>\n"
	# Ezoic adwords
	page += '''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->'''
	page += "	<title>ACCGs for Guild Wars 2</title>\n"
	page += "	<meta name=\"description\" content=\"Always Current Crafting Guides for Guild Wars 2 with guides that are updated every 30 minutes based on current TP prices.  Multiple styles.\">\n"
	page += '	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n'
	page += "	<meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n"
	page += '	<meta http-equiv="Cache-Control" content="public, max-age=7776000">\n'
	page += "	<link href=\"/css/layout.css\" rel=\"stylesheet\" type=\"text/css\" />\n"
	page += "	<link rel=\"icon\" type=\"image/png\" href=\"/fi.gif\">\n"
	page += "	<link rel=\"image_src\" href=\"apple-touch-icon-precomposed.png\">\n"
	page += "	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js\"></script>\n"
	page += "	<script src=\"/js/menu.js\" type=\"text/javascript\"></script>\n"
	page += "</head>\n"
	page += "<body>\n"
	page += """<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
#	page += u"<div id=\"fb-root\"></div><script>(function(d, s, id) {var js, fjs = d.getElementsByTagName(s)[0];if (d.getElementById(id)) return;js = d.createElement(s); js.id = id;js.src = \"//connect.facebook.net/en_US/all.js#xfbml=1\";fjs.parentNode.insertBefore(js, fjs);}(document, 'script', 'facebook-jssdk'));</script>"
	page += Globals.header.format(localText.path, localText.home, localText.nGuides, localText.fGuides, localText.special, localText.cooking, localText.nHearts, localText.tHearts, localText.aHearts, localText.jc, localText.art, localText.hunt, localText.wc, localText.ac, localText.lw, localText.tailor, localText.scribe, localText.totals, localText.about, localText.lang, localText.lang_code, 'index.html', 'free/' if free else '')
	page += "<section class=\"main\">\n"
	page += f"<strong>Notice:</strong> you are following a {'F2P' if free else 'Core'} guide.  <a href=\"{'/' if free else '/free/'}{localText.path}index.html\">Click here for a {'Core' if free else 'F2P'} account guide</a>.<br />"
#	page += u"<p>The scribe guides need a new guild with unlocks as RiFa appears to be defunct.  Please email me at <a href=\"mailto:gw2crafts@live.com\">gw2crafts@live.com</a> if you have a guild that can accommodate.  Would need a contact name and guild, they will go on the scribe page.</p>"
	page += "<p>All guide pages now have a permalink, at the top in the warning, to a cached version.  Amazon claims unlimited space, so these likely won't be deleted.</p>"
	page += "<p>Support for Cooking 400-450 has been added.  450+ needs to be done via the in-game quest system and cannot be handled by these guides.</p>"
#	page += u"\t<div class=\"g-plusone\" data-size=\"medium\" data-href=\"http://gw2crafts.net\"></div><script type=\"text/javascript\">(function() {var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;po.src = 'https://apis.google.com/js/plusone.js';var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);})();</script>\n"
#	page += u"\t<div class=\"fb-like\" data-href=\"http://gw2crafts.net\" data-width=\"150\" data-layout=\"button_count\" data-show-faces=\"false\" data-send=\"false\"></div>"
	page += "<hr>"
#	page += u"<strong>%s</strong>: <a href=\"/\" hreflang=\"en\">English</a>, <a href=\"/fr/\" hreflang=\"fr\">Français</a>, <a href=\"/de/\" hreflang=\"de\">Deutsch</a>, <a href=\"/es/\" hreflang=\"es\">Español</a> (temporary to draw attention)\n<br />"%(localText.navLang)
	page += "<strong>%s</strong><br /><br />\n"%(localText.region)
	page += "<strong>%s:</strong>\n"%(localText.fThings)
	page += "<ul>\n"
	page += "<li>%s</li>\n"%(localText.t1)
	page += "<li>%s</li>\n"%(localText.t2)
	page += "<li>%s</li>\n"%(localText.t3)
	page += "<li>%s</li>\n"%(localText.t4)
	page += "</ul><br />\n"
	page += "<strong>%s:</strong> %s\n"%(localText.nGuides,localText.nge)
	page += "<br /><br />\n"
	page += "<strong>%s:</strong> %s\n"%(localText.fGuides,localText.fge)
	page += "<br /><br />\n"
	page += "%s\n"%(localText.wit)
	page += "<br /><br />\n"
	page += "%s\n"%(localText.nWarn)
	page += "<br /><br />\n"
	page += "%s\n"%(localText.rCost)
#	page += u"<br /><hr>\n"
#	page += u"%s\n<br />"%(localText.thanks2)
	# adword adaptive
	page += '<br /><hr><br /><div style="width: 100%;display:block;">\n \
<!-- Ezoic - Tail - bottom_of_page -->\n \
<div id="ezoic-pub-ad-placeholder-102"></div>\n \
<!-- End Ezoic - Tail - bottom_of_page --></div>\n'
	page += "</section>\n"
	page += localText.cright
	page += "</body>\n"
	page += "</html>\n"

	output.write_file(f"{'free/' if free else ''}{localText.path}",'index.html',page)
	return


def main():
	for free in [True, False]:
		for lang in [Localen, Localde, Localfr, Locales, Localcz, Localptbr, Localzh]:
			print(lang, free)
			faq(lang, free)
			nav(lang, free)
			index(lang, free)


# If ran directly, call main
if __name__ == '__main__':
	main()
