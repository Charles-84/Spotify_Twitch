# Spotify_Twitch

Spotify_Twitch est un bot Twitch qui permet de récupérer les informations de lecture actuelles sur Spotify et les afficher sur le chat Twitch en réponse aux commandes `!musique` et `!playlist`.

## Installation

1. Installez les bibliothèques nécessaires :

```bash
pip install twitchio spotipy
```

Créez un fichier config.ini dans le même répertoire que votre script principal, en suivant l'exemple ci-dessous :

2. Configuration :

### 2.1 Configuration du compte Spotify

Avant de pouvoir utiliser l'API Spotify, vous devez créer une application sur le [Tableau de bord des développeurs Spotify](https://developer.spotify.com/dashboard/applications).

1. Connectez-vous à votre compte Spotify et accédez au [Tableau de bord des développeurs Spotify](https://developer.spotify.com/dashboard/applications).

2. Cliquez sur le bouton "Create an App" pour créer une nouvelle application.

3. Remplissez les informations requises pour votre nouvelle application, acceptez les conditions et cliquez sur "Create".

4. Une fois l'application créée, vous verrez les informations "Client ID" et "Client Secret" sur la page de votre application. Notez ces informations, car vous en aurez besoin pour configurer le bot.

5. Cliquez sur "Edit Settings" et ajoutez l'URL de redirection pour votre application (par exemple, `http://localhost:8080`), puis cliquez sur "Save".

### 2.2 Configuration du bot

Dans le fichier principal de votre bot, vous devrez définir les variables de configuration pour Twitch et Spotify. Remplacez les valeurs des variables par vos propres informations d'identification.

```python
# Configuration Twitch et Spotify
twitch_bot_name = "VOTRE_NOM_DE_BOT"
twitch_client_id = "VOTRE_CLIENT_ID"
twitch_refresh_token = "VOTRE_REFRESH_TOKEN"
twitch_token = "VOTRE_TOKEN"
twitch_channel = "VOTRE_CHAINE"

spotify_client_id = "VOTRE_CLIENT_ID_SPOTIFY"
spotify_client_secret = "VOTRE_CLIENT_SECRET_SPOTIFY"
spotify_redirect_uri = "http://localhost:8080"
```

Après avoir défini les variables de configuration, le bot sera lancé avec ces informations. En cas d'erreur, le bot tentera de rafraîchir le token Twitch et de se relancer.

⚠️ Attention : Assurez-vous d'utiliser un compte Spotify Premium pour que le bot fonctionne correctement. Les comptes gratuits ne sont pas compatibles avec certaines fonctionnalités de l'API Spotify.

3. Exécutez le script principal :

```bash
python main.py
```

# Commandes

!musique : Affiche la chanson en cours de lecture, l'artiste et le lien.

!playlist : Affiche le nom de la playlist et son lien.

# Fonctionnalités

Récupère les informations de lecture actuelles sur Spotify.

Vérifie si le streamer est en direct.

Gestion des erreurs de commandes et des délais d'attente.

Rafraîchit automatiquement le jeton d'accès Twitch si nécessaire.
