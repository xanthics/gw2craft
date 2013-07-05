# -*- coding: utf-8 -*-
'''
* Copyright (c) 2013 Jeremy Parks. All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
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
Purpose: de Localized text
Note: Requires Python 2.7.x
'''


# Copyright notice for GW2 IP
cright = u'''<footer>
    Guild Wars 2 © 2012 ArenaNet, Inc. Alle Rechte vorbehalten. NCsoft, das ineinander greifende NC-Logo, ArenaNet, Guild Wars, Guild Wars Factions, Guild Wars Nightfall, Guild Wars: Eye sind der Norden, Guild Wars 2 und alle in Verbindung stehenden Logos und Designs sind Warenzeichen oder eingetragene Warenzeichen der NCsoft Corporation. Alle anderen Warenzeichen sind das Eigentum ihrer jeweiligen Eigentümer.
</footer>'''

# renown heart vendors
crandle    = u"Agent Crandle - Fort Trinity(Straits of Devastation 70-75)"
aidem      = u"Aidem Finlay - Hidden Lake(Brisban Wildlands 15-25)"
albin      = u"Albin Chronicler - The Icesteppes(Wayfarer Foothills 1-15)"
jack       = u"Apple Jack(16c per) - Cornucopian Fields(Gendarran Fields 25-35)"
victor     = u"Assistant Chef Victor - Scaver Plateau(Queensdale 1-15)"
bjarni     = u"Bjarni - Breakneck Pass(Wayfarer Foothills 1-15)"
braxa      = u"Braxa Scalehunter - Champion's Shield(Iron Marches 50-60)"
jenks      = u"Deputy Jenks - Giant's Passage (Kessex Hills 15-25)"
disa       = u"Disa - Snowslide Ravine(Dredgehaunt Cliffs 40-50)"
drottot    = u"Drottot Lashtail - Devourer's Mouth(Plains of Ashford 1-15)"
elain      = u"Elain - Grenbrack Delves(Caledon Forest 1-15)"
jenrys     = u"Environmental Activist Jenrys - Judgement Rock(Mount Maelstrom 60-70)"
eona       = u"Eona - Mabon Market(Caledon Forest 1-15)"
makayla    = u"Fallen Angel Makayla - Stronghold of Ebonhawke(Fields of Ruin 30-40)"
eda        = u"Farmer Eda - Shaemoor Fields(Queensdale 1-15)"
leius      = u"Field Medic Leius - Nebo Terrace(Gendarran Fields 25-35)"
glubb      = u"Glubb - Degun Shun(Blazeridge Steppes 40-50)"
hune       = u"Hune - The Thunderhorns(Lornar's Pass 25-40)"
ichtaca    = u"Ichtaca - Hunting Banks(Timberline Falls 50-60)"
kastaz     = u"Kastaz Strongpaw - Noxin Dells(Diessa Plateau 15-25)"
laewyn     = u"Laewyn - Wychmire Swamp(Caledon Forest 1-15)"
laudren    = u"Laudren - Thundertroll Swamp(Sparkfly Fen 55-65)"
pickins    = u"Lieutenant Pickins - Greystone Rise(Harathi Hinterlands 35-45)"
summers    = u"Lieutenant Summers - Nightguard Beach(Harathi Hinterlands 35-45)"
auda       = u"Lionguard Auda - Dragon's Rising(Silverpeak Mountains 15-25)"
tunnira    = u"Lionscout Tunnira - Archen Foreland(Bloodtide Coast 45-55)"
kevach     = u"Lodge Keeper Kevach - Dolyak Pass(Wayfarer Foothills 1-15)"
mcov       = u"Master Craftsman or Vendor"
maxtar     = u"Maxtar Rapidstep - Dolyak Pass(Wayfarer Foothills 1-15)"
milton     = u"Milton Book - Cornucopian Fields(Gendarran Fields 25-35)"
naknar     = u"Naknar - Ebbing Heart Run(Iron Marches 50-60)"
nrocroc    = u"Nrocroc Chief - Apostate Wastes(Fireheart Rise 60-70)"
hrouda     = u"PR&T Senior Investigator Hrouda - Akk Wilds(Metrica Province 1-15)"
pochtecatl = u"Pochtecatl - Jelako Cliffrise(Bloodtide Coast 45-55)"
hrappa     = u"Researcher Hrappa - Voloxian Passage(Metrica Province 1-15)"
sagum      = u"Sagum Relicseeker - Agnos Gorge(Plains of Ashford 1-15)"
sangdo     = u"Sangdo Swiftwing - Cereboth Canyon(Kessex Hills 15-25)"
tholin     = u"Scholar Tholin - Krongar Pass(Timberline Falls 50-60)"
vejj       = u"Security Captain Vejj - Almuten Estates(Gendarran Fields 25-35)"
triktiki   = u"Sentry Triktiki - Arcallion Digs(Harathi Hinterlands 35-45)"
brian      = u"Seraph Archer Brian - Ossencrest Climb(Snowden Drifts 15-25)"
goran      = u"Seraph Soldier Goran - The Wendon Steps(Brisban Wildlands 15-25)"
shelp      = u"Shelp - Degun Shun(Blazeridge Steppes 40-50)"
vaastas    = u"Vaastas Meatslayer - Village of Butcher's Block(Diessa Plateau 15-25)"
krug       = u"Veteran Krug - Taminn Foothills(Queensdale 1-15)"
wupwup     = u"Wupwup Chief - Apostate Wastes(Fireheart Rise 60-70)"

# guide variables
iCost        = u"Initial Cost"
eRecovery    = u"Expected Recovery"
fCost        = u"Expected Final Cost"
sList        = u"Sell List"
bRecipes     = u"BUY RECIPES"
collectibles = u"COLLECTIBLES(Check Bank First or Buy on TP)"
warning1     = u"Do not refresh this page."
warning2     = u"It may change. Updated"
moreInfo     = u"Whenever you see this %s you can click for more information"
soldVia      = u"Sold for %s per via"
method       = [u"Vendor",
                u"Max Buyout",
                u"Minimum Sale Price"]
valuePer     = u"per"
buyVendor    = u"BUY VENDOR"
mixedTP      = u"Mixed (Buy on TP)"
make         = u"Make"
discover     = u"Discover"
expand       = u"Expand all discovery recipes"
collapse     = u"Collapse all discovery recipes"
tier         = u"Tier %i. Levels %i-%i"
buyList      = u"Buy List(Only Tier %i)"
blNotice     = u"Notice: If you are following the full guide then you already purchased these materials."
costRT       = u"Cost: %s (Rolling Total: %s)"
level        = u"Level"
finish       = u"Nothing.  You are done!"
updated      = u"Updated"
note         = u"<strong>Note:</strong> The prices show here are initial costs and do not take sellback into account."
craft        = u"Craft"
tiers        = u"Tier"
toggle       = u"Click To Toggle"
kNote        = u"Note: 11 Basil Leaf(e.g.) means buy 1 bulk Basil Leaf and you will have 14 left over"
bNote        = u"Produces 5 Ingot per make"
sNote        = u"Produces 2 Soles per make"

# FAQ strings
costs    = u"Die Kosten werden abgedeckt, aber Spenden sind willkommen"
gw2spidy = u"Auch diese Führungen wäre ohne <a möglich href=\"http://www.gw2spidy.com\"> gw2spidy </ a> und seine API."
oThread  = u"GW2 Official Forum Discussion Thread"
rThread  = u"reddit Discussion Thread"
gThread  = u"guildwars2guru Discussion Thread"
twitter  = u"Twitter"
email    = u"Email"
contact  = u"Wenn Sie irgendwelche Fragen, Kommentare, Anliegen oder das Gefühl, dass Sie bemerkt haben einen Fehler bitte kontaktieren Sie mich mit einer dieser Methoden."
faq      = u"FAQ"
question = u"Q"
answer   = u"A"
source   = u"Der Quellcode?"
q1       = u"Wie viele Stufen kann ich von Crafting bekommen?"
a11      = u"Die Menge an Erfahrung, die Sie von Charakter Crafting bekommen durch Ihre Fortschritte durch die Crafting Ebenen die folgenden Werte ermittelt;"
a12      = u"1-100 1% der aktuellen Ebene pro Handwerksstufe"
a13      = u"101-200 2% der aktuellen Ebene pro Handwerksstufe"
a14      = u"201-300 3% der aktuellen Ebene pro Handwerksstufe"
a15      = u"301-400 4% der aktuellen Ebene pro Handwerksstufe"
a16      = u"Und diese Werte lassen sich teilweise Ebenen, wie lvl 1, ist halb voll bar 1,5% eines Levels. Gehen 0-400 Ihnen 10 Stufen aus welcher Ebene auch immer Sie begann, zu jeder Zeit."
a17      = u"Es gibt 1 Ausnahme, dass XP Belohnungen 1-15 sind größer als die tatsächliche xp für diesen Ebenen benötigt. (<a href=\"http://wiki.guildwars2.com/wiki/Experience#Total_experience_gain_per_level\"> Quelle </ a>), so dass Sie über 13 Ebenen zu bekommen, während Crafting."
a18      = u"Das heißt, Sie können 2-80 vollständig nivellieren von Crafting da 8 Handwerk sind."
q2       = u"Wird nicht diese Führungen falsch sein, wenn jeder kauft aus Artikel X?"
a2       = u"Diese Führungen vorschlagen Crafting oder Kauf von Produkten über aktuelle TP Preisen. Sie werden anpassen vorgeschlagenen Elemente, da die Preise zu ändern. (Fast) alle möglichen Rezepte werden bei der Führungen erzeugt werden."
q3       = u"Verschiedene Fragen zu crit rate / Zufall oder Crafting-Booster."
a31      = u"Dieses Skript nimmt eine 0% crit rate, so crits kann die Zahl der Handwerke zu reduzieren und somit benötigten Materialien."
a32      = u"Crafting-Booster geben Ihnen einen +50% Additiv mit wvw Bonus Chance auf kritische dabei ein Handwerk. Max-Bonus von 70%. Was macht eine kritische während Crafting ist Ihnen 50% Bonus Handwerkserfahrung die Additiv mit anderen Crafting Boni (Entdeckung, Meisterwerk und seltene Handwerk). Crafting-Booster kann es so machen Sie weniger Handwerk bis 400 in einem Handwerk erreichen müssen, aber es wird nicht dazu führen Sie zu mehr als 10 Charakter-Level zu gewinnen."
q4       = u"Kann ich wiederverwenden oder Link zu Ihrer Führer?"
a4       = u"Ja, nur bewusst sein, die aktuelle Ausgabe kann sich ändern, und ich werde nicht unterstützen. Bitte liefern Sie ebenfalls angemessene Zuordnung (xanthic.9478 und einen Link zu dieser Website)."
q5       = u"Verschiedene Fragen zu erwägen TP Werte verkaufen oder Hinzufügen Anbieter Kostendeckung."
a51      = u"Balancing auf Basis verkaufen TP Werte würden Risiko für den Zielpreis hinzufügen, wie würden die Preise stagnieren und sogar aus dem Entfernen der Fähigkeit für einige Leute zu Bergungskosten so und damit ihren Lauf durch die Führung mehrerer Silber teurer. Ich habe zZ einen \"best guess\" Kostendeckung auf Maximalgebot oder Verkäufer Preis, je nachdem, was größer ist bezogen, und wenn mindestens 0 TP Verkaufspreis."
a52      = u"Es existiert auch nicht eine \"automatische\" Weg, um festzustellen, ob ein Element wird tatsächlich zu dem Preis gelistet entweder verkaufen."
q6       = u"Wie geht es Ihnen machen diese Führungen?"
a6       = u"Multi-Teil Python 2.7.3 Skript, das eine Greedy-Algorithmus verwendet und Preisdaten aus gw2spidy den niedrigsten anfänglichen gold Verfahren der Nivellierung ein Handwerk mit in Spiel Formeln berechnen"
q7       = u"Nein, ich meine, wie werden Sie diese Führungen machen? (Einfache Antwort)"
a7       = u"Für jede \"make\", erzeugen ich eine Liste der Elemente, die Berechnung der höchsten xp / niedrigsten Kosten Weg zu diesem Artikel basieren auf Crafting oder Kauf seiner Teile zu machen und dann wählen Sie das beste Produkt zu machen"
q8       = u"Nein, ich meine, wie werden Sie diese Führungen machen? (Elaborate Antwort)"
a8       = u"First Ich teile Crafting up in 16 Punkt 25 Eimer (dh 0-24, 25-49). Dann ab der 375 I berechnen (für jedes Element, das xp gibt) seine xp / base_cost, und dann für jeden sub Teil dieser Artikel berechne ich die xp / base_cost und wenn eines dieser Elemente sub Teile habe ich dann berechnen ihre xp / base_cost bis ich Produkte ohne Rezepte zu erreichen. Sub Teile sind so gewählt, gemacht werden, wenn sie billiger als der Kauf der Teil sind, oder sie erhöhen die xp / Kosten-Verhältnis mehr als der Kauf das Teil. Welches ist, warum der Guide wird Ihnen sagen kann, etwas zu basteln, auch wenn es etwas billiger ist, es zu kaufen. Dann, nachdem die beste Wahl gefunden wird, werden Änderungen xp berechnet (über alle Eimer) und dann die beste Wahl ist wieder gefunden."
thanks   = u"Vielen Dank an die Menschen, die Führer vor mir geschaffen; Qorthos, pwnuniversity, gw2wiz und guildwars-2-Crafting. Ich würde nicht auf die Idee gekommen, dies ohne Ihre Führer bietet eine Vorlage für mich aus bauen schreiben."

# index strings
fThings = u"Vier Dinge, die Sie wissen sollten"
t1      = u"<img src=\"/img/arrow.png\"> </ img> kann für alle Rezeptentdeckungen sowie für Verkaufslisten geklickt werden"
t2      = u"<input type=\"checkbox\"/> hilft den Überblick über den Fortschritt in der Liste zu bewahren"
t3      = u"Für alle Anleitungen (außer den Küchenmeister) existieren Rangspezifische Kauflisten, die über gesonderte Schaltflächen zu erreichen sind"
t4      = u"<a href=\"/de/nav.html\"> Navigation </a>, solltet ihr das Navigationsmenü nicht verwenden können"
nge     = u"Wägt das Herstellen und Einkaufen von Zutaten und Elementen eines Gegenstandes ab. Meist die kostengünstigste Methode aber stellt komplexere Anforderungen an das Inventar."
fge     = u"Macht den gleichen Gegenstand für 25 Handwerkspunkte. Schneller und einfacher als andere Anleitungen dafür kostenaufwendiger."
tge     = u"Versucht die Zutaten wenn möglich herzustellen als sie zu kaufen. In der Regel teurer als normale Anleitungen, aber weniger komplex. Vergleichbar mit Anleitungen die vor ACCG existierten."
wit     = u"<strong> Was ist das hier überhaupt? </ strong> Immer aktuelle Handwerksanleitungen für Guild Wars 2. Alle Anleitungen werden jede Stunde auf Basis der aktuellen Handelspostenpreise neu berechnet, sofern der Server läuft und gw2spidy erreichbar ist. Diese Anleitungen wurden ursprünglich für Freunde erstellt, doch die Popularität meiner Arbeit brachte mich dazu noch mehr daran zu arbeiten - Das Ergebnis seht ihr hier. Dieses Skript setzt allerdings voraus, dass es eine \"unendliche\" Menge der Artikel zu einem bestimmten Preis im Handelsposten gibt. Wurden also alle aufgekauft oder es sind weniger vorhanden als angenommen können die Preise bis zum nächten Update abweichen."
nWarn   = u"<strong> [Hinweis] </ strong> Wenn du nicht vorhast die Anleitung in einem Rutsch durchzuziehen, dann speichere Sie bitte auf deinem PC, dann Sie ist ständigen Änderungen unterworfen und wird stündlich aktualisiert."
rCost   = u"<strong> Hinweis, Kosten zu senken: </ strong> Speichere dir eine Kopie der Anleitung und platziere Kaufgeobte im Handelsposten für die Materialien."
thanks2 = u"Ich danke  bkohli, TimeBomb und saladon für einige der CSS-Styles auf diesen Seiten. Und danke an @figgityfigs für das neue Icon-Design (Favicon und apple-touch-icon) und Hosting"

# nav strings
navNotice = u"Dies ist eine einfache nav Seite, sollten Sie nur dann erreichen, wenn Sie nicht verwenden können, die Navigationsleiste. Wenn Sie diese Seite übersetzen sind bitte mailen Sie mir an gw2crafts@live.com mit der Ausgangssprache und Übersetzung Seite verwendet und ich werde versuchen, es zu beheben."
navLang   = u"Sprache"

#nav page headers and guide names
home    = u"Startseite"
nGuides = u"Normale Anleitung"
fGuides = u"Schnelle Anleitung"
tGuides = u"Traditionelle Anleitung"
cooking = u"Küchenmeister"
nHearts = u"Ohne Herzen"
tHearts = u"Top 5 Herzen"
aHearts = u"Alle Herzen"
jc      = u"Juwelier"
art     = u"Konstrukteur"
hunt    = u"Waidmann"
wc      = u"Waffenschmied"
ac      = u"Rüstungsschied"
lw      = u"Lederer"
tailor  = u"Schneider"
totals  = u"Insgesamt"
about   = u"Über"
lang    = u"Deutsch"

# directory path
path = "de/"

# don't change this
header = u"""<nav>
    <ul>
        <li><a href="http://gw2crafts.net/"""+path+u"""">"""+home+u"""</a></li>
        <li><a href="http://gw2crafts.net/"""+path+u"""nav.html">"""+nGuides+u"""</a>
        <ul>
            <li><a href="#">"""+cooking+u"""</a>
            <ul>
                <li><a href="http://gw2crafts.net/"""+path+u"""cooking.html">"""+nHearts+u"""</a></li>
                <li><a href="http://gw2crafts.net/"""+path+u"""cooking_karma_light.html">"""+tHearts+u"""</a></li>
                <li><a href="http://gw2crafts.net/"""+path+u"""cooking_karma.html">"""+aHearts+u"""</a></li>
            </ul>
            </li>
            <li><a href="http://gw2crafts.net/"""+path+u"""jewelcraft.html">"""+jc+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""artificing.html">"""+art+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""huntsman.html">"""+hunt+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""weaponcraft.html">"""+wc+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""armorcraft.html">"""+ac+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""leatherworking.html">"""+lw+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""tailor.html">"""+tailor+u"""</a></li>
        </ul>
        </li>
        <li><a href="http://gw2crafts.net/"""+path+u"""nav.html">"""+fGuides+u"""</a>
        <ul>
            <li><a href="#">"""+cooking+u"""</a>
            <ul>
                <li><a href="http://gw2crafts.net/"""+path+u"""cooking_fast.html">"""+nHearts+u"""</a></li>
                <li><a href="http://gw2crafts.net/"""+path+u"""cooking_karma_fast_light.html">"""+tHearts+u"""</a></li>
                <li><a href="http://gw2crafts.net/"""+path+u"""cooking_karma_fast.html">"""+aHearts+u"""</a></li>
            </ul>
            </li>
            <li><a href="http://gw2crafts.net/"""+path+u"""jewelcraft_fast.html">"""+jc+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""artificing_fast.html">"""+art+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""huntsman_fast.html">"""+hunt+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""weaponcraft_fast.html">"""+wc+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""armorcraft_fast.html">"""+ac+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""leatherworking_fast.html">"""+lw+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""tailor_fast.html">"""+tailor+u"""</a></li>
        </ul>
        </li>
        <li><a href="http://gw2crafts.net/"""+path+u"""nav.html">"""+tGuides+u"""</a>
        <ul>
            <li><a href="http://gw2crafts.net/"""+path+u"""jewelcraft_craft_all.html">"""+jc+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""artificing_craft_all.html">"""+art+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""huntsman_craft_all.html">"""+hunt+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""weaponcraft_craft_all.html">"""+wc+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""armorcraft_craft_all.html">"""+ac+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""leatherworking_craft_all.html">"""+lw+u"""</a></li>
            <li><a href="http://gw2crafts.net/"""+path+u"""tailor_craft_all.html">"""+tailor+u"""</a></li>
        </ul>
        </li>
        <li><a href="http://gw2crafts.net/"""+path+u"""total.html">"""+totals+u"""</a></li>
        <li><a href="http://gw2crafts.net/"""+path+u"""faq.html">"""+about+u"""</a></li>
        <li><a href="#" hreflang="en">"""+lang+u"""</a>
        <ul>
          <li><a href="http://gw2crafts.net/%s" hreflang="en">English</a></li>
          <li><a href="http://gw2crafts.net/fr/%s" hreflang="fr">Français</a></li>
          <li><a href="# hreflang="de">Deutsch</a></li>
          <li><a href="http://gw2crafts.net/es/%s" hreflang="es">Español</a></li>
        </ul>
        </li>
    </ul>
</nav>
"""
