# lean: Installation procedure
Learning analytics + Web server experimentation.
To use this code, please follow the following steps:<br>

**a.Install Python**
Install Python 2.x version.

**b.Create a Virtual Environment and clone to this page**
Use the following steps to create a virtual environment.

`sudo apt-get install python-virtualenv`

`git clone ...`

Create a new Virtual environment named "lenv"<br>
`virtualenv lenv`

Activate the Virtual Environment.

`source lenv/bin/activate`

Install flask:

`pip install flask`

Install rest of the packages defined in requirements.txt

`pip install -r requirements/dev.txt`




