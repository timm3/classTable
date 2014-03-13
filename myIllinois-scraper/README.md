myIllinois-scraper
==================
1. Importing the Project:

	If you try to run the scripts and they raise exception about import of modules it means that the project is not set correctly. 
	If folder icons appear instead in place of package icons in the PyDev Package Explorer view in PyDev perspective it's another sign  that the project is not set properly.
	
	To solve problems with the setup create following files for the project: .project and .pydevproject
	Follow the following link for instructions how to create a project configuration files: http://pydev.org/faq.html#PyDevFAQ-HowdoIimportexistingprojects%2FsourcesintoPyDev%3F
	
	If problems with importing modules persist add an empty file in each package named __init__.py