gw2craft
========

These are all the python files that generate http://gw2crafts.net

Requires Python 2.7.x.  You will need to define a ftp_info.py file.

Crafting.py is the main file.
create_recipes.py creates all the other files you will need.  A recent snapshot of those files is also included.

How-To
======

Update recipes:
Run create_recipes.py and when it finished you will have updated recipes for Crafting.py

Generate guides:
First create a ftp_info.py file will the variables ftp_url, ftp_user and ftp_pass.  All 3 variables should be strings.

If you don't want to upload the guides somewhere, delete:

```python
	print "Starting upload"
	myFtp = FTP(ftp_url)
	myFtp.login(ftp_user,ftp_pass)
	for item in ["cooking_fast.html", "cooking_karma_fast.html", "cooking_karma_fast_light.html", "leatherworking_fast.html", "tailor_fast.html", "artificing_fast.html", "jewelcraft_fast.html", "weaponcraft_fast.html", "huntsman_fast.html", "armorcraft_fast.html", "cooking.html", "cooking_karma.html", "cooking_karma_light.html", "leatherworking.html", "tailor.html", "artificing.html", "jewelcraft.html", "weaponcraft.html", "huntsman.html", "armorcraft.html", "leatherworking_craft_all.html", "tailor_craft_all.html", "artificing_craft_all.html", "jewelcraft_craft_all.html", "weaponcraft_craft_all.html", "huntsman_craft_all.html", "armorcraft_craft_all.html", "total.html"]:
		with open(item,'rb') as f:
			myFtp.storbinary('STOR /gw2crafts.net/'+item,f)
		os.remove(item)
	myFtp.close()
```

from Crafting.py.  Finally run Crafting.py and it will generate your guides.
