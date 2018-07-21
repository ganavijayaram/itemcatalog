# Linux Server Configuration Project

## About

This tutorial will guide you through the steps to take a baseline installation of a Linux server and prepare it to host your Web applications.

### Technical Information About the Project

- **Server IP Address:** 206.189.46.108
- **SSH server access port:** 2200
- **SSH login username:** grader
- **Application URL:** http://206.189.46.108.xip.io

## Steps to Set up the Server

### 1. Creating the RSA Key Pair

On your local machine, you will first have to set up the public and private key pair. 
To generate a key pair, run the following command:

   ```console
   $ ssh-keygen
   ```

When it asks to enter a passphrase, you may either leave it empty or enter some passphrase.

You now have a public and private key that you can use to authenticate. The public key is called `udacity_project.pub` and the corresponding private key is called `udacity_project`. The key pair is stored inside the `~/.ssh/` directory.

### 2. Setting Up a DigitalOcean Droplet

1. Log in or create an account on [DigtalOcean](https://cloud.digitalocean.com/login).

2. Go to the Dashboard, and click **Create Droplet**.

3. Choose **Ubuntu 18.04 x64** image from the list of given images.

4. Choose a preferred size. In this project, I have chosen the **1GB/1 vCPU/25GB** configuration.

5. In the section **Add Your SSH Keys**, paste the content of your public key, `udacity_project.pub`:


   This step will automatically create the file `~/.ssh/authorized_keys` with appropriate permissions and add your public key to it. It would also add the following rule in the `/etc/ssh/sshd_config` file automatically:

   ```
   PasswordAuthentication no
   ```

 6. Click **Create** to create the droplet. This will take some time to complete. After the droplet has been created successfully, a public IP address will be assigned. In this project, the public IPv4 address that I have been assigned is `206.189.46.108`.

### 3. Logging In as `root` via SSH and Updating the System

#### 3.1. Logging in as `root` via SSH

As the droplet has been successfully created, you can now log into the server as `root` user by running the following command in your host machine:

```
  $ ssh root@206.189.46.108
```

#### 3.2. Updating the System

Run the following command to update the virtual server:

```
 # apt update && apt upgrade
```

```
# reboot
```

### 4. Changing the SSH Port from 22 to 2200

1. Open the `/etc/ssh/sshd_config` file with `nano` or any other text editor of your choice:

   ```
   # nano /etc/ssh/sshd_config
   ```

2. Find the line `#Port 22` (would be located around line 13) and change it to `Port 2200`, and save the file.

3. Restart the SSH server to reflect those changes:
   ```
   # service ssh restart
   ```

4. To confirm whether the changes have come into effect or not, run:
   ```
   # exit
   ```

   This will take you back to your host machine. After you are back to your local machine, run:

   ```
   $ ssh root@206.189.46.108 -p 2200
   ```

### 5. Configure Timezone to Use UTC

To configure the timezone to use UTC, run the following command:

```
# sudo dpkg-reconfigure tzdata
```

It then shows you a list. Choose ``None of the Above`` and press enter. In the next step, choose ``UTC`` and press enter.

### 6. Setting Up the Firewall

Now we would configure the firewall to allow only incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123):

```
# ufw allow 2200/tcp
# ufw allow 80/tcp
# ufw allow 123/udp
```

To enable the above firewall rules, run:

```
# ufw enable
```

To confirm whether the above rules have been successfully applied or not, run:

```
# ufw status
```

You should see something like this:

```
Status: active

To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123/udp                    ALLOW       Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123/udp (v6)               ALLOW       Anywhere (v6)
```

### 7. Creating the User `grader` and Adding it to the `sudo` Group

#### 7.1. Creating the User `grader`

While being logged into the virtual server, run the following command and proceed:

```
  # adduser grader
```


**Note**: Above, the UNIX password I have entered for the user `grader` is, `root`. 

#### 7.2. Adding `grader` to the Group `sudo`

Run the following command to add the user `grader` to the `sudo` group to grant it administrative access:

```
  # usermod -aG sudo grader
```

### 8. Adding SSH Access to the user `grader`

To allow SSH access to the user `grader`, first log into the account of the user `grader` from your virtual server:

```
# su - grader
```


Now enter the following commands to allow SSH access to the user `grader`:

```
$ mkdir .ssh
$ chmod 700 .ssh
$ cd .ssh/
$ touch authorized_keys
$ chmod 644 authorized_keys
```

After you have run all the above commands, go back to your local machine and copy the content of the public key file `~/.ssh/udacity_project.pub`. Paste the public key to the server's `authorized_keys` file using `nano` or any other text editor, and save.

After that, run `exit`. You would now be back to your local machine. To confirm that it worked, run the following command in your local machine:

```console
ssh grader@206.189.46.108-p 2200
```

You should now be able to log in as `grader` and would get a prompt to enter commands.

Next, run `exit` to go back to the host machine and proceed to the following step to disable `root` login.

### 9. Disabling Root Login

1. Run the following command on your local machine to log in as `root` in the server:
   ```
   $ ssh root@206.189.46.108-p 2200
   ```

2. After you are logged in, open the file `/etc/ssh/sshd_config` with `nano`:
   ```
   # nano /etc/ssh/sshd_config
   ```

3. Find the line `PermitRootLogin yes` and change it to `PermitRootLogin no`.

4. Restart the SSH server:
   ```
   # service ssh restart
   ```

5. Terminate the connection:
   ```
   # exit
   ```

### 10. Installing Apache Web Server

To install the Apache Web Server, run the following command after logging in as the `grader` user via SSH:

```
$ sudo apt update
$ sudo apt install apache2
```

To confirm whether it successfully installed or not, enter the URL `http://206.189.46.108` in your Web browser:

If the installation has succeeded, you should see the following Webpage:

![Screenshot](https://res.cloudinary.com/sdey96/image/upload/v1527170572/Capture_seeiof.png)

### 11. Installing `pip3`

The package `pip3` will be required to install certain packages. To install it, run:

```
$ sudo apt install python3-pip
```

To confirm whether or not it has been successfully installed, run:
   
```
$ pip3 --version
```

You should see something like this if it has been successfully installed:
   
```
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```

### 12. Installing and Configuring Git

#### 12.1. Installing Git

In Ubuntu 18.04, `git` might already be pre-installed. If it isn't, run the following commands:

```
$ sudo add-apt-repository ppa:git-core/ppa
$ sudo apt update
$ sudo apt install git
```

#### 12.2. Configuring Git

To continue using `git`, you will have to configure a username and an email:

```
$ git config --global user.name "name"

$ git config --global user.email "emai"
```

### 13. Installing and Configuring PostgreSQL

#### 13.1. Installing PostgreSQL

1. Create the file `/etc/apt/sources.list.d/pgdg.list`:

   ```
   $ nano /etc/apt/sources.list.d/pgdg.list
   ```

   And, add the following line to it:
   ```
   deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main
   ```

2. Import the repository signing key, and update the package lists:

   ```
   $ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
   $ sudo apt update
   ```

3. Install PostgreSQL:

   ```
   $ sudo apt install postgresql-10
   ```

#### 13.2. Configuring PostgreSQL

1. Log in as the user `postgres` that was automatically created during the installation of PostgreSQL Server:

   ```
   $ sudo su - postgres
   ```

2. Open the `psql` shell:

   ```
   $ psql
   ```

3. This will open the `psql` shell. Now type the following commands one-by-one:

   ```sql
   postgres=# CREATE DATABASE catalog;
   postgres=# CREATE USER catalog;
   postgres=# ALTER ROLE catalog WITH PASSWORD 'password';
   postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
   ```

   Then exit from the terminal by running `\q` followed by `exit`.

### 14. Setting Up Apache to Run the Flask Application

#### 14.1. Installing `mod_wsgi`

The module `mod_wsgi` will allow your Python applications to run from Apache server. To install it, run the following command:
   
```
$ sudo apt install libapache2-mod-wsgi-py3
```

This would also enable `wsgi`. So, you don't have to enable it manually.

After the installation has succeeded, restart the Apache server:

```
$ sudo service apache2 restart
```

#### 14.2. Cloning the Item Catalog Flask application

1. Change the current working directory to `/var/www/`:

   ```
   $ cd /var/www/
   ```

2. Create a directory called `FlaskApp` and change the working directory to it:

   ```
   $ sudo mkdir FlaskApp
   $ cd FlaskApp/
   ```

3. Clone [this repository](https://github.com/SDey96/Udacity-Item-Catalog-Project/tree/development) as the directory `FlaskApp`:

   ```
   $ sudo git clone "yourrepo" FlaskApp
   ```

4. Move inside the newly created directory:

   ```
   $ cd FlaskApp/
   ```


#### 14.3. Installing `virtualenv` and All the Required Packages

1. To install `virtualenv`, run the following command:

   ```
   $ sudo pip3 install virtualenv
   ```

2. Then move to `/var/www/FlaskApp/`:

   ```
   $ cd /var/www/FlaskApp/
   ```

3. Create a Virtual Environment:

   ```
   $ sudo python3 -m virtualenv venv
   ```

4. Change the mode of `venv` to 777:

   ```
   $ sudo chmod 777 venv/
   ```
5. Activate `venv`:

   ```
   $ source venv/bin/activate
   ```

   You should now see a prompt like this:

   ```console
   (venv) grader@ubuntu-s-1vcpu-1gb-sgp1-01:/var/www/FlaskApp$
   ```

6. Install required packages:

   ```
   sudo pip3 install Flask
   sudo pip3 install sqlalchemy
   sudo pip3 install Flask-SQLAlchemy
   sudo pip3 install psycopg2
   sudo apt-get install python-psycopg2 
   sudo pip3 install flask-seasurf
   sudo pip3 install oauth2client
   sudo pip3 install httplib2
   sudo pip3 install requests
   ```

#### 14.4. Setting Up Virtual Hosts

1. Run the following command in terminal to set up a file called `FlaskApp.conf` to configure the virtual hosts:

   ```
   $ sudo nano /etc/apache2/sites-available/FlaskApp.conf
   ```

2. Add the following lines to it:

   ```

   <VirtualHost *:80>
      ServerName 206.189.46.108
      ServerAlias 206.189.46.108.xip.io
      ServerAdmin contact.ganavijayaram1996@gmail.com
      WSGIDaemonProcess FlaskApp python-path=/var/www \
        python-home=/var/www/FlaskApp/venv
      WSGIProcessGroup FlaskApp
      WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
      <Directory /var/www/FlaskApp/FlaskApp/>
          Require all granted
      </Directory>
      Alias /static /var/www/FlaskApp/FlaskApp/static
      <Directory /var/www/FlaskApp/FlaskApp/static/>
          Require all granted
      </Directory>
      ErrorLog ${APACHE_LOG_DIR}/error.log
      LogLevel warn
      CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>

   ```

3. Enable the virtual host:

   ```
   $ sudo a2ensite FlaskApp
   ```

4. Restart Apache server:

   ```
   $ sudo service apache2 restart
   ```

5. Creating the .wsgi File

   Apache uses the `.wsgi` file to serve the Flask app. Move to the `/var/www/FlaskApp/` directory and create a file named `flaskapp.wsgi` with following commands:

   ```
   $ cd /var/www/FlaskApp/
   $ sudo nano flaskapp.wsgi
   ```

   Add the following lines to the `flaskapp.wsgi` file:

   ```python
   #!/var/www/FlaskApp/venv/bin/python3
   import sys
   import logging
   logging.basicConfig(stream=sys.stderr)
   sys.path.insert(0, "/var/www/FlaskApp/")

   from FlaskApp import app as application
   ```

6. Restart Apache server:

   ```
   $ sudo service apache2 restart
   ```
   
   Now you should be able to run the application at <http://206.189.46.108.xip.io/>.
   
   **Note**:If You  still see the default Apache page, run the following commands in order:
   
   ```
   $ sudo a2dissite 000-default.conf
   $ sudo service apache2 restart
   ```

## Debugging


```
$ sudo cat /var/log/apache2/error.log
```

