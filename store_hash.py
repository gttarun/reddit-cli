import os

def store_hash(hash_code=''):
	if hash_code:
		w_directory = os.getcwd()
		hash_file = open(w_directory + "hash.txt", "a")
		hash_file.write(hash_code)
		hash_file.close()
	return

store_hash("hash")
