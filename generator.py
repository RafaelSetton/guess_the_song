import requests
from datetime import datetime
import os
import pickle


class Generator:
    def __init__(self, access_token: str, directory: str):
        self.access_token = access_token
        self.directory = directory
        self.compiled_data: map[str, list[str]] = {}

    def get_playlist_tracks(self, playlist_data: dict) -> list[str]:
        _id = playlist_data['id']
        qtd = playlist_data['tracks']['total']
        tracks = []
        for i in range(0, qtd, 50):
            tracks.extend(requests.get(f"https://api.spotify.com/v1/playlists/{_id}/tracks?offset={i}&limit=50", headers={"Authorization": f"Bearer {self.access_token}"}).json()['items'])

        final = []
        for track in tracks:
            try:
                final.append(f"{track['track']['name']} - {track['track']['artists'][0]['name']}")
            except TypeError:
                pass

        return final

    @property
    def cache_dir(self) -> str:
        return os.path.join(os.getcwd(), "cache")

    def get_data(self, username: str, use_cache: bool) -> dict: 
        """ 
        {playlist_name: [(song_name, artist), ...], ...}
        """
        if os.path.exists(f"{self.cache_dir}/{username}.pickle") and use_cache:
            with open(f"{self.cache_path}/{username}.pickle", 'rb') as f:
                return pickle.load(f)
            
        res = requests.get(f"https://api.spotify.com/v1/users/{username}/playlists?offset=0&limit=50", headers={"Authorization": f"Bearer {self.access_token}"})

        if res.status_code == 401:
            raise TimeoutError("O Token de Acesso Expirou")

        data = {pl['name']: self.get_playlist_tracks(pl) for pl in res.json()['items']}
        
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)
        with open(f"{self.cache_dir}/{username}.pickle", 'wb') as f:
            pickle.dump(data, f)
        return data

    @staticmethod
    def get_all_tracks(data: dict) -> set:
        all_tracks = set()

        for pl in data.values():
            all_tracks.update(set(pl))

        return all_tracks

    def update_compiled(self, tracks: set[str], name: str) -> None:
        for t in tracks:
            if self.compiled_data.get(t) is not None:
                self.compiled_data[t].append(name)
            else:
                self.compiled_data[t] = [name]

    def create_files(self, usernames: map, use_cache: bool = True) -> None:        
        for _id, name in usernames.items():
            tracks = self.get_all_tracks(self.get_data(_id, use_cache))
            self.update_compiled(tracks, name)
            print(f"Analisadas todas as {len(tracks)} músicas de {name}")

        FILES = {}

        for song, users in self.compiled_data.items():
            if len(users)>1:
                users = tuple(users)
                if FILES.get(users) is not None:
                    FILES[users].append(song)
                else:
                    FILES[users] = [song]

        report1 = []
        report2 = {name: 0 for name in usernames.values()}
        tot = 0

        for group, songs in FILES.items():
            group_name = '-'.join(group)
            with open(f"{self.directory}/{group_name}.txt", 'w') as file:
                file.write("\n".join(songs))
            report1.append(f"{group_name}: {len(songs)}")
            tot += len(songs)
            for name in group:
                report2[name] += len(songs)


        report = "\n".join(sorted(report1, key=lambda line: line.count('-')))
        report += "\n\nTotal por pessoa:\n" + "\n".join([f"{k}: {v}" for k, v in report2.items()])
        report += f"\n\nTOTAL DE MÚSICAS: {tot}"

        timestamp = datetime.now().strftime("%d_%m_%y %H_%M")

        with open(f"{self.directory}/{timestamp}.log", 'w', encoding='UTF-8') as rep:
            rep.write(report)

