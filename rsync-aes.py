#!/usr/bin/python -d

import sys
import getopt
import os
from Crypto.Cipher import AES


## Fonction aide ##
def usage():
	print "-a		Mode archivage = -u"
	print "-d, --delete	Suppression des fichiers sur la destination, etant manquant sur la source."
	print "-u		Mise a jour des fichiers si plus recent."
	print "--test		Test de la copie"
	print "-h, --help	Cette aide"
	print "-v		Mode verbeux"


## Fonction de gestion des parametres ##
def set_param(argv):
	
	try:
		opts, args = getopt.getopt(argv, 'adhuv', ['delete','help','test'])
	except getopt.GetoptError, err:
		print str(err)
		usage()                         
		sys.exit(2)                     

	if opts:
		for opt, arg in opts:
			if opt in ( "-h", "--help" ):
				usage() 	# 
				return 1
			elif opt == '-a':
				print "Parametre -a"
			elif opt in ( '-d','--delete' ):
				print "Parametre -d ou --delette : "
			elif opt == '-u':
				print "Parametre -u"
			elif opt in '-v':
				print "Parametre -v"
			else:
				usage()
				return 1
	else:
		usage()
		return 1

	return args


class fichier():
	def __init__(self,fichier):
		self.size=os.path.getsize(fichier)

		try:
			self.fd=os.open(fichier,os.O_RDWR)
		except OSError:
			print str(error)
			sys.exit(2)

	def read(self):
		try:
			return os.read(self.fd,self.size)
		except OSError:
			print str(error)
			sys.exit(2)

	def write(self,datas):
		try:
			os.write(self.fd,datas)
		except OSError:
			print str(error)
			sys.exit(2)

	def close(self):
		try:
			os.close(self.fd)
		except OSError:
			print str(error)
			sys.exit(2)
		

def main(argv=None):
	# Gestion de parametres 
	if argv is None:
		argv = sys.argv[1:]
	fichiers=set_param(argv)

	fsrc=fichier(fichiers[0])
	datas=fsrc.read()


	key = '0123456789abcdef'
	mode = AES.MODE_CBC
	encryptor = AES.new(key, mode)
	decryptor = AES.new(key, mode)

	fdst=fichier(fichiers[1])
	fdst.write(encryptor.encrypt(datas))


	fsrc.close()
	fdst.close()


	fd=os.open(fichiers[1],os.O_RDONLY)
#	print "file crypte", os.read(fd,os.path.getsize(fichiers[1]))
	print "file decrypte : ", decryptor.decrypt(os.read(fd,os.path.getsize(fichiers[1])))

if __name__ == "__main__":
	sys.exit(main())
