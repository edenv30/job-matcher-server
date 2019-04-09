"# job-matcher-server" 

<h3>Setup</h3>
run the <b>Bolded commands</b> in terminal

<h5>Python Installations</h5>
1) Install <a href="https://www.python.org/">Python3</a>

2) install <a href="https://virtualenv.pypa.io/en/stable/installation/">virtual environment</a> => <b>pip3 install virtualenv</b> OR <b>pip install virtualenv</b>

<h5>Clone the repository</h5>

<h5>Create virtual environment (in the cloned repository base directory)</h5>
1) setup new virtual env => <b>virtualenv venv</b>

2) activate the new evn => <b>venv/bin/activate</b>

3) install all required dependencies (setup.py) => <b>pip install .</b>

<h5>Setup Python dev server configuration to PyCharm</h5>
1) Click on the <b>R<u>u</u>n</b> menu => <b>Edit Configu<u>r</u>ations</b> (Alt + u + r)

2) Script Path => X:\path\to\project\server\server.py (C:\Users\Tal\PycharmProjects\server\jobmatcher\server\server.py)

3) Parameters => --mode=dev

4) Environment variables => PYTHONUNBUFFERED=1

5) Python interpreter => Python 3.x (server) [make sure it's the one that installed on the virtual environment] 

6) Working directory => X:\path\to\project\server\project_name\server (C:\Users\Tal\PycharmProjects\server\jobmatcher\server)

start the server :)

<h5>Troubleshooting</h5>
- 'pip' is not recognized as an internal or external command,
operable program or batch file.
<a href="https://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command">https://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command</a>
