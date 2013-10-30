gw2craft
========

Note: This readme needs to be updated, including using pypy instead of python to generate the guides and providing more information.  I am currently in the process of porting the code to python3

These are all the python files that generate http://gw2crafts.net

Requires Python 2.7.x.  You will need to define a ftp_info.py file.

Crafting.py is the main file.
gen_ifn.py generates the localized FAQ, nav and index pages
localxx.py are the localized language files
create_recipes.py creates all the other files you will need.  A recent snapshot of those files is also included.

How-To
======

Update recipes:
Run create_recipes.py and when it finished you will have updated recipes for Crafting.py

Generate guides:
First create a ftp_info.py file will the variables ftp_url, ftp_user and ftp_pass.  All 3 variables should be strings.

If you don't want to upload the guides somewhere, search for

```python
	myFtp = FTP(ftp_url)
```
And delete everything until 

```python
	myFtp.close()
```

from Crafting.py.  Finally run Crafting.py and it will generate your guides.
