# portfolio-insights

Steps :

1) Install Node.js V6.11 along with npm, Install postgres(9.6), Install redis(3.0.51)
Link for redis : https://github.com/rgl/redis/downloads, Python(3.4.3)
2) Install Webstorm(2018.5.1) as an IDE
3) Download Git Bash(2.18) for windows
4) From Git bash console fire following commands
5) git clone https://github.com/Sumit1311/portfolio-insights.git (Follow git tutorial)
6) git checkout develop
7) In webstorm, File -> Open -> To this directory
8) Create a Run Configuration (Run -> Edit Configurations)
	- Change the node path
	- Chagne Project home directory
	- Modify Environment Variables according to requirement(sample variables available in scripts/environment_setup)
    - For executing python script properly on all platforms set PYTHON_EXEC with proper executable name and make sure that this is added in PATH
	- Create the database user and database for use
	- Change the line pg_hba.conf file according to this:
host    all             all             0.0.0.0/0            password
9) Run npm install and install psycopg2 module using pip for python 
10) Set Javascript File as app.js
	- Run npm install from this directory
11) Run the app

