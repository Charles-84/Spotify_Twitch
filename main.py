import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import commands
import requests

class TwitchSpotifyBot(commands.Bot):
    def __init__(
        self,
        twitch_bot_name,
        twitch_client_id,
        twitch_token,
        twitch_channel,
        spotify_client_id,
        spotify_client_secret,
        spotify_redirect_uri,
    ):
        super().__init__(
            token=twitch_token,
            client_id=twitch_client_id,
            nick=twitch_bot_name,
            prefix="!",
            initial_channels=[twitch_channel],
        )

        # Configuration de l'authentification Spotify
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=spotify_client_id,
                client_secret=spotify_client_secret,
                redirect_uri=spotify_redirect_uri,
                scope="user-read-playback-state",
                cache_path = ".cache_spotify"
            )
        )

    async def event_ready(self):
        print(f"Bot '{self.nick}' prêt et connecté à Twitch.")
    
    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            remaining_time = int(error.retry_after)
            await ctx.send(f"Vous devez attendre {remaining_time} secondes avant d'utiliser cette commande à nouveau.")
        else:
            print(f"Une erreur inattendue est survenue: {error}")

    # Fonction pour récupérer les informations de lecture actuelles sur Spotify
    def get_spotify_info(self):
        current_playback = self.sp.current_playback()
        if not current_playback:
            return (
                "Aucune musique en cours de lecture",
                "Aucun artiste",
                "Aucune playlist",
                "",
                "",
            )

        current_song = current_playback["item"]["name"]
        current_song_link = current_playback["item"]["external_urls"]["spotify"]
        artist = current_playback["item"]["artists"][0]["name"]
        playlist_id = current_playback["context"]["uri"].split(":")[-1]
        playlist = self.sp.playlist(playlist_id)
        playlist_name = playlist["name"]
        playlist_link = playlist["external_urls"]["spotify"]

        return (
            current_song,
            artist,
            playlist_name,
            current_song_link,
            playlist_link,
        )

    # Commande pour afficher la chanson en cours de lecture, l'artiste et le lien
    @commands.command(name="musique")
    @commands.cooldown(rate=1, per=60, bucket=commands.Bucket.user)
    async def musique(self, ctx):
        if await self.is_live(twitch_channel):
            return

        current_song, artist, _, current_song_link, _ = self.get_spotify_info()
        if current_song == "Aucune musique en cours de lecture":
            await ctx.send(current_song)
        else:
            await ctx.send(
                f"Chanson en cours de lecture: {current_song} - Artiste: {artist} - Lien: {current_song_link}"
            )

    # Commande pour afficher le nom de la playlist et son lien
    @commands.command(name="playlist")
    @commands.cooldown(rate=1, per=60, bucket=commands.Bucket.user)
    async def playlist(self, ctx):
        if not await self.is_live(twitch_channel):
            return

        _, _, playlist_name, _, playlist_link = self.get_spotify_info()
        if playlist_name == "Aucune playlist":
            await ctx.send(playlist_name)
        else:
            await ctx.send(
                f"Nom de la playlist: {playlist_name} - Lien: {playlist_link}"
            )

    # Vérifie si le streamer est en live
    async def is_live(self, channel):
        streams = await self.fetch_streams(user_logins=[channel])
        if streams:
            stream = streams[0]
            return stream.type == "live"
        return False

    async def refresh_twitch_token(client_id, client_secret, refresh_token):
        url = "https://id.twitch.tv/oauth2/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            json_response = response.json()
            new_access_token = json_response["access_token"]
            new_refresh_token = json_response["refresh_token"]

            return new_access_token, new_refresh_token
        else:
            raise Exception("Failed to refresh Twitch access token.")


if __name__ == "__main__":
    twitch_bot_name = "Fullbot"
    twitch_client_id = "VOTRE_CLIENT_ID"
    twitch_refresh_token = "VOTRE_REFRESH_TOKEN"
    twitch_token = "VOTRE_TOKEN"
    twitch_channel = "VOTRE_CHAINE"

    spotify_client_id = "VOTRE_CLIENT_ID_SPOTIFY"
    spotify_client_secret = "VOTRE_CLIENT_SECRET_SPOTIFY"
    spotify_redirect_uri = "http://localhost:8080"

    try : 
        bot = TwitchSpotifyBot(
            twitch_bot_name,
            twitch_client_id,
            twitch_token,
            twitch_channel,
            spotify_client_id,
            spotify_client_secret,
            spotify_redirect_uri,
        )
        
        bot.run()
    except:
        twitch_token = TwitchSpotifyBot.refresh_twitch_token(twitch_client_id, twitch_token, twitch_refresh_token)

        bot = TwitchSpotifyBot(
            twitch_bot_name,
            twitch_client_id,
            twitch_token,
            twitch_channel,
            spotify_client_id,
            spotify_client_secret,
            spotify_redirect_uri,
        )
        
        bot.run()
