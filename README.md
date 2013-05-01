gw2craft
========

These are all the python files that generate http://gw2crafts.net

Requires Python 2.7.x and Linux (Mint 14).  You will need to define a ftp_info.py file.

Crafting.py is the main file.  Due to differences in how multiprocessing is implemented on Windows and Linux, this script is written specifically for Linux and also takes advantage of some coding elements that only work on Linux.

How-To
======

Adding a recipe:
First add the recipe to the correct craft and skill level. e.g.

  "Malign Chain Boots-Fine":{"Bronze Chain Boot Panel":1,"Bronze Chain Boot Lining":1,"Malign Jute Insignia":1}

and tier "0" of armorcrafting.  If any of the sub parts have recipes you will need to add them as well if they don't already exist.  Names need to be unique due to how Python dictionaries work.

Then add all new items to itemlist.py so we can get the price data from gw2spidy

  "Malign Chain Boots-Fine":{"item_id":"10454","type":"3"}

"type" is 3 for an item, 5 is for everything else.  Everything used by cooking and all end(usable) products are an item while generally everything else isn't.  If something is an item but it isn't discovered(ie from a recipe) add "discover":0 so the script grants the correct xp.

If an item is defined in itemlist.py but not given a recipe, it is assumed to have no recipe and will always try to buy the item if needed.
