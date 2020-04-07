# PAWS

[PAWS](https://www.mediawiki.org/wiki/PAWS): A Web Shell (PAWS) is a Jupyter notebooks deployment that has been customized to make interacting with Wikimedia wikis easier. It allows users to create and share documents that contain live code, visualizations such as graphs, rich text, etc. The user created notebooks are a powerful tool that enables data analysis and scientific research, and also transforms the way in which programmers write code - by enabling an exploratory environment with a quick feedback loop, and a low barrier for entry through it's easy to use graphical interface. 

In addition, PAWS is a customized JupyterHub on Kubernetes running inside Wikimedia Cloud Services. It provides quite a simple way to use Python and pywikibot to interact with Wikimedia Projects,via OAuth, the Wiki Replicas Cloud service, and others. 

# How to contribute
1. Just simply clone the project repo to your computer by using the command: 'git clone https://github.com/toolforge/paws.git' 
2. cd paws
3. open up the files you would want to change and edit them
4. check the status of the repo by typing  'git status' in the terminal
5. Add the files by typing 'git add README.md'
6. check the status again by running the command 'git status'
7. Then commit the changes made using the command 'git commit -m "add README file"'
8. The push it to the github repository, specifying the branch as master branch using 'git push origin master'
9. check your github repo by refreshing it, and the file will be there.
10. Then go to the main repo, click on the pull request tab, and click 'compare across forks'
11. Then create pull request.

PAWS provides some very core features on top of which people can build stuff.
Notebooks

It provides Jupyter notebooks (previously known as IPython Notebooks)
Web based Terminal
## Useful libraries
### Accessing Database Replicas With Pandas and Sqlalchemy

Pandas is a lovely high level library for in-memory data manipulations. In order to get the result of a SQL query as a pandas dataframe use:
```
from sqlalchemy import create_engine
import sys, os
import pandas as pd

constr = 'mysql+pymysql://{user}:{pwd}@{host}'.format(user=os.environ['MYSQL_USERNAME'],
                                                      pwd=os.environ['MYSQL_PASSWORD'],
                                                      host=os.environ['MYSQL_HOST'])
con = create_engine(constr)

df = pd.read_sql('select * from plwiki_p.logging limit 10', con)
```
### Storage space
Publishing space

A notebook can be turned into a public notebook by publishing a link to it. This works as the notebook is made available in a read only mode. An example might be …revisions-sql.ipynb?kernel_name=python3. It could be wise to add the kernel name to the link, even if it isn't necessary in some cases.

If you want to run the copy yourself, or do interactive changes, you must download the notebook and reupload on your own account. Downloading the raw format of the previous example can be done by adding format=raw to the previous example …revisions-sql.ipynb?format=raw. This download-reupload-process is somewhat awkward.

Note that a notebook will always be published, as the link can be guessed, so don't add any private information. 
# chat
 Contributors can get help and feedback from the community members in the public IRC channel,[IRC chat](https://webchat.freenode.net/#wikimedia-cloud),they should introduce themselves on the public project chat, and specifically state their questions. 

# Try paws yourself
Try out paws yourself in order to familiarise your self with it, all you need is to login with your wikimedia account and you're good to go. Follow the link [create a note book](https://paws.wmflabs.org/paws/hub/login) 



### To know more about paws have a look at:
https://wikitech.wikimedia.org/wiki/PAWS
