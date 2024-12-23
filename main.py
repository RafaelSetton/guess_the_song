from txt_to_xl import create_score_table
from generator import Generator
from token_handler import load_token
from gui import App
from os import path, mkdir

def onSubmit(usernames: map, directory: str, use_cache: bool):
    token = load_token()

    if not path.exists(directory):
        mkdir(directory)

    Generator(token, directory).create_files(usernames, use_cache)
    create_score_table(directory, list(usernames.values()))

if __name__ == '__main__':
    app = App(onSubmit)
    app.add_components()
    app.mainloop()
    