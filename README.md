gw2craft
========

These are all the Python files that generate http://gw2crafts.net

Requires Python 2.7.x.  You will need to define a ftp_info.py file which contains 3 strings; ftp_url, ftp_user, and ftp_pass.


**Primary .py Files:**

Crafting -- The main file.


gen_ifn -- generates the localized FAQ, nav and index pages


localxx -- Localized language files.  Need to be updated by hand.


create_recipes -- creates all the secondary .py files you will need.  A recent snapshot of those files is included.

**Secondary .py Files:**

Armorsmith, Artificer, Chef, Chef_karma, Huntsman, Jeweler, Leatherworker, Tailor -- Contain all recipes used by Crafting.py indexed by itemid(int).

Items_xx -- Contains itemid:name pairs for outputting item names in the correct language

items -- contains item_id indexed dictionary of thumbnail url, item count, rarity, vendor value, type, and if the item is discovered.

How-To
======

Update recipes:
Run create_recipes.py and when it finished you will have updated recipes for Crafting.py

Generate guides:
First create a ftp_info.py file will the variables ftp_url, ftp_user and ftp_pass.  All 3 variables should be strings.

If you don't want to upload the guides somewhere, search for (in 2 places)

```python
	myFtp = FTP(ftp_url)
```
And delete everything until 

```python
	myFtp.close()
```

from Crafting.py.  Finally run Crafting.py, this step is much faster if you use pypy, and it will generate your guides.
