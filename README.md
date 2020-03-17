# paws

[PAWS](https://www.mediawiki.org/wiki/PAWS) is a customized JupyterHub on Kubernetes running inside Wikimedia Cloud Services. It provides a simple way to use Python and pywikibot interact with the Wikimedia Projects, including the various wikis via OAuth, the Wiki Replicas Cloud service, and others.
This project is to add the ability for a PAWS notebook user to run their own notebooks and related PAWS features on a schedule. This will likely use Kubernetes CronJob objects as the back-end technology, but must be done in a secure way.
PAWS involves configurations of nginx (with some lua in it), docker images, interacting with Kubernetes via helm charts, python scripts and Jupyterhub itself. This project may involve work with some or all of these.

 A Web Shell (PAWS) is a Jupyter notebooks deployment that has been customized to make interacting with Wikimedia wikis easier. It allows users to create and share documents that contain live code, visualizations such as graphs, rich text, etc. The user created notebooks are a powerful tool that enables data analysis and scientific research, and also transforms the way in which programmers write code - by enabling an exploratory environment with a quick feedback loop, and a low barrier for entry through it's easy to use graphical interface.
 # Chat
 Applicants can get help and feedback from both mentors and community members. Community members discuss their contributions in a public chat.
Please introduce yourself on the public project chat, follow the link  [IRC chat](https://webchat.freenode.net/#wikimedia-cloud)

# Try paws yourself
Try out paws yourself inorder to familiarise your self with it, all you need is to login with your wikimedia account and you're good to go. Follow the link [create a note book](https://paws.wmflabs.org/paws/hub/login) 

# Create a pull request
Navigate to PAWS github repository, [Paws repo](https://github.com/toolforge/paws) and follow the following steps to make your contribution

Fork the repository
Clone thee repository to your machine
Make changes(make your contribution) and commit those changes to your github repository
Push your changes to github
Make a pull requsst to submit your changes for review
