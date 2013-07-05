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
Purpose: fr Localized text
Note: Requires Python 2.7.x
'''


# Copyright notice for GW2 IP
cright = u'''<footer>
    Guild Wars 2 © 2012 ArenaNet, Inc. Tous droits réservés. NCsoft, le logo NC, ArenaNet, Guild Wars, Guild Wars Factions, Guild Wars Nightfall, Guild Wars: Eye of the North, Guild Wars 2 et tous les logos et dessins associés sont des marques commerciales ou déposées de NCsoft Corporation. Toutes les autres marques sont la propriété de leurs propriétaires respectifs.
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
costs    = u"Les coûts sont couverts, mais les dons sont appréciés"
gw2spidy = u"Aussi ces guides ne serait pas possible sans <a href=\"http://www.gw2spidy.com\">gw2spidy</a> et son API."
oThread  = u"GW2 Official Forum Discussion Thread"
rThread  = u"reddit Discussion Thread"
gThread  = u"guildwars2guru Discussion Thread"
twitter  = u"Twitter"
email    = u"Email"
contact  = u"Si vous avez des questions, des commentaires, des préoccupations ou sentez que vous avez remarqué un bug merci de me contacter en utilisant l'une de ces méthodes."
faq      = u"FAQ"
question = u"Q"
answer   = u"A"
source   = u"Le code source?"
q1       = u"Combien de niveaux puis-je obtenir de l'artisanat?"
a11      = u"La quantité d'expérience de personnage que vous obtenez de l'artisanat est déterminé par votre progression à travers les niveaux artisanat basé sur les valeurs suivantes;"
a12      = u"1-100 1% du niveau actuel par niveau d'artisanat"
a13      = u"101-200 2% du niveau actuel par niveau d'artisanat"
a14      = u"201-300 3% du niveau actuel par niveau d'artisanat"
a15      = u"301-400 4% du niveau actuel par niveau d'artisanat"
a16      = u"Et ces valeurs d'échelle de niveaux partielles, comme lvl 1, la moitié de la barre pleine est de 1,5% d'un niveau. Aller 0-400 va vous donner 10 niveaux de n'importe quel niveau vous avez commencé à, à chaque fois."
a17      = u"Il ya 1 exception, les récompenses xp 1-15 sont plus grandes que le xp effectif nécessaire pour ces niveaux. (<a href=\"http://wiki.guildwars2.com/wiki/Experience#Total_experience_gain_per_level\"> sources < a>) et vous obtiendrez environ 13 niveaux tout en artisanat."
a18      = u"Cela signifie que vous pouvez le niveau 2-80 entièrement de l'artisanat comme il ya 8 artisanat."
q2       = u"Est-ce que ces guides pas se tromper une fois tout le monde achète des ouvrages X?"
a2       = u"Ces guides proposent artisanat ou l'achat d'articles basés sur les prix de TP. Ils permettent de régler des suggestions que les prix changent. (Presque) toutes les recettes possibles sont pris en compte lors guides sont générés."
q3       = u"Divers questions sur le taux de critique / hasard ou boosters d'artisanat."
a31      = u"Ce script suppose un taux de critique de 0%, si crits peuvent réduire le nombre de métiers et donc les matériaux nécessaires."
a32      = u"Boosters d'artisanat vous donnent un +50%, additif avec prime wvw, chance de critique tout en faisant un métier. Max prime de 70%. Quelle critique ne tout en artisanat est de vous donner 50% de bonus d'expérience d'artisanat qui est additif avec d'autres bonus d'artisanat (découverte, chef-d'œuvre et de l'artisanat rares). Boosters d'artisanat peuvent faire en sorte que vous avez besoin de moins artisanat pour atteindre 400 dans un métier, mais il ne sera pas vous faire gagner plus de 10 niveaux de personnage."
q4       = u"Puis-je réutiliser ou un lien vers vos guides?"
a4       = u"Oui, mais il faut savoir le courant de sortie peut changer et je ne fournira pas de support. Aussi s'il vous plaît fournir une attribution correcte (xanthic.9478 et un lien vers ce site)."
q5       = u"Diverses questions concernant l'examen TP vendre des valeurs ou l'ajout de recouvrement des coûts des fournisseurs."
a51      = u"sur la base TP vendre valeurs ajouteraient risque pour le prix d'objectif, les prix seraient égaliser et stagner enlevant la possibilité pour certaines personnes de frais de recouvrement de cette façon et ce qui rend leur course à travers le guide plusieurs argent plus cher. Je fournis actuellement une «meilleure estimation» du recouvrement des coûts sur la base enchère maximale ou les prix des fournisseurs, selon le plus élevé, et si 0 minimum TP prix de vente."
a52      = u"Il n'existe également pas de façon \"automatique\" pour déterminer si un élément sera effectivement vendre au prix indiqué non plus.."
q6       = u"Comment allez-vous faire de ces guides?"
a6       = u"Multi-partie Python 2.7.3 script qui utilise un algorithme glouton et données sur les prix de gw2spidy pour calculer la méthode d'or initiale plus faible de niveler un métier à l'aide de formules de jeu"
q7       = u"Non, je veux dire, comment faites-vous de ces guides? (La réponse est simple)"
a7       = u"Pour chaque \"fais\", je génère une liste d'éléments, calculer le chemin le plus élevé xp / coût le plus bas pour rendre cet élément basé sur l'artisanat ou l'achat de ses parties et ensuite choisir le meilleur élément à prendre."
q8       = u"Non, je veux dire, comment faites-vous de ces guides? (Réponse Elaborer)"
a8       = u"J'ai d'abord diviser l'artisanat en 16 25 seaux de points (ie 0-24, 25-49). Ensuite, à partir de la 375 I calcul (pour chaque élément qui donne xp) sa xp / base_cost, puis pour chaque sous-partie de cet article je calcule son xp / base_cost et si l'un de ces éléments ont des sous parties puis-je calculer leur xp / base_cost jusqu'à ce que j'atteigne articles sans recettes. Sous partie sont choisis pour être prise si elles sont moins cher que l'achat de la partie, ou qu'ils augmentent le xp / coût plus que l'achat de la partie. C'est pourquoi le guide peut vous dire de fabriquer quelque chose, même si elle est légèrement moins cher à acheter. Puis, après le meilleur choix est trouvée, les changements XP sont calculées (dans tous les seaux) et alors le meilleur choix est retrouvé."
thanks   = u"Merci aux personnes qui ont créé des guides avant moi; Qorthos, pwnuniversity, gw2wiz et Guildwars-2-crafting. Je n'aurais pas eu l'idée d'écrire ce sans vos guides fournissant un modèle pour moi de construire à partir."

# index strings
fThings = u"4 choses que vous devez savoir"
t1      = u"<img src=\"/img/arrow.png\"></img> peut être cliqué pour toutes les recettes de découverte ainsi que la liste des objets vendus"
t2      = u"<input type=\"checkbox\"/> existe afin que vous puissiez suivre votre position dans la liste buy"
t3      = u"listes d'achat spécifiques de niveau existent pour les guides non-cuisson (cliquez sur le bouton) "
t4      = u"<a href=\"nav.html\">la page Nav</a> si vous ne pouvez pas utiliser la barre de navigation"
nge     = u"va faire des choix judicieux entre l'artisanat ou l'achat de sous-parties d'un article. Presque toujours la méthode la moins coûteuse mais plus complexe avec les exigences de l'inventaire."
fge     = u"fait le même point pour 25 points. Plus rapide et plus facile que d'autres guides, mais plus cher."
tge     = u"sera l'artisan des sous parties d'un article si possible au lieu d'acheter. Généralement plus cher que les guides normales, mais peut être moins complexe. Ceci est similaire à l'artisanat guides qui existaient avant ACCG."
wit     = u"<strong> C'est quoi? </strong> Toujours guides d'artisanat actuelles pour Guild Wars 2. Tous les guides sont recalculés sur la base des prix actuels de TP chaque heure en supposant que l'ordinateur exécutant le script est en marche et gw2spidy est accessible. Ces guides ont été créés à l'origine pour des amis, mais basés sur la popularité de ces derniers dans la communauté de Guild Wars 2, j'ai continué à les améliorer à ce que vous voyez aujourd'hui. Ce script ne suppose qu'il ya «infinie» d'un point à un coût donné, donc si ils ont tous se rachetés, ou il ya très peu disponibles dans les prix de la fenêtre de mise à jour peut être mal jusqu'à la prochaine mise à jour."
nWarn   = u"<strong> [Avis] </strong> Si vous n'allez pas faire le guide dans une séance assurez-vous de l'enregistrer sur votre machine. Comme ces guides peut et va changer."
rCost   = u"<strong> Conseils pour réduire les coûts: </strong> Enregistrer une copie du guide et de placer des ordres d'achat pour les matériaux."
thanks2 = u"Merci à bkohli, TimeBomb et saladon pour certains du style CSS sur ces pages. Et merci à @ figgityfigs pour la nouvelle icône du design (favicon et apple-touch-icon) et l'hébergement"

# nav strings
navNotice = u"C'est une page de nav simple, vous ne devriez l'atteindre si vous ne pouvez pas utiliser la barre de navigation. Si vous traduisez ce site s'il vous plaît écrivez-moi à gw2crafts@live.com avec la langue source et la page de traduction utilisés et je vais essayer d'y remédier."
navLang   = u"Langue"

#nav page headers and guide names
home    = u"Maison"
nGuides = u"Guides Normales"
fGuides = u"Guides Rapides"
tGuides = u"Guides Traditionnels"
cooking = u"Cuisiner"
nHearts = u"Pas De Coeurs"
tHearts = u"Top 5 Des Coeurs"
aHearts = u"Tous Les Coeurs"
jc      = u"Joaillerie"
art     = u"Artificing"
hunt    = u"Huntsman"
wc      = u"Weaponcrafting"
ac      = u"Armurerie"
lw      = u"Travail du cuir"
tailor  = u"Couture"
totals  = u"Totales"
about   = u"Sur"
lang    = u"Français"

# directory path
path = "fr/"

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
          <li><a href="#" hreflang="fr">Français</a></li>
          <li><a href="http://gw2crafts.net/de/%s" hreflang="de">Deutsch</a></li>
          <li><a href="http://gw2crafts.net/es/%s" hreflang="es">Español</a></li>
        </ul>
        </li>
    </ul>
</nav>
"""
