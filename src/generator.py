from datetime import datetime
from typing import List
from src.user import User

class Generator:
    def __init__(self, users: List[User]):
        self.users = users
        self.compiled_data: map[str, list[str]] = {}

    def update_compiled(self, tracks: set[str], name: str) -> None:
        for t in tracks:
            if self.compiled_data.get(t) is not None:
                self.compiled_data[t].append(name)
            else:
                self.compiled_data[t] = [name]

    def create_files(self, directory: str) -> None:        
        for user in self.users:
            tracks = user.get_all_tracks()
            self.update_compiled(tracks, user.name)
            print(f"Analisadas todas as {len(tracks)} músicas de {user.name.ljust(20)}")

        #self.compiled_data = {track1: [u1, u2, u3], track2: [u4], ...}

        FILES = {}

        for song, users in self.compiled_data.items():
            if len(users) > 1:
                users = tuple(users)
                if FILES.get(users) is not None:
                    FILES[users].append(song)
                else:
                    FILES[users] = [song]

        # FILES = {(u1, u2): [tr1, tr2, tr3], (u1, u3): [tr4, tr5], ...}

        report1 = []
        report2 = {user.name: 0 for user in self.users}
        tot = 0

        for group, songs in FILES.items():
            group_name = '-'.join(group)
            with open(f"{directory}/{group_name}.txt", 'w', encoding='UTF-8') as file:
                file.write("\n".join(songs))
            
            report1.append(f"{group_name}: {len(songs)}")
            tot += len(songs)
            for name in group:
                report2[name] += len(songs)


        report = "\n".join(sorted(report1, key=lambda line: line.count('-')))
        report += "\n\nTotal por pessoa:\n" + "\n".join([f"{k}: {v}" for k, v in report2.items()])
        report += f"\n\nTOTAL DE MÚSICAS: {tot}"

        timestamp = datetime.now().strftime("%d_%m_%y %H_%M")

        with open(f"{directory}/{timestamp}.log", 'w', encoding='UTF-8') as rep:
            rep.write(report)

