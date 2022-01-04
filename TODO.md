The following are things that need to be done before final release, that are not embedded in a file.  This is not a checklist of things to do but instead things encountered during development that were put off until later.


**Verify the following recipes**

These recipes are not from master merchants or purchasable on the tp
```python
someval = {
	7288: [44662, 44714],  # Recipe: Major Sigil of Malice
	7291: [44656, 44718],  # Recipe: Major Sigil of Renewal
	7294: [44659, 44716],  # Recipe: Minor Sigil of Bursting
	7293: [44660, 44715],  # Recipe: Minor Sigil of Bursting
	7287: [44663, 44713],  # Recipe: Minor Sigil of Malice
	7290: [44657, 44717],  # Recipe: Minor Sigil of Renewal

	12096: 84618,  # Recipe Desert: Pile of Jacarandere
	12140: 83775,  # Recipe Desert: Plate of Sugar Rib Roast
	12289: 82352,  # Recipe: Bowl of "Elon Red"
	12207: 84053,  # Recipe: Bowl of Lentil Soup
	12160: 83169,  # Recipe: Bowl of Spiced Red Lentil Stew
	12271: 84562,  # Recipe: Cup of Light-Roasted Coffee
	12068: 83256,  # Recipe: Dollop of Choya Harissa
	12111: 82750,  # Recipe: Red Lentil Saobosa
	12158: 82370,  # Recipe: Spearmarshal's Boots
	12253: 83070,  # Recipe: Spearmarshal's Breastplate
	12077: 83841,  # Recipe: Spearmarshal's Cowl
	12191: 84744,  # Recipe: Spearmarshal's Gauntlets
	12254: 84607,  # Recipe: Spearmarshal's Gloves
	12072: 84231,  # Recipe: Spearmarshal's Greaves
	12292: 82900,  # Recipe: Spearmarshal's Helm
	12282: 84070,  # Recipe: Spearmarshal's Jerkin
	12238: 83124,  # Recipe: Spearmarshal's Leggings
	12200: 82601,  # Recipe: Spearmarshal's Mask
	12263: 83101,  # Recipe: Spearmarshal's Pants
	12182: 84221,  # Recipe: Spearmarshal's Shoes
	12138: 84635,  # Recipe: Spearmarshal's Shoulderpads
	12266: 82688,  # Recipe: Spearmarshal's Tasset
	12123: 84125,  # Recipe: Spearmarshal's Vambraces
	12295: 84153,  # Recipe: Spearmarshal's Vestments
	2840: 9609,  # Recipe: 10 Slot Ogre Bag
	13389: 93738,  # Recipe: Amalgamated Draconic Lodestone
	13385: 93802,  # Recipe: Amalgamated Draconic Lodestone
	11721: 72759,  # Recipe: Anthology of Villains
	3722: 9607,  # Recipe: Arctodus Amulet
	4314: 9605,  # Recipe: Ascalon Ghost Potion
	2827: 9499,  # Recipe: Ash Legion's Boot
	2828: 9501,  # Recipe: Ash Legion's Coat
	2831: 9502,  # Recipe: Ash Legion's Gloves
	2829: 9500,  # Recipe: Ash Legion's Leggings
	5344: 9410,  # Recipe: Atzintli's Spear
	13417: 94464,  # Recipe: Azure Dragon Slayer Axe
	13428: 94559,  # Recipe: Azure Dragon Slayer Dagger
	13423: 94504,  # Recipe: Azure Dragon Slayer Focus
	13434: 94599,  # Recipe: Azure Dragon Slayer Greatsword
	13420: 94555,  # Recipe: Azure Dragon Slayer Hammer
	13431: 94505,  # Recipe: Azure Dragon Slayer Longbow
	13443: 94620,  # Recipe: Azure Dragon Slayer Mace
	13448: 94541,  # Recipe: Azure Dragon Slayer Pistol
	13422: 94578,  # Recipe: Azure Dragon Slayer Rifle
	13429: 94525,  # Recipe: Azure Dragon Slayer Scepter
	13419: 94462,  # Recipe: Azure Dragon Slayer Shield
	13424: 94475,  # Recipe: Azure Dragon Slayer Short Bow
	13444: 94522,  # Recipe: Azure Dragon Slayer Staff
	13418: 94573,  # Recipe: Azure Dragon Slayer Sword
	13438: 94470,  # Recipe: Azure Dragon Slayer Torch
	13446: 94549,  # Recipe: Azure Dragon Slayer Warhorn
	9708: 66441,  # Recipe: Black Pepper Cactus Salad
	1117: 9522,  # Recipe: Bloodsaw work Boots
	1119: 9523,  # Recipe: Bloodsaw work Coat
	1120: 9527,  # Recipe: Bloodsaw work gloves
	1121: 9525,  # Recipe: Bloodsaw work helm
	1122: 9524,  # Recipe: Bloodsaw work pants
	1123: 9526,  # Recipe: Bloodsaw work shoulders
	12291: 84683,  # Recipe: Bounty Hunter's Boots
	12124: 82208,  # Recipe: Bounty Hunter's Breastplate
	12231: 83450,  # Recipe: Bounty Hunter's Cowl
	12213: 82491,  # Recipe: Bounty Hunter's Gauntlets
	12275: 83430,  # Recipe: Bounty Hunter's Gloves
	12299: 82259,  # Recipe: Bounty Hunter's Greaves
	12162: 82273,  # Recipe: Bounty Hunter's Helmet
	12268: 82584,  # Recipe: Bounty Hunter's Jerkin
	12152: 83187,  # Recipe: Bounty Hunter's Leggings
	12306: 83351,  # Recipe: Bounty Hunter's Mantle
	12167: 83803,  # Recipe: Bounty Hunter's Mask
	12106: 84247,  # Recipe: Bounty Hunter's Pants
	12262: 82421,  # Recipe: Bounty Hunter's Pauldrons
	12209: 84135,  # Recipe: Bounty Hunter's Shoes
	12120: 83433,  # Recipe: Bounty Hunter's Shoulderpads
	12217: 83371,  # Recipe: Bounty Hunter's Tassets
	12222: 84136,  # Recipe: Bounty Hunter's Vambraces
	12170: 83538,  # Recipe: Bounty Hunter's Vestments
	9993: 75909,  # Recipe: Bowl of Chocolate Tapioca Pudding
	10747: 74157,  # Recipe: Bowl of Curry Mussel Soup
	11585: 72066,  # Recipe: Bowl of Lemongrass Mussel Pasta
	11620: 71997,  # Recipe: Bowl of Mussel Soup
	11583: 70576,  # Recipe: Bowl of Passion Fruit Tapioca Pudding
	10100: 72693,  # Recipe: Bowl of Prickly Pear Tapioca Pudding
	11002: 70617,  # Recipe: Bowl of Sawgill Mushroom Risotto
	9719: 66442,  # Recipe: Cactus Fruit Salad
	9715: 66448,  # Recipe: Cactus Soup
	9712: 66439,  # Recipe: Candy Cactus Cornbread
	6494: 36126,  # Recipe: Candy Corn Tonic
	10632: 76771,  # Recipe: Canvas
	11195: 73773,  # Recipe: Capacitive Bottle
	13268: 91993,  # Recipe: Carne Khan Chili
	2972: 9563,  # Recipe: Celebratory Meat
	13381: 93843,  # Recipe: Charged Stormcaller Axe
	13372: 93721,  # Recipe: Charged Stormcaller Dagger
	13384: 93749,  # Recipe: Charged Stormcaller Focus
	13379: 93757,  # Recipe: Charged Stormcaller Greatsword
	13378: 93743,  # Recipe: Charged Stormcaller Hammer
	13387: 93728,  # Recipe: Charged Stormcaller Longbow
	13371: 93755,  # Recipe: Charged Stormcaller Mace
	13380: 93769,  # Recipe: Charged Stormcaller Pistol
	13388: 93908,  # Recipe: Charged Stormcaller Rifle
	13377: 93905,  # Recipe: Charged Stormcaller Scepter
	13383: 93902,  # Recipe: Charged Stormcaller Shield
	13386: 93789,  # Recipe: Charged Stormcaller Short Bow
	13382: 93820,  # Recipe: Charged Stormcaller Staff
	13374: 93808,  # Recipe: Charged Stormcaller Sword
	13375: 93809,  # Recipe: Charged Stormcaller Torch
	13376: 93857,  # Recipe: Charged Stormcaller Warhorn
	6073: 9610,  # Recipe: Chieftan's Mace
	5415: 9503,  # Recipe: Cleaver
	6495: 36128,  # Recipe: Concentrated Halloween Tonic
	5423: 9554,  # Recipe: Copper Mace
	5422: 9556,  # Recipe: Copper Sword
	10570: 73114,  # Recipe: Corrupted Jar
	13440: 94568,  # Recipe: Crimson Dragon Slayer Axe
	13427: 94527,  # Recipe: Crimson Dragon Slayer Dagger
	13445: 94460,  # Recipe: Crimson Dragon Slayer Focus
	13447: 94461,  # Recipe: Crimson Dragon Slayer Greatsword
	13439: 94528,  # Recipe: Crimson Dragon Slayer Hammer
	13426: 94501,  # Recipe: Crimson Dragon Slayer Longbow
	13430: 94608,  # Recipe: Crimson Dragon Slayer Mace
	13432: 94482,  # Recipe: Crimson Dragon Slayer Pistol
	13437: 94574,  # Recipe: Crimson Dragon Slayer Rifle
	13436: 94575,  # Recipe: Crimson Dragon Slayer Scepter
	13425: 94571,  # Recipe: Crimson Dragon Slayer Shield
	13441: 94582,  # Recipe: Crimson Dragon Slayer Short Bow
	13435: 94474,  # Recipe: Crimson Dragon Slayer Staff
	13421: 94611,  # Recipe: Crimson Dragon Slayer Sword
	13433: 94516,  # Recipe: Crimson Dragon Slayer Torch
	13442: 94497,  # Recipe: Crimson Dragon Slayer Warhorn
	11827: 78432,  # Recipe: Crude Leather Book
	5328: 9391,  # Recipe: Crusader's Shield
	10793: 75449,  # Recipe: Crystal Jar
	3872: 9561,  # Recipe: Crystal Scroll
	3163: 9613,  # Recipe: Degun Stew
	3469: 9548,  # Recipe: Deldrimor Ring Replica
	10989: 71546,  # Recipe: Destroyer Jar
	2970: 9560,  # Recipe: Dolyak Stew
	11878: 79935,  # Recipe: Dragon Hatchling Doll Eyes
	11888: 79924,  # Recipe: Dragon Hatchling Doll Frame
	11889: 79931,  # Recipe: Dragon Hatchling Doll Hide
	13396: 94205,  # Recipe: Dragon Slayer Axe
	13401: 94314,  # Recipe: Dragon Slayer Dagger
	13403: 94236,  # Recipe: Dragon Slayer Focus
	13397: 94181,  # Recipe: Dragon Slayer Greatsword
	13410: 94267,  # Recipe: Dragon Slayer Hammer
	13402: 94356,  # Recipe: Dragon Slayer Longbow
	13408: 94350,  # Recipe: Dragon Slayer Mace
	13407: 94168,  # Recipe: Dragon Slayer Pistol
	13409: 94167,  # Recipe: Dragon Slayer Rifle
	13404: 94263,  # Recipe: Dragon Slayer Scepter
	13395: 94230,  # Recipe: Dragon Slayer Shield
	13406: 94299,  # Recipe: Dragon Slayer Short Bow
	13399: 94182,  # Recipe: Dragon Slayer Staff
	13405: 94302,  # Recipe: Dragon Slayer Sword
	13411: 94212,  # Recipe: Dragon Slayer Torch
	13398: 94349,  # Recipe: Dragon Slayer Warhorn
	7234: 43551,  # Recipe: Dragon's Revelry Starcake
	2843: 9493,  # Recipe: Drottot's Poached Eggs
	2968: 9550,  # Recipe: Eggs Beetletun
	3828: 9912,  # Recipe: Embellished Brilliant Beryl Jewel
	3829: 9908,  # Recipe: Embellished Brilliant Chrysocola Jewel
	3830: 9913,  # Recipe: Embellished Brilliant Coral Jewel
	3831: 9914,  # Recipe: Embellished Brilliant Emerald Jewel
	3832: 9910,  # Recipe: Embellished Brilliant Opal Jewel
	3833: 9911,  # Recipe: Embellished Brilliant Ruby Jewel
	3834: 9909,  # Recipe: Embellished Brilliant Sapphire Jewel
	3814: 9899,  # Recipe: Embellished Gilded Amethyst Jewel
	3815: 9898,  # Recipe: Embellished Gilded Carnelian Jewel
	3816: 9900,  # Recipe: Embellished Gilded Lapis Jewel
	3817: 9896,  # Recipe: Embellished Gilded Peridot Jewel
	3820: 9895,  # Recipe: Embellished Gilded Spinel Jewel
	3818: 9897,  # Recipe: Embellished Gilded Sunstone Jewel
	3819: 9894,  # Recipe: Embellished Gilded Topaz Jewel
	3807: 9892,  # Recipe: Embellished Intricate Amethyst Jewel
	3808: 9891,  # Recipe: Embellished Intricate Carnelian Jewel
	3809: 9893,  # Recipe: Embellished Intricate Lapis Jewel
	3810: 9889,  # Recipe: Embellished Intricate Peridot Jewel
	3813: 9888,  # Recipe: Embellished Intricate Spinel Jewel
	3811: 9890,  # Recipe: Embellished Intricate Sunstone Jewel
	3812: 9887,  # Recipe: Embellished Intricate Topaz Jewel
	3821: 9905,  # Recipe: Embellished Ornate Beryl Jewel
	3822: 9901,  # Recipe: Embellished Ornate Chrysocola Jewel
	3823: 9906,  # Recipe: Embellished Ornate Coral Jewel
	3824: 9907,  # Recipe: Embellished Ornate Emerald Jewel
	3825: 9903,  # Recipe: Embellished Ornate Opal Jewel
	3826: 9904,  # Recipe: Embellished Ornate Ruby Jewel
	3827: 9902,  # Recipe: Embellished Ornate Sapphire Jewel
	3393: 9408,  # Recipe: Enchanted Rock Pendant
	12950: 89124,  # Recipe: Enhanced Lucent Oil
	2965: 9535,  # Recipe: Ettin Stew
	10298: 76309,  # Recipe: Evergreen Jar
	2830: 9394,  # Recipe: Excavator's Gloves
	4459: 9400,  # Recipe: Experimental Skritt Musket
	3840: 9392,  # Recipe: Experimenter's Collection Staff
	13264: 92038,  # Recipe: Firebreather Chili
	3868: 9532,  # Recipe: Flame Legion Focus
	3867: 9531,  # Recipe: Flame Legion Scepter
	3866: 9530,  # Recipe: Flame Legion Staff
	13498: 95278,  # Recipe: Fried Banana Chips
	12065: 81699,  # Recipe: Fried Oyster Sandwich
	3159: 9388,  # Recipe: Front Line Stew
	11736: 75645,  # Recipe: Gift of Blood
	11739: 73366,  # Recipe: Gift of Bones
	11744: 75071,  # Recipe: Gift of Claws
	11741: 70646,  # Recipe: Gift of Dust
	4315: 9618,  # Recipe: Gift of Energy
	11737: 74882,  # Recipe: Gift of Fangs
	6074: 9615,  # Recipe: Gift of Metal
	11743: 76121,  # Recipe: Gift of Scales
	11742: 75337,  # Recipe: Gift of Totems
	11735: 73389,  # Recipe: Gift of Venom
	5114: 9617,  # Recipe: Gift of Wood
	11061: 71122,  # Recipe: Glacial Imbued Jar
	6479: 36123,  # Recipe: Glazed Peach Tart
	6478: 36122,  # Recipe: Glazed Pear Tart
	11887: 79820,  # Recipe: Gossamer Stuffing
	3869: 9549,  # Recipe: Grawl Snowman Potion
	5417: 9505,  # Recipe: Greatsword
	13269: 91894,  # Recipe: Green Chile Ice Cream
	2981: 9603,  # Recipe: Griffon Egg Omelet
	5418: 9507,  # Recipe: Hammer
	11808: 78136,  # Recipe: Hunter's Kit
	9802: 67224,  # Recipe: Hylek Maintenance Oil
	4218: 9601,  # Recipe: Irradiated Focus
	5068: 9599,  # Recipe: Irradiated Pistol
	6058: 9597,  # Recipe: Irradiated Sword
	11856: 79582,  # Recipe: Island Pudding
	11404: 73557,  # Recipe: Jerk Poultry Flatbread Sandwich
	10596: 71174,  # Recipe: Jerk Poultry and Nopal Flatbread Sandwich
	2964: 9515,  # Recipe: Kastaz Strongpaw Stuffed Poultry
	9801: 67215,  # Recipe: Krait Tuning Crystal
	11928: 80232,  # Recipe: Lake Doric Mussels
	10442: 79996,  # Recipe: Legendary Inscription
	4497: 9510,  # Recipe: Longbow
	12450: 85432,  # Recipe: Lunatic Acolyte Boots
	12436: 85386,  # Recipe: Lunatic Acolyte Coat
	12449: 85515,  # Recipe: Lunatic Acolyte Gloves
	12441: 85439,  # Recipe: Lunatic Acolyte Mantle
	12448: 85520,  # Recipe: Lunatic Acolyte Mask
	12435: 85474,  # Recipe: Lunatic Acolyte Pants
	12444: 85443,  # Recipe: Lunatic Gossamer Insignia
	12454: 85513,  # Recipe: Lunatic Noble Boots
	12442: 85412,  # Recipe: Lunatic Noble Coat
	12433: 85389,  # Recipe: Lunatic Noble Gloves
	12437: 85390,  # Recipe: Lunatic Noble Mask
	12453: 85487,  # Recipe: Lunatic Noble Pants
	12440: 85382,  # Recipe: Lunatic Noble Shoulders
	12434: 85489,  # Recipe: Lunatic Templar Breastplate
	12455: 85427,  # Recipe: Lunatic Templar Gauntlets
	12457: 85410,  # Recipe: Lunatic Templar Greaves
	12445: 85500,  # Recipe: Lunatic Templar Helm
	12447: 85395,  # Recipe: Lunatic Templar Pauldrons
	12443: 85486,  # Recipe: Lunatic Templar Tassets
	10320: 73734,  # Recipe: Lye
	5419: 9508,  # Recipe: Mace
	7285: 44647,  # Recipe: Major Rune of Exuberance
	7297: 44654,  # Recipe: Major Rune of Perplexity
	7300: 44651,  # Recipe: Major Rune of Tormenting
	4503: 9553,  # Recipe: Match Grade Standard Rifle
	5416: 9506,  # Recipe: Meat Carver
	7286: 44648,  # Recipe: Minor Rune of Exuberance
	7296: 44653,  # Recipe: Minor Rune of Perplexity
	7299: 44650,  # Recipe: Minor Rune of Tormenting
	3161: 9604,  # Recipe: Minotaur Steak
	10088: 76095,  # Recipe: Minstrel's Intricate Gossamer Insignia
	9921: 74839,  # Recipe: Minstrel's Orichalcum Imbued Inscription
	5421: 9533,  # Recipe: Moogooloo Harpoon
	4502: 9552,  # Recipe: Moogooloo Speargun
	3870: 9551,  # Recipe: Moogooloo Trident
	12303: 84454,  # Recipe: Mordant Bonespitter
	12130: 83944,  # Recipe: Mordant Brazier
	12141: 82659,  # Recipe: Mordant Cesta
	12193: 83848,  # Recipe: Mordant Crosier
	12075: 83731,  # Recipe: Mordant Crusher
	12197: 82129,  # Recipe: Mordant Edge
	12269: 82100,  # Recipe: Mordant Infantry Bow
	12243: 84288,  # Recipe: Mordant Inscription
	12082: 84021,  # Recipe: Mordant Key
	12180: 82663,  # Recipe: Mordant Longbow
	12246: 84309,  # Recipe: Mordant Revolver
	12104: 82668,  # Recipe: Mordant Scutum
	12132: 82183,  # Recipe: Mordant Sickle
	12129: 83842,  # Recipe: Mordant Slayer
	12258: 82961,  # Recipe: Mordant Slicer
	12100: 83696,  # Recipe: Mordant Trumpet
	12155: 82730,  # Recipe: Mordant Warclub
	6496: 36127,  # Recipe: Mummy Tonic
	2844: 9399,  # Recipe: Mushroom Soup
	12959: 91479,  # Recipe: Mystic Aspect
	12833: 91571,  # Recipe: Mystic Mote
	9663: 66455,  # Recipe: Nomad's Intricate Gossamer Insignia
	9662: 66456,  # Recipe: Nomad's Orichalcum Imbued Inscription
	9717: 66443,  # Recipe: Nopalitos Sauté
	9803: 67223,  # Recipe: Ogre Sharpening Stone
	10474: 75730,  # Recipe: Ooze Terrarium
	2966: 9544,  # Recipe: Outrider Stew
	3470: 9547,  # Recipe: Owl Amulet
	3555: 9565,  # Recipe: Owl Amulet
	12062: 81749,  # Recipe: Oysters with Cocktail Sauce
	12059: 81989,  # Recipe: Oysters with Pesto Sauce
	12058: 81618,  # Recipe: Oysters with Spicy Sauce
	12052: 81636,  # Recipe: Oysters with Zesty Sauce
	10648: 76248,  # Recipe: Pile of Jerk Spices
	6493: 36125,  # Recipe: Plastic Spider Tonic
	11093: 75604,  # Recipe: Plate of Jerk Poultry
	9792: 66906,  # Recipe: Plate of Meaty Plant Food
	11359: 77053,  # Recipe: Plate of Mussels Gnashblade
	12050: 82053,  # Recipe: Plate of Oysters Gnashblade
	9790: 66907,  # Recipe: Plate of Piquant Plant Food
	12883: 89236,  # Recipe: Potent Lucent Oil
	4316: 9620,  # Recipe: Potion of Azantil
	13239: 91303,  # Recipe: Powerful Potion of Branded Slaying
	13236: 91277,  # Recipe: Powerful Potion of Mordrem Slaying
	13238: 91341,  # Recipe: Powerful Potion of Slaying Scarlet's Armies
	9718: 66446,  # Recipe: Prickly Pear Pie
	9720: 66440,  # Recipe: Prickly Pear Sorbet
	1116: 9386,  # Recipe: Quiet Leather Leggings
	3029: 9606,  # Recipe: Raspberry Pie
	9716: 66444,  # Recipe: Roasted Cactus
	12857: 89149,  # Recipe: Rune of Balthazar
	12958: 89153,  # Recipe: Rune of Divinity
	12948: 89109,  # Recipe: Rune of Dwayna
	13131: 90000,  # Recipe: Rune of Fireworks
	12930: 89129,  # Recipe: Rune of Grenth
	12971: 89269,  # Recipe: Rune of Hoelbrak
	12995: 89143,  # Recipe: Rune of Infiltration
	12919: 89155,  # Recipe: Rune of Lyssa
	12868: 89192,  # Recipe: Rune of Melandru
	12929: 89222,  # Recipe: Rune of Mercy
	12986: 89221,  # Recipe: Rune of Rage
	12918: 89154,  # Recipe: Rune of Rata Sum
	12866: 89146,  # Recipe: Rune of Scavenging
	12957: 89178,  # Recipe: Rune of Snowfall
	12939: 89233,  # Recipe: Rune of Strength
	12992: 89102,  # Recipe: Rune of the Afflicted
	12889: 89193,  # Recipe: Rune of the Centaur
	12981: 89163,  # Recipe: Rune of the Citadel
	12870: 89107,  # Recipe: Rune of the Dolyak
	12936: 89272,  # Recipe: Rune of the Eagle
	12962: 89232,  # Recipe: Rune of the Flame Legion
	12940: 89128,  # Recipe: Rune of the Flock
	12874: 89261,  # Recipe: Rune of the Grove
	12951: 89180,  # Recipe: Rune of the Lich
	12846: 89194,  # Recipe: Rune of the Traveler
	11906: 80532,  # Recipe: Saffron Mussels
	7880: 49509,  # Recipe: Settler's Intricate Gossamer Insignia
	7342: 45597,  # Recipe: Settler's Orichalcum Imbued Inscription
	2833: 9537,  # Recipe: Shadow Garb
	2834: 9538,  # Recipe: Shadow Gloves
	2836: 9541,  # Recipe: Shadow Helm
	2835: 9539,  # Recipe: Shadow Leggings
	2837: 9540,  # Recipe: Shadow Mantle
	2832: 9536,  # Recipe: Shadow Shoes
	4498: 9511,  # Recipe: Short Bow
	12944: 89246,  # Recipe: Sigil of Agony
	12867: 89112,  # Recipe: Sigil of Air
	13000: 89215,  # Recipe: Sigil of Battle
	12858: 89123,  # Recipe: Sigil of Bloodlust
	12842: 89229,  # Recipe: Sigil of Centaur Slaying
	12974: 89150,  # Recipe: Sigil of Chilling
	12830: 89255,  # Recipe: Sigil of Corruption
	12852: 89116,  # Recipe: Sigil of Debility
	12990: 89251,  # Recipe: Sigil of Demon Slaying
	12966: 89254,  # Recipe: Sigil of Demons
	13004: 89248,  # Recipe: Sigil of Earth
	12954: 89249,  # Recipe: Sigil of Energy
	13001: 89185,  # Recipe: Sigil of Fire
	12844: 89100,  # Recipe: Sigil of Force
	12849: 89122,  # Recipe: Sigil of Geomancy
	12967: 89196,  # Recipe: Sigil of Grawl Slaying
	12931: 89135,  # Recipe: Sigil of Hobbling
	12989: 89262,  # Recipe: Sigil of Hydromancy
	12923: 89191,  # Recipe: Sigil of Ice
	12895: 89111,  # Recipe: Sigil of Intelligence
	12943: 89226,  # Recipe: Sigil of Leeching
	12881: 89173,  # Recipe: Sigil of Life
	12901: 89137,  # Recipe: Sigil of Mischief
	12865: 89259,  # Recipe: Sigil of Nullification
	12859: 89165,  # Recipe: Sigil of Ogre Slaying
	12836: 89205,  # Recipe: Sigil of Perception
	12937: 89270,  # Recipe: Sigil of Purity
	12920: 89147,  # Recipe: Sigil of Rage
	12882: 89130,  # Recipe: Sigil of Restoration
	12985: 89213,  # Recipe: Sigil of Serpent Slaying
	12924: 89139,  # Recipe: Sigil of Smoldering
	12838: 89187,  # Recipe: Sigil of Stamina
	12991: 89250,  # Recipe: Sigil of Venom
	12885: 89197,  # Recipe: Sigil of Water
	9813: 67534,  # Recipe: Sinister Intricate Gossamer Insignia
	9811: 67527,  # Recipe: Sinister Orichalcum Imbued Inscription
	3871: 9562,  # Recipe: Skale Poking Stick
	4504: 9557,  # Recipe: Skale Repeater
	9949: 72929,  # Recipe: Slice of Allspice Cake
	11251: 73981,  # Recipe: Slice of Allspice Cake with Ice Cream
	11807: 78680,  # Recipe: Small Flute
	4477: 9415,  # Recipe: Soundless Warhorn
	5420: 9509,  # Recipe: Spear
	4501: 9514,  # Recipe: Speargun
	12225: 83154,  # Recipe: Spearmarshal's Mantle
	12233: 82274,  # Recipe: Spearmarshal's Pauldrons
	6482: 36124,  # Recipe: Spicy Pumpkin Cookie
	2967: 9543,  # Recipe: Sticky Bread
	13330: 93451,  # Recipe: Stormcaller Axe
	13351: 93520,  # Recipe: Stormcaller Dagger
	13362: 93497,  # Recipe: Stormcaller Focus
	13347: 93642,  # Recipe: Stormcaller Greatsword
	13340: 93433,  # Recipe: Stormcaller Hammer
	13346: 93358,  # Recipe: Stormcaller Longbow
	13345: 93362,  # Recipe: Stormcaller Mace
	13329: 93563,  # Recipe: Stormcaller Pistol
	13350: 93626,  # Recipe: Stormcaller Rifle
	13335: 93611,  # Recipe: Stormcaller Scepter
	13354: 93379,  # Recipe: Stormcaller Shield
	13337: 93657,  # Recipe: Stormcaller Short Bow
	13339: 93646,  # Recipe: Stormcaller Staff
	13341: 93608,  # Recipe: Stormcaller Sword
	13360: 93557,  # Recipe: Stormcaller Torch
	13344: 93377,  # Recipe: Stormcaller Warhorn
	9709: 66447,  # Recipe: Stuffed Nopales
	12242: 82453,  # Recipe: Sunspear Carver
	12245: 83184,  # Recipe: Sunspear Cutlass
	12136: 83416,  # Recipe: Sunspear Firelight
	12139: 83970,  # Recipe: Sunspear Greatblade
	12189: 82255,  # Recipe: Sunspear Horn
	12066: 83856,  # Recipe: Sunspear Matchlock
	12287: 84275,  # Recipe: Sunspear Pocketbow
	12088: 82265,  # Recipe: Sunspear Recurve
	12239: 82978,  # Recipe: Sunspear Rod
	12110: 83748,  # Recipe: Sunspear Runestone
	12143: 82737,  # Recipe: Sunspear Sidearm
	12188: 83531,  # Recipe: Sunspear Smasher
	12298: 83814,  # Recipe: Sunspear Standard
	12101: 84698,  # Recipe: Sunspear Thrasher
	12175: 83078,  # Recipe: Sunspear Wallshield
	12195: 84729,  # Recipe: Sunspear Warsickle
	7284: 44649,  # Recipe: Superior Rune of Exuberance
	7298: 44655,  # Recipe: Superior Rune of Perplexity
	7301: 44652,  # Recipe: Superior Rune of Tormenting
	11293: 76615,  # Recipe: Superior Rune of the Berserker
	10546: 71317,  # Recipe: Superior Rune of the Chronomancer
	10927: 71059,  # Recipe: Superior Rune of the Daredevil
	12283: 82725,  # Recipe: Superior Rune of the Deadeye
	10136: 75726,  # Recipe: Superior Rune of the Dragonhunter
	11521: 72611,  # Recipe: Superior Rune of the Druid
	12215: 82709,  # Recipe: Superior Rune of the Firebrand
	11101: 75631,  # Recipe: Superior Rune of the Herald
	12248: 84751,  # Recipe: Superior Rune of the Holosmith
	12093: 82625,  # Recipe: Superior Rune of the Mirage
	11634: 74112,  # Recipe: Superior Rune of the Reaper
	12201: 83361,  # Recipe: Superior Rune of the Renegade
	12148: 82713,  # Recipe: Superior Rune of the Scourge
	10748: 76790,  # Recipe: Superior Rune of the Scrapper
	12080: 82760,  # Recipe: Superior Rune of the Soulbeast
	12119: 82694,  # Recipe: Superior Rune of the Spellbreaker
	11275: 74806,  # Recipe: Superior Rune of the Tempest
	12202: 84572,  # Recipe: Superior Rune of the Weaver
	7295: 44661,  # Recipe: Superior Sigil of Bursting
	7289: 44664,  # Recipe: Superior Sigil of Malice
	7292: 44658,  # Recipe: Superior Sigil of Renewal
	11868: 79533,  # Recipe: Sweet Curried Mussels
	9710: 66445,  # Recipe: Sweet and Spicy Beans
	5113: 9611,  # Recipe: Sweptweave Rifle
	5414: 9504,  # Recipe: Sword
	3162: 9614,  # Recipe: Tasty Wurm Stew
	13331: 93408,  # Recipe: Tengu Axe
	13332: 93437,  # Recipe: Tengu Blade
	13343: 93405,  # Recipe: Tengu Dagger
	13336: 93483,  # Recipe: Tengu Focus
	13334: 93532,  # Recipe: Tengu Greatsword
	13352: 93431,  # Recipe: Tengu Hammer
	13353: 93595,  # Recipe: Tengu Longbow
	13342: 93356,  # Recipe: Tengu Mace
	13349: 93537,  # Recipe: Tengu Pistol
	13355: 93551,  # Recipe: Tengu Rifle
	13348: 93436,  # Recipe: Tengu Scepter
	13358: 93535,  # Recipe: Tengu Shield
	13357: 93404,  # Recipe: Tengu Short Bow
	13356: 93652,  # Recipe: Tengu Staff
	13338: 93387,  # Recipe: Tengu Sword
	13361: 93354,  # Recipe: Tengu Torch
	13359: 93403,  # Recipe: Tengu Warhorn
	4499: 9512,  # Recipe: Torch
	2841: 9383,  # Recipe: Trail Mix
	10990: 71454,  # Recipe: Trailblazer's Intricate Gossamer Insignia
	10948: 70510,  # Recipe: Trailblazer's Orichalcum Imbued Inscription
	11426: 76327,  # Recipe: Trickster's Cream Pie
	3865: 9529,  # Recipe: Trident
	3354: 9816,  # Recipe: Triktiki Omelet
	13504: 95503,  # Recipe: Turrón Slice
	11004: 74439,  # Recipe: Vigilant Intricate Gossamer Insignia
	11496: 74235,  # Recipe: Vigilant Orichalcum Imbued Inscription
	11110: 73230,  # Recipe: Vile Jar
	10511: 74019,  # Recipe: Viper's Intricate Gossamer Insignia
	11498: 77137,  # Recipe: Viper's Orichalcum Imbued Inscription
	2852: 9412,  # Recipe: Warden Rations
	4500: 9513,  # Recipe: Warhorn
	253: 9521,  # Recipe: Water Filter
	1125: 9564,  # Recipe: Wrangler's Bag
}
```