# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks, Vítězslav Jaroš (translation)
Purpose: czech Localized text
Note: Requires Python 2.7.x
'''
# pypy doesn't like the é.  Should be fine after transition to .format is complete
region = "NA/EU price data only"#"pouze NA/EU cenové data"

# Copyright notice for GW2 IP
cright = u'''<footer>
    Guild Wars 2 © 2012 ArenaNet, Inc. Všechny práva vyhrazen. NCsoft, the interlocking NC logo, ArenaNet, Guild Wars, Guild Wars Factions, Guild Wars Nightfall, Guild Wars: Eye of the North, Guild Wars 2, a všechny přidružená loga a designy jsou ochranné známky nebo registrované ochranné známky společnosti NCsoft Corporation. Všechny další ochranné známky jsou majetkem příslušných vlastníků.
</footer>'''

scribetease = u"Click here for important hints"

scribeinfo = u"""Note, “Auto Turrets” in the guide are called “Gate Turrets” in game. (API error)<br />
<br />
Tip, If you are scribing a certain item but it does not complete (you do not get experience and no materials are used) the processing stack is full (250 of each item is max). To fix the issue, go to the processor and process the items you wanted to craft + wait until they are done. Then you can scribe your items. Keep in mind that you need to have the "edit assembly queue" guild permission in oder to be able to do this. Alternatively you can ask your guild leader (or someone with this permission) to do it for you. <br />
<br />
<strong>Guild unlocks</strong><br />
Most of the items the guide recommends you to scribe are guild unlocked recipes (see below for a list + alternatives). Your guild needs to have these unlocked before you can see them as recipes and scribe them. If your guild does not have them unlocked yet, you temporarily join another guild (for example “The rising falcons [RiFa]”, see below) that has the unlocks and scribe them in their hall.  <br />
<br />
<strong>Decoration crafting, required guild permissions and tips</strong><br />
The guide shows you the cheapest way to level up. Due to the recipes it is not likely decorations will be included, However if they are, OR if you want to level up through crafting decorations, you will need the following permissions form your guild leader to do so:<br />
- Use placeable (so you use decorations that the guild has for scribing)<br />
- edit assembly queue (so you can finish the decoration by adding it in the processor after which you can, depending on the decoration, also use it again for scribing at a higher level)<br />
After scribing your decorations, go to the processor (near the crafting stations in both halls) and queue the decorations you just crafted to complete them (takes 30 sec / item).<br />
<strong>Some additional decoration crafting tips:</strong><br />
1 You can buy basic decorations at the decorations vendor for 24 silver each if your guild has it unlocked. You can always buy them at the master scribe for 50 silver each (even if your guild does not have any decoration vendor unlocked).<br />
2 Some basic decorations can only be obtained from the guild trader (guild trader 4 or higher) for guild commendations.  <br />
3 some basic decorations can only be obtained from the decoration trader during certain in game events, for example snow piles from wintersday, pumpkins from Halloween, red lanterns from lunar new year, furniture coins to buy super cloud from SAB festival OR drops from bosses (basically for all the bronze, silver and gold trophies).<br />
<br />
<strong>Guild unlock List and alternatives for each scribe level range:</strong><br />
The guide will always show you the cheapest option. However, it could be that you lack that unlock in your guild but have another one that you could use instead. See this list for alternatives at each crafting level.<br />
Lv 0-25 refine<br />
Lv 25-50 WvW - Minor Supply Drop <discover/craft minor sigils as alternative><br />
Lv 50-75 Guild Banquet Schematic <decorations as alternative><br />
Lv 75-100 refine<br />
Lv 100-125 Guild Gathering Boost Banner Schematic#, Guild World Event Schematic, Sabotage Depot<br />
Lv 125-150 Guild Karma Banner Schematic*, Guild Experience Banner Schematic* <discover/craft major Sigils as alternative><br />
Lv 150-175 refine  Guild Road Marker Schematic#<br />
Lv 175-200 Guild Gold Gain Banner Schematic,  Hardened Gates, Invulnerable Dolyaks, Speedy Dolyaks<br />
Lv200-225 Guild Karma and Experience Banner Schematic *, turtle Banner, Iron guards, Guild Ballista Blueprints, Guild Arrow cart Blue prints  <br />
Lv 225-250 refine<br />
Lv 250-275 Guild Gathering and Swiftness Banner Schematic#, Packed Dolyaks, Centaur Banner<br />
Lv 275-300 no guild unlocked recipes at this level<br />
Lv 300-325 refine<br />
Lv 325-350 Invulnerable Fortifications. refine leather into book covers as alternative<br />
Lv 350-375 Vault Transport, Emergency Waypoint, Gate Turrets (in guide listed as “Auto Turrets”)<br />
 Lv375-400 Watchtower, Presence of the Keep<br />
* = these are related, you need 1 karma and 1 experience banner to craft 1 karma and Experience banner<br />
# = these are related, you need 1 Gathering boost banner and 1 Road marker to craft 1 Guild Gathering and swiftness banner.<br />
<br />
<strong>My guild lacks the unlocks/will not give me permissions to level up my scribe</strong><br />
If your guild is missing the guild unlocks (and alternatives) you can “visit” (temporarily join) a guild that has them unlocked so you can level your scribe in their hall. Just keep in mind that all the guild related itmes (banners, WvW items and decorations) that your craft in that guild hall, will stay in the guildhall that you are visiting.<br />
<br />
<strong>The Rising Falcons[RiFa] and the scribe guide History</strong><br />
Ever since <strong>Vin Lady Venture</strong> made the first static (now outdated) scribe together with <strong>Dulfy</strong> and found out that the guild unlocked scribe recipes could help leveling scribes safe a lot of gold  He opened up the guild “The rising Falcons[RiFa]” for scribes who wanted to level up and RiFa has continued to run this service ever since. While the original guide has now been replaced by the much more advanced and up to date guide that you see here, made by <strong>xanthic.9478</strong>, RiFa is still accepting scribes who do not have access to (all of) the guild unlocked recipes. It is a casual relaxed guild that offers this service to anyone who likes to level his/her scribe, free of charge. While RiFa is an EU based guild, US based players can also use the service and unlocks. The only thing is that you cannot see any of the main guild members.<br />
<br />
You can send an in game mail to  <strong>Vin lady venture (Rin of Rivvinda.4971)</strong> for an invite in RiFa, just make sure you have at least 1 free guild slot and you should be invited within 24 hours.  <br />
 """

# renown heart vendors
crandle    = u"Agent Crandle - Fort Trinity(Straits of Devastation 70-75)"
aidem      = u"Aidem Finlay - Hidden Lake(Brisban Wildlands 15-25)"
albin      = u"Albin Chronicler - The Icesteppes(Wayfarer Foothills 1-15)"
jack       = u"Apple Jack(16<span class=\"copperIcon\"></span> per) - Cornucopian Fields(Gendarran Fields 25-35)"
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
auda       = u"Lionguard Auda - Dragon's Rising(Snowden Drifts 15-25)"
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
yoal       = u"Yoal - Quetzal(Caledon Forest 1-15)"

# guide variables
iCost        = u"Základní cena"
remCost      = u"Remaining Cost"
eRecovery    = u"Očekávaná návratnost"
fCost        = u"Očekávaná koncová cena"
sList        = u"Seznam prodejů"
bRecipes     = u"NÁKUP RECEPTŮ"
collectibles = u"POTŘEBNÝ MATERIÁL(Zjistěte, jestli nemáte v bance nebo Nakupte na tržišti)"
warning1     = u"Neobnovujte tuto stránku."
warning2     = u"Může se změnit. Aktualizováno"
moreInfo     = u"Kdykoliv uvidíte tuto ikonu %s můžete si rozkliknout více informací."
soldVia      = u"Prodáváno za %s za pomocí"
method       = [u"Vendor (prodejce)",
                u"Max Buyout",
                u"Minimální prodejní cena"]
valuePer     = u"za"
buyVendor    = u"KUP U VENDORA (prodejce)"
mixedTP      = u"Předchystáno (Kup na tržišti)"
rTP          = u"Kup na tržišti"
make         = u"Vytvoř"
discover     = u"Objev"
expand       = u"Ukaž všechny recepty k objevení"
collapse     = u"Schovej všechny recepty k objevení"
tier         = u"Tier %i. Level %i-%i"
buyList      = u"Nákupní list(Pouze Tier %i)"
blNotice     = u"Poznámka: Pokud postupujete od začátku podle průvodce, pak už jste tyto materiály pořídil."
costRT       = u"Cena: %s (Kumulativní cena: %s)"
level        = u"Level"
finish       = u"Nic.  Vše hotovo!"
updated      = u"Aktualizováno"
note         = u"<strong>Poznámka:</strong> Tyto ceny jsou počáteční náklady, nejsou z nich odečteny zisky z prodeje."
craft        = u"Povolání"
tiers        = u"Tier"
toggle       = u"Ukázat / Schovat"
kNote        = u"Poznámka: 11 Basil Leaf(např.) znamená, že máte koupit 1 balení Basil Leaf a zněho Vám pak 14 ks zbyde"
bNote        = u"Vytvoří 5x Ingot najednou"
sNote        = u"Vytvoří 2x Sole najednou"

# FAQ strings
costs    = u"Náklady jsou pokryté, ale každé podpory si ceníme"
gw2spidy = u"Tyto průvodci fungují také díky <a href=\"http://www.gw2spidy.com\">gw2spidy</a> a <a href=\"http://www.guildwarstrade.com/\">guildwarstrade</a>."
oThread  = u"GW2 Oficiální Fórum - Diskuzní vlákno"
rThread  = u"reddit Diskuzní vlákno"
gThread  = u"guildwars2guru Diskuzní vlákno"
twitter  = u"Twitter"
email    = u"Email"
contact  = u"Pokud máte nějaké otázky, komentáře, připomínky nebo jste našli chybu, prosím kontaktujte mě některou z těchto metod."
faq      = u"FAQ"
question = u"Otázka"
answer   = u"Odpověď"
source   = u"Zdrojový kód?"
q1       = u"Kolik levlů můžu získat při výrobě?"
a11      = u"Celkový počet zkušeností získaných na postavě při výrobě vychází z crafting levelu podle následující tabulky;"
a12      = u"1-100 1% aktuálního levelu postavy na jeden crafting level"
a13      = u"101-200 2% aktuálního levelu postavy na jeden crafting level"
a14      = u"201-300 3% aktuálního levelu postavy na jeden crafting level"
a15      = u"301-400 4% aktuálního levelu postavy na jeden crafting level"
a16      = u"And these values scale to partial levels, like lvl 1, half full bar is 1.5% of a level. Získáním 400 bodů ve výrobě získáte teké 10 levelů na vaší postavě, je jedno na kterém levelu jste vyrábět začali."
a17      = u"Existuje 1 vyjímka u xp odměn v rozmezí 1-15 jsou větší než aktuální xp potřebné pro tyto levely. ( <a href=\"http://wiki.guildwars2.com/wiki/Experience#Total_experience_gain_per_level\">zdroj</a> ) takže získáte okolo 13 levelů za dokončení veškeré výroby."
a18      = u"This means you can level from 2-80 entirely from crafting as there are 8 crafts."
q2       = u"Budou tyto návody správné, když někdo vykoupí všechen materiál X?"
a2       = u"Tyto návody navrhují výrobu nebo nakupování materiálů na základě aktuálních cen na tržišti. Upravuje tedy navrhované předměty podle toho jak se mění jejich cena.  (Téměř) všechny možné recepty jsou porovnány před vygenerováním průvodce."
q3       = u"Otázka na critical rate/šanci nebo crafting boosters (ke zvýšení počtu získaných zkušeností)."
a31      = u"Tento script předpokládá 0% crit rate, protože criticaly redukují množství potřebných surovin k výrobě."
a32      = u"Crafting booster přidává +50%, plus wvw and guild booster bonus, zvyšuje šanci na critical. Maximální bonus je 90%. Critical přidá 50% bonus výrobních zkušeností, který se sčítá s dalšími bonusy (objevení nového předmětu, masterwork a rare crafty). Crafting booster tak snižuje počet výrobních procesů k dosažení 400, ale nemá to vliv na počet získaných levlů na postavě (vždy 10 levelů)."
q4       = u"Můžu použít nebo se odkazovat na tohoto průvodce?"
a4       = u"Ano, ale berte v úvahu, že současný výstup se může změnit a já neposkytuji podporu. Také prosím o použití správných atributů ( xanthic.9478 a odkaz na tuto stránku)."
q5       = u"Otázka zda brát ohled na ceny na tržišti nebo přidání hodnoty zisku při výkupu u prodejce."
a51      = u"Zvažování tržních cen by přidalo risk při odhadování koncových cen, protože ceny jednotlivých materiálů jsou nestabilní a nakonec by se koncová cena mohla zvednout i o několik stříbrňáků. Momentálně poskytuji \"nejlepší odhad\" návratnosti nákladů založené na maximální nabídce nebo ceně u prodejce podle toho, která je větší."
a52      = u"Taktéž neexistuje \"automatický\" způsob stanovení, že se daný předmět právě teď za tu cenu prodává."
q6       = u"Jak je tento průvodce vytvořen?"
a6       = u"Multi-part Python 2.7.3 script, který používá nenasytný algoritmus a cenné data z gw2spidy ke kalkulaci nejnižších počátečních nákladů a nejkratší cesty k získání konečného počtu zkušeností"
q7       = u"Ne, já myslel jak funguje tento průvodce? (Jednoduchá odpověď)"
a7       = u"Pro každou \"výrobu\", vygeneruji seznam materiálů, spočítám poměr nejvíc xp/nejmíň peněz, zvážím cesty výroby předmětu ze základních surovin nebo nákupu polotovarů a pak stanovým nejvýhodnější předmět k vytvoření."
q8       = u"Ne, já myslel jak funguje tento průvodce? (Elaborát)"
a8       = u"Nejdřív rozdělím výrobu na skupinky po 16 25 bodech(př. 0-24, 25-49).  Potom počínaje 375 spočítám (pro každý předmět, který dává xp) jeho poměr xp/základní cena a potom pro každou jeho součástku spočítám její poměr xp/základní cena a tak dále až se dostanu k součástce, která nemá recept na výrobu.  Součástky jsou určeny k výrobě, pokud není levnější je koupit, nebo se jejich výrobou nenavýší poměr xp/kupní cenu součástí.  A proto Vás někdy průvodce navede k výrobě ikdyž nákup je o něco levnější.  A potom co je vybrána nejlepší možnost, spočítají se změny xp (skrz všechny skupiny) a nejlepší možnost je znovu nalezena."
thanks   = u"Děkuji lidem, kteří vytvořili průvodce předemnou; Qorthos, pwnuniversity, gw2wiz a guildwars-2-crafting. Bez vaší šablony bych tohle všechno nestvořil."

# index strings
fThings = u"4 věci o kterých by jste měli vědět"
t1      = u"<img src=\"/img/arrow.png\" alt=\"ARROW\"> kliknutím na tuto ikonku si rozevřete recept, nebo nákupní seznam"
t2      = u"<input type=\"checkbox\"/> zaškrtněte si získané předměty v seznamu"
t3      = u"Tier specifický nákupní seznam se objeví u všech průvodců kromě Cooking (klikněte na tlačítko)"
t4      = u"<a href=\"nav.html\">Stromová struktura webu</a> pokud nemůžete použít horní menu"
nge     = u"Chytře vyberou mezi výrobou nebo nákupem součástí předmětu."
fge     = u"Vytvoří tolikrát stejný předmět kolikrát je potřeba pro zisk 25 bodů.  Rychlejší a jednodušší, ale dražší než normální."
tge     = u"Vytvoří součásti předmětu, pokud je to možné místo nákupu.  Obvykle dražší než normální průvodce, ale může být méně komplexní.  Toto je podobné výrobním průvodcům, kteří existovali před ACCG."
wit     = u"<strong>Co je toto za stránku?</strong> Stále aktuální výrobní průvodce pro Guild Wars 2. Všechny průvodce jsou spočítány na základě aktuálních tržních cen jednou za hodinu za předpokladu, že počítač se skriptem běží a gw2spidy je dostupné. Tento průvodce byl původně určen kamarádům, ale na základě zájmu ze strany Guild Wars 2 komunity, pokračuji ve vylepšování až do současné podoby.  Skript bere v úvahu určité \"konečné\" množství daného předmětu za danou cenu, takže když se vyprodají, nebo jich je velmi málo během aktualizace, tabulka s cenami může být chybná až do další aktualizece."
nWarn   = u"<strong>[Poznámka]</strong> Pokud nechcete projít celých výrobním procesem najednou, tak si ho prosím uložte do svého PC. Protože průvodce se neustále mění."
rCost   = u"<strong>Tip na snížení nákladů:</strong> Uložte si průvodce a dejte si nabídky na materiál na tržiště."
thanks2 = u"Děkuji za překladů Vítězslav Jaroš."

# nav strings
navNotice = u"Tohle je stránka s navigací stránek, používejte ji pouze pokud Vám nefunguje horní navigační menu.  Pokud překládáte tuto stránku prosím napište mi na email gw2crafts@live.com, přiložte název jazyka a zdrojový soubor jazykové mutace a já se o zbytek postarám."
navLang   = u"Jazyk"

#nav page headers and guide names
home    = u"Domů"
nGuides = u"Normalní průvodce"
fGuides = u"Rychlý průvodce"
tGuides = u"Tradiční průvodci"
cooking = u"Cooking"
nHearts = u"Bez srdíčka"
tHearts = u"Top 5 srdíček"
aHearts = u"Všechny srdíčka"
jc      = u"Jewelcrafting"
art     = u"Artificing"
hunt    = u"Huntsman"
wc      = u"Weaponcrafting"
ac      = u"Armorcrafting"
lw      = u"Leatherworking"
tailor  = u"Tailoring"
totals  = u"Náklady"
about   = u"O webu"
lang    = u"Čeština"
special = u"Special"
scribe  = u"Scribe"

# directory path
path = "cz/"

# don't change this
header = u"""<nav>
    <ul>
        <li><a href="/"""+path+u"""">"""+home+u"""</a></li>
        <li><a href="#">"""+nGuides+u"""</a>
        <ul>
            <li><a href="#">"""+cooking+u"""</a>
            <ul>
                <li><a href="/"""+path+u"""cooking.html">"""+nHearts+u"""</a></li>
                <li><a href="/"""+path+u"""cooking_karma_light.html">"""+tHearts+u"""</a></li>
                <li><a href="/"""+path+u"""cooking_karma.html">"""+aHearts+u"""</a></li>
            </ul>
            </li>
            <li><a href="/"""+path+u"""jewelcraft.html">"""+jc+u"""</a></li>
            <li><a href="/"""+path+u"""artificing.html">"""+art+u"""</a></li>
            <li><a href="/"""+path+u"""huntsman.html">"""+hunt+u"""</a></li>
            <li><a href="/"""+path+u"""weaponcraft.html">"""+wc+u"""</a></li>
            <li><a href="/"""+path+u"""armorcraft.html">"""+ac+u"""</a></li>
            <li><a href="/"""+path+u"""leatherworking.html">"""+lw+u"""</a></li>
            <li><a href="/"""+path+u"""tailor.html">"""+tailor+u"""</a></li>
            <li><a href="/"""+path+u"""scribe.html">"""+scribe+u"""</a></li>
        </ul>
        </li>
        <li><a href="#">"""+fGuides+u"""</a>
        <ul>
            <li><a href="#">"""+cooking+u"""</a>
            <ul>
                <li><a href="/"""+path+u"""cooking_fast.html">"""+nHearts+u"""</a></li>
                <li><a href="/"""+path+u"""cooking_karma_fast_light.html">"""+tHearts+u"""</a></li>
                <li><a href="/"""+path+u"""cooking_karma_fast.html">"""+aHearts+u"""</a></li>
            </ul>
            </li>
            <li><a href="/"""+path+u"""jewelcraft_fast.html">"""+jc+u"""</a></li>
            <li><a href="/"""+path+u"""artificing_fast.html">"""+art+u"""</a></li>
            <li><a href="/"""+path+u"""huntsman_fast.html">"""+hunt+u"""</a></li>
            <li><a href="/"""+path+u"""weaponcraft_fast.html">"""+wc+u"""</a></li>
            <li><a href="/"""+path+u"""armorcraft_fast.html">"""+ac+u"""</a></li>
            <li><a href="/"""+path+u"""leatherworking_fast.html">"""+lw+u"""</a></li>
            <li><a href="/"""+path+u"""tailor_fast.html">"""+tailor+u"""</a></li>
        </ul>
        </li>
        <li><a href="#">400-500</a>
        <ul>
            <li><a href="/"""+path+u"""artificing_400.html">"""+art+u"""</a></li>
            <li><a href="/"""+path+u"""huntsman_400.html">"""+hunt+u"""</a></li>
            <li><a href="/"""+path+u"""weaponcraft_400.html">"""+wc+u"""</a></li>
            <li><a href="/"""+path+u"""armorcraft_400.html">"""+ac+u"""</a></li>
            <li><a href="/"""+path+u"""leatherworking_400.html">"""+lw+u"""</a></li>
            <li><a href="/"""+path+u"""tailor_400.html">"""+tailor+u"""</a></li>
        </ul>
        </li>
        <li><a href="#">"""+special+u"""</a>
        <ul>
            <li><a href="#">"""+cooking+u""" 1-200</a>
            <ul>
                <li><a href="/"""+path+u"""cooking_fast_200.html">"""+nHearts+u"""</a></li>
                 <li><a href="/"""+path+u"""cooking_karma_fast_200.html">"""+aHearts+u"""</a></li>
            </ul>
            </li>
            <li><a href="#">400-450</a>
            <ul>
		    <li><a href="/"""+path+u"""artificing_450.html">"""+art+u"""</a></li>
		    <li><a href="/"""+path+u"""huntsman_450.html">"""+hunt+u"""</a></li>
		    <li><a href="/"""+path+u"""weaponcraft_450.html">"""+wc+u"""</a></li>
		    <li><a href="/"""+path+u"""armorcraft_450.html">"""+ac+u"""</a></li>
		    <li><a href="/"""+path+u"""leatherworking_450.html">"""+lw+u"""</a></li>
		    <li><a href="/"""+path+u"""tailor_450.html">"""+tailor+u"""</a></li>
            </ul>
            </li>
        </ul>
        </li>
        <li><a href="/"""+path+u"""total.html">"""+totals+u"""</a></li>
        <li><a href="/"""+path+u"""faq.html">"""+about+u"""</a></li>
        <li><a href="#" class="language" hreflang="cz">"""+lang+u"""</a>
        <ul>
          <li><a href="/%s" hreflang="en">English</a></li>
          <li><a href="/fr/%s" hreflang="fr">Français</a></li>
          <li><a href="#" hreflang="cz">Čeština</a></li>
          <li><a href="/de/%s" hreflang="de">Deutsch</a></li>
          <li><a href="/es/%s" hreflang="es">Español</a></li>
          <li><a href="/pt-br/%s" hreflang="pt-BR">Português do Brasil</a></li>
          <li><a href="/zh/%s" hreflang="zh">Chinese (Simplified)</a></li>
        </ul>
        </li>
    </ul>
</nav>
"""
