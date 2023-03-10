# -*- coding: utf-8 -*-
"""Trabalho de BI - Big Data - Hadoop.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qEKT2B2Pqo9qWOTP1kyxE-hTIX0y9cOo
"""

#Instalando java
!apt-get install openjdk-8-jdk-headless -qq > /dev/null

#Criando variável do java (JAVA_HOME)
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"

#Baixando HADOOP 3.3.0
!wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz

#Extraindo o hadoop ...
!tar -xzvf hadoop-3.3.0.tar.gz

#Copiando o hadoop para user/local
!cp -r hadoop-3.3.0/ /usr/local/

#Procurando o Path do Java
!readlink -f /usr/bin/java | sed "s:bin/java::"

#Rodando o  Hadoop da pasta /usr/local
!/usr/local/hadoop-3.3.0/bin/hadoop

#Criando a pasta de input dos resultados
!mkdir ~/testin

#Copiando os arquivos ...
!cp /usr/local/hadoop-3.3.0/etc/hadoop/*.xml ~/testin

#Rodando o MapReduce ...
!/usr/local/hadoop-3.3.0/bin/hadoop jar /usr/local/hadoop-3.3.0/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.0.jar grep ~/testin ~/testout 'allowed[.]*'

#Baixando a base de dados ...
!wget http://qwone.com/~jason/20Newsgroups/20news-18828.tar.gz
!tar -xzvf 20news-18828.tar.gz

#Alterando a permissão dos arquivos, para serem acessíveis pelo sistema
!chmod u+rwx /content/mapper.py
!chmod u+rwx /content/reducer.py

#Executando  o MapReduce
!/usr/local/hadoop-3.3.0/bin/hadoop jar /usr/local/hadoop-3.3.0/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -input /content/20news-18828/alt.atheism/49960 -output ~/tryout -file /content/mapper.py  -file /content/reducer.py  -mapper 'python mapper.py'  -reducer 'python reducer.py'

#Gerando mapper.py
content="""import sys
import io
import re
import nltk
nltk.download('stopwords',quiet=True)
from nltk.corpus import stopwords
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

stop_words = set(stopwords.words('english'))
input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='latin1')
for line in input_stream:
  line = line.strip()
  line = re.sub(r'[^\w\s]', '',line)
  line = line.lower()
  for x in line:
    if x in punctuations:
      line=line.replace(x, " ") 

  words=line.split()
  for word in words: 
    if word not in stop_words:
      print('%s\t%s' % (word, 1))
"""

f = open("mapper.py", "w")
f.write(content)
f.close()

#Gerando reducer.py
content="""from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    line=line.lower()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    try:
      count = int(count)
    except ValueError:
      #count was not a number, so silently
      #ignore/discard this line
      continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # write result to STDOUT
            print ('%s\t%s' % (current_word, current_count))
        current_count = count
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print( '%s\t%s' % (current_word, current_count))
"""

f = open("reducer.py", "w")
f.write(content)
f.close()