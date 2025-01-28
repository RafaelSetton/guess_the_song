from src.__init__ import *
import os
import pickle
from functools import wraps

def cache_to_pickle(file_path: str):
    def decorator(func):
        real_path = f"f'{file_path}'"
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            file_path = eval(real_path)

            # Load existing cache if file exists
            if os.path.exists(file_path) and CACHE_ENABLED:
                with open(file_path, "rb") as f:
                    return pickle.load(f)
                
            # Compute and cache result
            result = func(*args, **kwargs)
            
            # Save updated cache to pickle
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                pickle.dump(result, f)

            return result
        return wrapper
    return decorator


class Playlist:
    def __init__(self, data: dict):
        self.owner_id = data['owner']['id']
        self.id = data['id']
        self.name = data['name']
        self.qtd_tracks = data['tracks']['total']

    @cache_to_pickle("{CACHE_DIR}/{self.owner_id}/playlists/{self.id}.pickle")
    def get_tracks(self):
        tracks = []
        for i in range(0, self.qtd_tracks, 50):
            tracks.extend(api.get(f"playlists/{self.id}/tracks?offset={i}&limit=50").json()['items'])

        final = []
        for track in tracks:
            try:
                final.append(f"{track['track']['name']} - {track['track']['artists'][0]['name']}")
            except TypeError:
                pass

        return final

class User:
    def __init__(self, user_id, name, code):
        '''
        Parameters:
            user_id: Spotify User Id
            name: The Display Name
            code: The code for points calculation
        '''
        self.id = user_id
        self.name = name
        self.code = code
    
    def __repr__(self):
        return f"{self.name} ({self.code}): {self.id}"

    @classmethod
    def all_from_file(cls, file_path: str):
        with open(file_path, encoding='UTF-8') as f:
            for line in f.readlines():
                if line.strip().startswith("#"):
                    continue
                name, code, _id = line.split()
                yield cls(_id, name, code[1:-2])
        
    @cache_to_pickle("{CACHE_DIR}/{self.id}/playlists.pickle")
    def get_playlists(self):
            
        res = api.get(f"users/{self.id}/playlists?offset=0&limit=50")

        ret = [Playlist(pl) for pl in res.json()['items']]
        
        return ret

    @cache_to_pickle("{CACHE_DIR}/{self.id}/data.pickle")
    def get_data(self) -> dict: 
        """ 
        {playlist_name: [(song_name, artist), ...], ...}
        """
        playlists = self.get_playlists()

        msg = "Buscando playlists de {nome}: {qtd} / {tot};    Próxima: {prox}".format(nome=self.name, qtd='{qtd}', tot=len(playlists), prox='{prox}')

        data = {}
        for qtd, pl in enumerate(playlists):
            print(msg.format(qtd=qtd, prox=pl.name.ljust(50)), end='\r')
            data[pl.name] = pl.get_tracks()
        
        return data

    @cache_to_pickle("{CACHE_DIR}/{self.id}/all_tracks.pickle")
    def get_all_tracks(self) -> set:
        all_tracks = set()

        for pl in self.get_data().values():
            all_tracks.update(set(pl))

        return all_tracks



if __name__ == '__main__':
    u = User("31upyrfgyrgvomgguoe5jpppkq4e", "Setton", "S", False)
    print(u.get_playlists())