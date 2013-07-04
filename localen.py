# -*- coding: utf-8 -*-
# en Localized text
header = u"""<nav>
    <ul>
        <li><a href="http://gw2crafts.net/">Home</a></li>
        <li><a href="http://gw2crafts.net/nav.html">Normal Guides</a>
        <ul>
            <li><a href="#">Cooking</a>
            <ul>
                <li><a href="http://gw2crafts.net/cooking.html">No Hearts</a></li>
                <li><a href="http://gw2crafts.net/cooking_karma_light.html">Top 5 Hearts</a></li>
                <li><a href="http://gw2crafts.net/cooking_karma.html">All Hearts</a></li>
            </ul>
            </li>
            <li><a href="http://gw2crafts.net/jewelcraft.html">Jewelcrafting</a></li>
            <li><a href="http://gw2crafts.net/artificing.html">Artificing</a></li>
            <li><a href="http://gw2crafts.net/huntsman.html">Huntsman</a></li>
            <li><a href="http://gw2crafts.net/weaponcraft.html">Weaponcrafting</a></li>
            <li><a href="http://gw2crafts.net/armorcraft.html">Armorcrafting</a></li>
            <li><a href="http://gw2crafts.net/leatherworking.html">Leatherworking</a></li>
            <li><a href="http://gw2crafts.net/tailor.html">Tailoring</a></li>
        </ul>
        </li>
        <li><a href="http://gw2crafts.net/nav.html">Fast Guides</a>
        <ul>
            <li><a href="#">Cooking</a>
            <ul>
                <li><a href="http://gw2crafts.net/cooking_fast.html">No Hearts</a></li>
                <li><a href="http://gw2crafts.net/cooking_karma_fast_light.html">Top 5 Hearts</a></li>
                <li><a href="http://gw2crafts.net/cooking_karma_fast.html">All Hearts</a></li>
            </ul>
            </li>
            <li><a href="http://gw2crafts.net/jewelcraft_fast.html">Jewelcrafting</a></li>
            <li><a href="http://gw2crafts.net/artificing_fast.html">Artificing</a></li>
            <li><a href="http://gw2crafts.net/huntsman_fast.html">Huntsman</a></li>
            <li><a href="http://gw2crafts.net/weaponcraft_fast.html">Weaponcrafting</a></li>
            <li><a href="http://gw2crafts.net/armorcraft_fast.html">Armorcrafting</a></li>
            <li><a href="http://gw2crafts.net/leatherworking_fast.html">Leatherworking</a></li>
            <li><a href="http://gw2crafts.net/tailor_fast.html">Tailoring</a></li>
        </ul>
        </li>
        <li><a href="http://gw2crafts.net/nav.html">Traditional Guides</a>
        <ul>
            <li><a href="http://gw2crafts.net/jewelcraft_craft_all.html">Jewelcrafting</a></li>
            <li><a href="http://gw2crafts.net/artificing_craft_all.html">Artificing</a></li>
            <li><a href="http://gw2crafts.net/huntsman_craft_all.html">Huntsman</a></li>
            <li><a href="http://gw2crafts.net/weaponcraft_craft_all.html">Weaponcrafting</a></li>
            <li><a href="http://gw2crafts.net/armorcraft_craft_all.html">Armorcrafting</a></li>
            <li><a href="http://gw2crafts.net/leatherworking_craft_all.html">Leatherworking</a></li>
            <li><a href="http://gw2crafts.net/tailor_craft_all.html">Tailoring</a></li>
        </ul>
        </li>
        <li><a href="http://gw2crafts.net/total.html">Totals</a></li>
        <li><a href="http://gw2crafts.net/faq.html">About</a></li>
        <li><a href="#" hreflang="en">English</a>
        <ul>
          <li><a href="#" hreflang="en">English</a></li>
          <li><a href="http://gw2crafts.net/fr/%s" hreflang="fr">French</a></li>
          <li><a href="http://gw2crafts.net/de/%s" hreflang="de">German</a></li>
          <li><a href="http://gw2crafts.net/es/%s" hreflang="es">Spanish</a></li>
        </ul>
        </li>
    </ul>
</nav>
"""

# Copyright notice for GW2 IP
cright = u'''<footer>
    Guild Wars 2 © 2012 ArenaNet, Inc. All rights reserved. NCsoft, the interlocking NC logo, ArenaNet, Guild Wars, Guild Wars Factions, Guild Wars Nightfall, Guild Wars: Eye of the North, Guild Wars 2, and all associated logos and designs are trademarks or registered trademarks of NCsoft Corporation. All other trademarks are the property of their respective owners.
</footer>'''

karma_items  = {12337:{'note':"Lieutenant Pickins - Greystone Rise(Harathi Hinterlands 35-45) <br /> Disa - Snowslide Ravine(Dredgehaunt Cliffs 40-50)",'cost':77}, # Almond
                12165:{'note':"Farmer Eda - Shaemoor Fields(Queensdale 1-15) <br /> Apple Jack(16c per) - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Apple
                12340:{'note':"Fallen Angel Makayla - Stronghold of Ebonhawke(Fields of Ruin 30-40)",'cost':77}, # Avocado
                12251:{'note':"Deputy Jenks - Giant's Passage (Kessex Hills 15-25) <br /> Sangdo Swiftwing - Cereboth Canyon(Kessex Hills 15-25) <br /> Seraph Soldier Goran - The Wendon Steps(Brisban Wildlands 15-25) <br /> Security Captain Vejj - Almuten Estates(Gendarran Fields 25-35)",'cost':49}, # Banana
                12237:{'note':"Deputy Jenks - Overlake Haven(Kessex Hills 15-25) <br /> Field Medic Leius - Nebo Terrace(Gendarran Fields 25-35)",'cost':49}, # Black Bean
                12240:{'note':"Bjarni - Hangrammr Climb(Wayfayer Foothills 1-15) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Celery Stalk
                12338:{'note':"Lieutenant Summers - Nightguard Beach(Harathi Hinterlands 35-45) <br /> Disa - Snowslide Ravine(Dredgehaunt Cliffs 35-45)",'cost':77}, # Cherry
                12515:{'note':"Naknar - Ebbing Heart Run(Iron Marches 50-60)",'cost':112}, # Chickpea
                12350:{'note':"Lionscout Tunnira - Archen Foreland(Bloodtide Coast 45-55)",'cost':112}, # Coconut
                12256:{'note':"Sagum Relicseeker - Agnos Gorge(Plains of Ashford 1-15) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Cumin
                12502:{'note':"Environmental Activist Jenrys - Judgement Rock(Mount Maelstrom 60-70)",'cost':154}, # Eggplant
                12232:{'note':"Albin Chronicler - The Icesteppes(Wayfarer Foothills 1-15)",'cost':35}, # Green Bean
                12518:{'note':"Laudren - Thundertroll Swamp(Sparkfly Fen 55-65) <br /> Wupwup Chief - Apostate Wastes(Fireheart Rise 60-70)",'cost':112}, # Horseradish Root
                12239:{'note':"Seraph Archer Brian - Ossencrest Climb(Snowden Drifts 15-25) <br /> Kastaz Strongpaw - Noxin Dells(Diessa Plateau 15-25) <br /> Hune - The Thunderhorns(Lornar's Pass 25-40)",'cost':49}, # Kidney Bean
                12252:{'note':"Eona - Mabon Market(Caledon Forest 1-15) <br /> Researcher Hrappa - Voloxian Passage(Metrica Province 1-15) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Lemon
                12339:{'note':"Shelp - Degun Shun(Blazeridge Steppes 40-50)",'cost':77}, # Lime
                12543:{'note':"Agent Crandle - Fort Trinity(Straits of Devastation 70-75)",'cost':203}, # Mango
                12249:{'note':"Farmer Eda - Shaemoor Fields(Queensdale 1-15) <br /> Deputy Jenks - Overlake Haven(Kessex Hills 15-25) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Nutmeg Seed
                12503:{'note':"Nrocroc Chief - Apostate Wastes(Fireheart Rise 60-70)",'cost':154}, # Peach
                12514:{'note':"Braxa Scalehunter - Champion's Shield(Iron Marches 50-60)",'cost':112}, # Pear
                12516:{'note':"Scholar Tholin - Krongar Pass(Timberline Falls 50-60)",'cost':112}, # Pinenut
                12517:{'note':"Ichtaca - Hunting Banks(Timberline Falls 50-60)",'cost':112}} # Shallot

karma_chef   = {12159:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Cheese Wedge
                12137:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Glass of Buttermilk
                12152:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Packet of Yeast
                12145:{'note':"Master Chef or vendor near cooking area",'cost':49}, # Rice Ball
                12325:{'note':"Master Chef or vendor near cooking area",'cost':77}, # Bowl of Sour Cream
                12141:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Tomato
                12328:{'note':"Master Chef or vendor near cooking area",'cost':77}, # Ginger Root
                12245:{'note':"Master Chef or vendor near cooking area",'cost':49}, # Basil Leaf
                12235:{'note':"Master Chef or vendor near cooking area",'cost':49}} # Bell Pepper

karma_recipe = {12131:{'note':"Elain - Grenbrack Delves(Caledon Forest 1-15)",'cost':35}, # Bowl of Watery Mushroom Soup
                12185:{'note':"Bjarni - Breakneck Pass(Wayfarer Foothills 1-15)",'cost':35}, # Handful of Bjarni's Rabbit Food
                12140:{'note':"PR&T Senior Investigator Hrouda - Akk Wilds(Metrica Province 1-15)",'cost':35}, # Bowl of Gelatinous Ooze Custard
                 8587:{'note':"Drottot Lashtail - Devourer's Mouth(Plains of Ashford 1-15)",'cost':35}, # Poached Egg
                12211:{'note':"Lodge Keeper Kevach - Dolyak Pass(Wayfarer Foothills 1-15)",'cost':35}, # Bowl of Cold Wurm Stew
                12198:{'note':"Vaastas Meatslayer - Village of Butcher's Block(Diessa Plateau 15-25)",'cost':35}, # Celebratory Steak
                12133:{'note':"Laewyn - Wychmire Swamp(Caledon Forest 1-15)",'cost':35}, # Warden Ration
                12149:{'note':"Veteran Krug - Taminn Foothills(Queensdale 1-15)",'cost':35}, # Bowl of Ettin Stew
                12203:{'note':"Maxtar Rapidstep - Dolyak Pass(Wayfarer Foothills 1-15)",'cost':35}, # Bowl of Dolyak Stew
                12139:{'note':"Aidem Finlay - Hidden Lake(Brisban Wildlands 15-25)",'cost':35}, # Bowl of Front Line Stew
                12150:{'note':"Farmer Eda - Shaemoor Fields(Queensdale 1-15)",'cost':35}, # Eda's Apple Pie
                12343:{'note':"Kastaz Strongpaw - Noxin Dells(Diessa Plateau 15-25)",'cost':35}, # Kastaz Roasted Poultry
                12160:{'note':"Lionguard Auda - Dragon's Rising(Silverpeak Mountains 15-25)",'cost':35}, # Loaf of Walnut Sticky Bread
                12154:{'note':"Seraph Archer Brian - Ossencrest Climb(Snowden Drifts 15-25)",'cost':35}, # Bowl of Outrider Stew
                12292:{'note':"Glubb - Degun Shun(Blazeridge Steppes 40-50)",'cost':35}, # Bowl of Degun Shun Stew
                12233:{'note':"Scholar Tholin - Krongar Pass(Timberline Falls 50-60)",'cost':35}, # Handful of Trail Mix
                12739:{'note':"Sentry Triktiki - Arcallion Digs(Harathi Hinterlands 35-45)",'cost':35}, # Triktiki Omelet
                12352:{'note':"Pochtecatl - Jelako Cliffrise(Bloodtide Coast 45-55)",'cost':35}, # Griffon Egg Omelet
                12264:{'note':"Nrocroc Chief - Apostate Wastes(Fireheart Rise 60-70)",'cost':35}, # Raspberry Pie
                12192:{'note':"Assistant Chef Victor - Scaver Plateau(Queensdale 1-15)",'cost':35}, # Beetletun Omelette
                19955:{'note':"Master Craftsman or Vendor",'cost':350}, # Ravaging Intricate Wool Insignia
                19956:{'note':"Master Craftsman or Vendor",'cost':350}, # Rejuvenating Intricate Wool Insignia
                19957:{'note':"Master Craftsman or Vendor",'cost':350}, # Honed Intricate Wool Insignia
                19958:{'note':"Master Craftsman or Vendor",'cost':350}, # Pillaging Intricate Wool Insignia
                19959:{'note':"Master Craftsman or Vendor",'cost':350}, # Strong Intricate Wool Insignia
                19960:{'note':"Master Craftsman or Vendor",'cost':350}, # Vigorous Intricate Wool Insignia
                19961:{'note':"Master Craftsman or Vendor",'cost':350}, # Hearty Intricate Wool Insignia
                19962:{'note':"Master Craftsman or Vendor",'cost':455}, # Ravaging Intricate Cotton Insignia
                19963:{'note':"Master Craftsman or Vendor",'cost':455}, # Rejuvenating Intricate Cotton Insignia
                19964:{'note':"Master Craftsman or Vendor",'cost':455}, # Honed Intricate Cotton Insignia
                19965:{'note':"Master Craftsman or Vendor",'cost':455}, # Pillaging Intricate Cotton Insignia
                19966:{'note':"Master Craftsman or Vendor",'cost':455}, # Strong Intricate Cotton Insignia
                19967:{'note':"Master Craftsman or Vendor",'cost':455}, # Vigorous Intricate Cotton Insignia
                19968:{'note':"Master Craftsman or Vendor",'cost':455}, # Hearty Intricate Cotton Insignia
                19969:{'note':"Master Craftsman or Vendor",'cost':567}, # Carrion Intricate Linen Insignia
                19970:{'note':"Master Craftsman or Vendor",'cost':567}, # Cleric's Intricate Linen Insignia
                19971:{'note':"Master Craftsman or Vendor",'cost':567}, # Explorer's Intricate Linen Insignia
                19972:{'note':"Master Craftsman or Vendor",'cost':567}, # Berserker's Intricate Linen Insignia
                19973:{'note':"Master Craftsman or Vendor",'cost':567}, # Valkyrie Intricate Linen Insignia
                19974:{'note':"Master Craftsman or Vendor",'cost':567}, # Rampager's Intricate Linen Insignia
                19975:{'note':"Master Craftsman or Vendor",'cost':567}, # Knight's Intricate Linen Insignia
                19880:{'note':"Master Craftsman or Vendor",'cost':672}, # Carrion Intricate Silk Insignia
                19881:{'note':"Master Craftsman or Vendor",'cost':672}, # Cleric's Intricate Silk Insignia
                19882:{'note':"Master Craftsman or Vendor",'cost':672}, # Explorer's Intricate Silk Insignia
                19883:{'note':"Master Craftsman or Vendor",'cost':672}, # Berserker's Intricate Silk Insignia
                19886:{'note':"Master Craftsman or Vendor",'cost':672}, # Valkyrie Intricate Silk Insignia
                19884:{'note':"Master Craftsman or Vendor",'cost':672}, # Rampager's Intricate Silk Insignia
                19885:{'note':"Master Craftsman or Vendor",'cost':672}, # Knight's Intricate Silk Insignia
                19934:{'note':"Master Craftsman or Vendor",'cost':350}, # Ravaging Iron Imbued Inscription
                19935:{'note':"Master Craftsman or Vendor",'cost':350}, # Rejuvenating Iron Imbued Inscription
                19936:{'note':"Master Craftsman or Vendor",'cost':350}, # Honed Iron Imbued Inscription
                19937:{'note':"Master Craftsman or Vendor",'cost':350}, # Pillaging Iron Imbued Inscription
                19938:{'note':"Master Craftsman or Vendor",'cost':350}, # Strong Iron Imbued Inscription
                19939:{'note':"Master Craftsman or Vendor",'cost':350}, # Vigorous Iron Imbued Inscription
                19940:{'note':"Master Craftsman or Vendor",'cost':350}, # Hearty Iron Imbued Inscription
                19941:{'note':"Master Craftsman or Vendor",'cost':455}, # Ravaging Steel Imbued Inscription
                19942:{'note':"Master Craftsman or Vendor",'cost':455}, # Rejuvenating Steel Imbued Inscription
                19943:{'note':"Master Craftsman or Vendor",'cost':455}, # Honed Steel Imbued Inscription
                19944:{'note':"Master Craftsman or Vendor",'cost':455}, # Pillaging Steel Imbued Inscription
                19945:{'note':"Master Craftsman or Vendor",'cost':455}, # Strong Steel Imbued Inscription
                19946:{'note':"Master Craftsman or Vendor",'cost':455}, # Vigorous Steel Imbued Inscription
                19947:{'note':"Master Craftsman or Vendor",'cost':455}, # Hearty Steel Imbued Inscription
                19948:{'note':"Master Craftsman or Vendor",'cost':567}, # Carrion Darksteel Imbued Inscription
                19949:{'note':"Master Craftsman or Vendor",'cost':567}, # Cleric's Darksteel Imbued Inscription
                19950:{'note':"Master Craftsman or Vendor",'cost':567}, # Explorer's Darksteel Imbued Inscription
                19951:{'note':"Master Craftsman or Vendor",'cost':567}, # Berserker's Darksteel Imbued Inscription
                19952:{'note':"Master Craftsman or Vendor",'cost':567}, # Valkyrie Darksteel Imbued Inscription
                19953:{'note':"Master Craftsman or Vendor",'cost':567}, # Rampager's Darksteel Imbued Inscription
                19954:{'note':"Master Craftsman or Vendor",'cost':567}, # Knight's Darksteel Imbued Inscription
                19897:{'note':"Master Craftsman or Vendor",'cost':672}, # Carrion Mithril Imbued Inscription
                19898:{'note':"Master Craftsman or Vendor",'cost':672}, # Cleric's Mithril Imbued Inscription
                19899:{'note':"Master Craftsman or Vendor",'cost':672}, # Explorer's Mithril Imbued Inscription
                19900:{'note':"Master Craftsman or Vendor",'cost':672}, # Berserker's Mithril Imbued Inscription
                19903:{'note':"Master Craftsman or Vendor",'cost':672}, # Valkyrie Mithril Imbued Inscription
                19901:{'note':"Master Craftsman or Vendor",'cost':672}, # Rampager's Mithril Imbued Inscription
                19902:{'note':"Master Craftsman or Vendor",'cost':672}, # Knight's Mithril Imbued Inscription
                24904:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Topaz Jewel
                24902:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Spinel Jewel
                24901:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Peridot Jewel
                24903:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Sunstone Jewel
                24899:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Carnelian Jewel
                24898:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Amethyst Jewel
                24900:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Lapis Jewel
                24911:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Topaz Jewel
                24905:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Amethyst Jewel
                24906:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Carnelian Jewel
                24907:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Lapis Jewel
                24908:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Peridot Jewel
                24909:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Spinel Jewel
                24910:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Sunstone Jewel
                24912:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Beryl Jewel
                24913:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Chrysocola Jewel
                24914:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Coral Jewel
                24915:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Emerald Jewel
                24916:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Opal Jewel
                24917:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Ruby Jewel
                24918:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Sapphire Jewel
                24919:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Beryl Jewel
                24920:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Chrysocola Jewel
                24921:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Coral Jewel
                24922:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Emerald Jewel
                24923:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Opal Jewel
                24924:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Ruby Jewel
                24925:{'note':"Master Craftsman or Vendor",'cost':231}} # Embellished Brilliant Sapphire Jewel

iCost = u"Initial Cost"
eRecovery = u"Expected Recovery"
fCost = u"Expected Final Cost"
sList = u"Sell List"
bRecipes = u"BUY RECIPES"
collectibles = u"COLLECTIBLES(Check Bank First or Buy on TP)"

warning1 = u"Do not refresh this page."
warning2 = u"It may change. Updated:"
moreInfo = u"Whenever you see this %s you can click for more information"
soldVia = u"Sold for %s per via"
vendor = u"Vendor"
maxBuy = u"Max Buyout"
minSell = u"Minimum Sale Price"
valuePer = u"per"
buyVendor = u"BUY VENDOR"
mixedTP = u"Mixed (Buy on TP)"
make = u"Make"
discover = u"Discover"
expand = u"Expand all discovery recipes"
collapse = u"Collapse all discovery recipes"
tier = u"Tier %i. Levels %i-%i:"
buyList = u"Buy List(Only Tier %i)"
blNotice = u"Notice: If you are following the full guide then you already purchased these materials."
costRT = u"Cost: %s (Rolling Total: %s)"
level = u"Level"
finish = u"Nothing.  You are done!"
