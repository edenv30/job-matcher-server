"# job-matcher-server" 

<h3>Setup</h3>
run the <b>Bolded commands</b> in terminal

<h5>Python Installations</h5>
<ol>
<li>Install <a href="https://www.python.org/">Python3</a></li>
<li>install <a href="https://virtualenv.pypa.io/en/stable/installation/">virtual environment</a> => <b>pip3 install virtualenv</b> OR <b>pip install virtualenv</b></li>
</ol>
<h5>Clone the repository</h5>

<h5>Create virtual environment (in the cloned repository base directory)</h5>
<ol>
<li>setup new virtual env => <b>virtualenv venv</b></li>
<li>activate the new evn => <b>venv/bin/activate</b></li>
<li>install all required dependencies (setup.py) => <b>pip install .</b></li>
</ol>

<h5>Setup Python dev server configuration to PyCharm</h5>
<ol>
<li>Click on the <b>R<u>u</u>n</b> menu => <b>Edit Configu<u>r</u>ations</b> (Alt + u + r)</li>
<li>Script Path => X:\path\to\project\server\server.py (C:\Users\Tal\PycharmProjects\server\jobmatcher\server\server.py)</li>
<li>Parameters => --mode=dev</li>
<li>Environment variables => PYTHONUNBUFFERED=1</li>
<li>Python interpreter => Python 3.x (server) [make sure it's the one that installed on the virtual environment]</li>
<li>Working directory => X:\path\to\project\server\project_name\server (C:\Users\Tal\PycharmProjects\server\jobmatcher\server)</li>
</ol>

start the server :)

<h5>Troubleshooting</h5>
- 'pip' is not recognized as an internal or external command,
operable program or batch file.
<a href="https://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command">https://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command</a>