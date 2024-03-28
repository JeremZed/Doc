# Installation d'un VPS pour un site web

## Obtenir le VPS

Par exemple commander un VPS sur ovh : https://www.ovhcloud.com/fr/vps/

##  Premier pas

### Se connecter

Depuis la machine en local, vérification des identifiants de connexion.

```sh
ssh <username>@<IP>
```

### Changer le mot de passe

Lancer la commande suivante et suivre les instructions.

```sh
passwd
```

### Ajouter sa clé SSH

Au lieu de se connecter avec le couple user/password, préviligier la connexion via ses clés SSH.
Exécuter la commande sur la machine en local pour envoyer la clé ssh de l'utilisateur en cours.

```sh
ssh-copy-id <username>@<IP>
```

Si on souhaite ajouter directement la clé public de l'utilisateur depuis le serveur distant. On edite le fichier authorized_keys sur le serveur et on copie/colle la clé du nouvel utilisateur a qui on souhaite donner un accès ssh.

```sh
nano ~/.ssh/authorized_keys
```

```sh
sudo systemctl restart ssh
```

Une fois l'ajouter terminé, on vérifie que la connexion se fait correctement. Aucune demande de mot de passe de l'utilisateur ne doit apparaître. Un mot de passe peut être demandé si la clé ssh elle-même possède une sécurité avec un mot de passe.

```sh
ssh <username>@<IP>
```

### Ajouter un alias

Au lieu de toujours indiquer l'adresse IP du serveur, on va utiliser un alias.

```sh
nano ~/.ssh/config
```

```txt
Host vps
    HostName <IP-SERVER>
    IdentityFile ~/.ssh/id_rsa
```

```sh
ssh <username>@vps
```

Ou alors on indique directement l'user dans le fichier ~/.ssh/config

```txt
Host vps
    HostName <IP-SERVER>
    IdentityFile ~/.ssh/id_rsa

Host vps_client1
    HostName <IP-SERVER>
    User <username>
    IdentityFile ~/.ssh/id_rsa
```

```sh
ssh vps_client1
```

On peut même générer une clé ssh en local par vps, et les enregistrer dans des fichiers spécifiques et ensuite les utiliser via le fichier de config.

### Fail2ban

Installation d'un minimum de sécurité avec Fail2ban

```sh
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

```txt
[sshd]
enabled = true
port = ssh
filter = sshd
maxretry = 3
findtime = 5m
bantime  = 30m
```

```sh
sudo service fail2ban restart
```

### Sécurisation serveur SSH

Apporter un minimum de sécurité sur le serveur SSH.

```sh
sudo nano /etc/ssh/sshd_config
```

```txt
PermitRootLogin no

PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

RSAAuthentication no
UsePAM no
KerberosAuthentication no
GSSAPIAuthentication no
PasswordAuthentication no
```

```sh
sudo /etc/init.d/ssh restart
```

## Installation Apache2

Installation du serveur web.

```sh
sudo apt install apt-transport-https lsb-release ca-certificates apache2 zip unzip
```

## Installation PHP8.2

Installation de php8.2

```sh
sudo dpkg -l | grep php | tee packages.txt
sudo add-apt-repository ppa:ondrej/php
sudo apt update
sudo apt install php8.2 php8.2-cli php8.2-{bz2,curl,mbstring,dom}
sudo apt install php8.2-fpm

sudo a2enconf php8.2-fpm
sudo systemctl reload apache2
```

## Installation de Composer

Se réferer à la documention : https://getcomposer.org/download/

Et ne pas oublier de créer le lien pour une utilisation globale sur le serveur.

```sh
sudo mv composer.phar /usr/local/bin/composer
composer --version
```

## Installation de Node

Se référer à la documention  : https://nodejs.org/en/download/package-manager

Exemple :

```sh
# installs NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# download and install Node.js
nvm install 21
# verifies the right Node.js version is in the environment
node -v # should print `v21.7.1`
# verifies the right NPM version is in the environment
npm -v # should print `10.5.0`
```

## Installation de Git

```sh
sudo apt install git
```

## Installation d'un projet

On récupère le projet via git.

```sh
git clone xxxxx
```

On se positionne dans le projet web.

```sh
composer install
npm install
npm run build
```

## Création du vhost apache

```sh
cd /etc/apache2/sites-available/
sudo nano mysite.conf
```

```apache
<VirtualHost example.local:80>
    # The ServerName directive sets the request scheme, hostname and port that
    # the server uses to identify itself. This is used when creating
    # redirection URLs. In the context of virtual hosts, the ServerName
    # specifies what hostname must appear in the request's Host: header to
    # match this virtual host. For the default virtual host (this file) this
    # value is not decisive as it is used as a last resort host regardless.
    # However, you must set it for any further virtual host explicitly.
    #ServerName www.example.com

    ServerName example.local

    ServerAdmin webmaster@localhost
    DocumentRoot /home/jeremy/Lab/repo/site-example/site/public

    # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
    # error, crit, alert, emerg.
    # It is also possible to configure the loglevel for particular
    # modules, e.g.
    #LogLevel info ssl:warn

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    <Directory /home/jeremy/Lab/repo/site-example/site/public>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # For most configuration files from conf-available/, which are
    # enabled or disabled at a global level, it is possible to
    # include a line for only one particular virtual host. For example the
    # following line enables the CGI configuration for this host only
    # after it has been globally disabled with "a2disconf".
    #Include conf-available/serve-cgi-bin.conf
</VirtualHost>
```

```sh
sudo a2ensite mysite.conf
sudo systemctl reload apache2
sudo a2enmod rewrite
sudo systemctl reload apache2
# sudo adduser -g www-data $(whoami)
# sudo usermod -a -G www-data $(whoami)
sudo systemctl reload apache2
```

## Créer un alias sur un nom de domaine

Sur OVH, se positionner sur le nom de domaine souhaité. Ensuite Zone DNS, ajouter une entrée de type A et indiquer l'adresse IP du VPS.

## Laravel

Donner les droits sur le fichier de log.

```sh
sudo chown -R www-data:www-data /path/du/projet/storage/
```

Créer un fichier .env

```sh
cd /path/to/project
nano .env


sudo su www-data -s /bin/sh
php artisan optimize
```

## Installer SSL

```sh
sudo apt install certbot python3-certbot-apache
sudo certbot --apache
```

- Indiquez une adresse email.
- Accepter les CGU.
- Decliner la proposition de partage de l'adresse email.
- Selection du domaine à sécuriser.

## Installer base de données MySQL

```sh
sudo apt install mysql-server
sudo mysql_secure_installation
```

Sélectionner l'option "2", et ensuite répondre "Y" pour le reste.

Créer un nouvel utilisateur avec un mot de passe.

```sh
sudo mysql
CREATE USER 'username'@'localhost' IDENTIFIED BY 'here-password-very-strong';
GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' WITH GRANT OPTION;
```

Si une erreur du type "Client does not support authentification protocol requested by server..."

```sh
CREATE USER 'username'@'localhost' IDENTIFIED WITH mysql_native_password BY 'here-password-very-strong';
```
