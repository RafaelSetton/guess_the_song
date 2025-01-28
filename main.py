from src.__init__ import *
from src.generator import Generator
from src.user import User
from src.txt_to_xl import create_score_table
from os import path, mkdir

def main(output_directory: str, input_file: str):
	# directory = "./out/vizinhos"
	if not path.exists(output_directory):
		mkdir(output_directory)

	users = list(User.all_from_file(input_file))

	Generator(users).create_files(output_directory)
	create_score_table(output_directory, [user.name for user in users])


if __name__ == '__main__':
	out_dir = input("Caminho para o diretório de saída: ")
	in_file = input("Caminho para o arquivo de entrada: ")
	cache = None
	while cache == None:
		if (temp := input("Usar dados do cache? (S/N) ").upper()) in ('S', 'N'):
			cache = temp == 'S'
			cache_path = input("Caminho para o diretório de cache: (Deixe em branco para usar o padrão)")
			if cache_path:
				CACHE_DIR = cache_path
	CACHE_ENABLED = cache
	main(out_dir, in_file)