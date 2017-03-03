import sys

class Symbol:

	def __init__(self, token, tokenType, line):
		self.token     = token
		self.tokenType = tokenType
		self.line      = line

	def __str__(self):
		return "%s\t\t\t%s\t\t\t%d" % (self.token, self.tokenType, self.line)

class Lexical:

	def __init__(self, inputFile):
		self.file = inputFile
		self.symbols = []
		self.comment = False
		self.reserved  = ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 'not', 'do']
		self.delimiters = [',', '.',';', ':', ':=', ')', '(' ]
		self.operators = ['+', '-', '*', '/', '=', '<', '>', '>=', '<=', 'and', 'or']

	def __str__(self):
		r = "Token\t\t\tClassification\t\t\tLine\n\n"
		for s in self.symbols:
			r += str(s) + '\n'
		return r

	def isBlank(self, a):
		return ((a == ' ') or (a == '\t') or (a == '\n') )

	#Identifica palavras
	def recognizeWord(self, line, i, l):

		s = line[i]
		i += 1

		while(str.isalpha(line[i]) or str.isdigit(line[i]) or line[i] == '_'):
			s += line[i]
			i += 1

		#checar se eh reservado ou se eh identificador ou operador (and e or)
		if(s in self.reserved):
			self.symbols.append(Symbol(s, "Reserved Word", l))
		elif(s in self.operators):
			self.symbols.append(Symbol(s, "Operator", l))
		else:
			self.symbols.append(Symbol(s, "Indentifier", l))

		return i

	#Checar se a entrada eh um numero (real ou inteiro)
	def recognizeNumber(self, line, i, l):
		s = line[i]
		i += 1

		while(str.isdigit(line[i])):
			s += line[i]
			i += 1

		#checar se eh inteiro ou real
		if(line[i] == '.' and str.isdigit(line[i+1])):
			s += line[i]
			i += 1

			while(str.isdigit(line[i])):
				s += line[i]
				i += 1

			self.symbols.append(Symbol(s, "Real Number", l))

		else:
			self.symbols.append(Symbol(s, "Integer Number", l))

		return i

	#Trata os comentarios entre chaves
	def checkComents(self, line, i, lim, l):
		if(line[i] == '{'):
			i += 1
			self.comment = True

		while((i < lim) and (line[i] != '}') ):
			i += 1

		#encontrou o '}'
		if(i != lim):
			i += 1
			self.comment = False

		return i

	#Checar se eh delimitador ou operador
	def recognizeOthers(self, line, i, l):

		#checa os operadores e delimitadores com mais de um caractere
		if( ( (line[i] == ':') or (line[i] == '>') or (line[i] == '<') ) and (line[i+1] == '=') ) :
			s = line[i] + line[i+1]
			i += 1
			if( s in self.delimiters):
				self.symbols.append(Symbol(s, "Delimiter", l))

			elif (s in self.operators):
				self.symbols.append(Symbol(s, "Operator", l))
				
		#verifica se o char eh um delimitador
		elif( line[i] in self.delimiters):
			self.symbols.append(Symbol(line[i], "Delimiter", l))

		elif (line[i] in self.operators):
			self.symbols.append(Symbol(line[i], "Operator", l))

		return i

	def checkValidation(self,line, i):
		return ( (not str.isalpha(line[i]) ) and
		 		 (not str.isdigit(line[i]) ) and
		 		 (not self.isBlank(line[i])) and 
		 		 (not (line[i] in self.delimiters)) and
		 		 (not (line[i] in self.operators) ) and 
		 		 (line[i] != '{') and (line[i] != '}'))

	def buildLexical(self):
		l = 1

		with open(self.file) as fp:
		
			for line in fp:
				
				length = len(line)
				i = 0

				while(i < length):
					#Tratar comentarios
					if(line[i] == '}' and (not self.comment)):
						print("ERRO! COMENTARIO NAO INICIADO, LINHA %d" % l)
						sys.exit(1)

					if(line[i] == '{' or self.comment):
						i = self.checkComents(line, i, length, l)

					#Caso o comentario seja de bloco
					if(self.comment):
						break

					#checar se a palavra eh composta por letras, numeros e underline
					if(str.isalpha(line[i]) or (line[i] == '_')):
						i = self.recognizeWord(line, i, l)

					#checar se eh numero
					if(str.isdigit(line[i])):
						i = self.recognizeNumber(line, i, l)

					#checa os operadores e delimitadores
					if( (line[i] in self.delimiters) or (line[i] in self.operators) ):
						i = self.recognizeOthers(line, i, l)
					
					if(self.checkValidation(line, i)):
						print("ERRO! %s NAO FAZ PARTE DO ALFABETO, LINHA %d" % (line[i], l))
						i += 1
						sys.exit(1)

					#incrementa o ponteiro que aponta pra cada char da linha
					i += 1
				l += 1

		if(self.comment):
			print("ERRO! COMENTARIO NAO FINALIZADO")
			sys.exit(1)

lex = Lexical("../entrada.txt")
lex.buildLexical()
print(lex)