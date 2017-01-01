# This Python file uses the following encoding: utf-8
"""
Usage:
python step1.py inputfile outputfile logfile
e.g.
python step1.py sk0.txt sk1.txt step1_notes.txt
"""
import re,codecs,sys
import transcoder
def step1(filein,filout,logfile):
	fin = codecs.open(filein,'r','utf-8')
	fout = codecs.open(fileout,'w','utf-8')
	fillog = codecs.open(logfile,'w','utf-8')
	fillog.write('; denotes unchanged item. $ denotes verb number. * denotes internal SK reference\n')
	sksutranum = []
	rootnum = 0
	for line in fin:
		# Point 5a
		if re.search(u'।([^।]+)([(]वा[)][ ]*।)',line):
			line = re.sub(u'।([^।]+)([(]वा[)][ ]*।)',u'{%\g<1>%} (वा)।',line)
		# Point 5b. 
		# Questionable vArtikas. Noted in sk1_notes.txt. Needs manual examination. If they are not vArtikas, their preceding and ending | need correction in sk0.txt for future automated generation of sk1.txt from sk0.txt.
		if re.search(u'।[^ ।]([^।]+)।।',line):
			line = re.sub(u'।([^ ।][^।0-9]+)।।',u'{%?\g<1>?%} ।।',line)
		# sUtra references
		if re.match('[(]([0-9]+)[)]',line):
			# Points 1,6a,6b
			sksutranum = re.findall(u'^[(]([0-9]+)[)]',line)
			line = re.sub(u'^[(]([0-9]+)[)]([^0-9]+)([\-0-9]+)','{#\g<1>#} \g<2>{@\g<3>@}',line) # (1)हलन्त्यम्    1-3-3 -> {#1#} हलन्त्यम्    {@1-3-3@}
		# Internal references of SK / verb numbers in tiGanta prakaraNa.
		elif re.search(u' [0-9]{1,4} ',line):
			m = re.findall(u' ([0-9]{1,4}) ',line)
			for member in m:
				if int(sksutranum[0]) > 2164 and int(sksutranum[0]) < 2829 and int(member) == rootnum+1: # Ignore roots having the same markup as internal references to SK.
					rootnum = int(member)
					line = line.replace(member,'{$'+member+'$}')
					fillog.write('$ '+sksutranum[0]+' '+member+'\n')
					print '$', sksutranum[0], member
					if member == '1208': # 1209 is missing in original too.
						rootnum = int(member)+1
				elif int(member) <= 5:
					print ';', sksutranum[0], member
					fillog.write('; '+sksutranum[0]+' '+member+'\n')
				else:
					print '*', sksutranum[0], member
					line = line.replace(member,'{*'+member+'*}')
					fillog.write('* '+sksutranum[0]+' '+member+'\n')
		elif re.search(u'[0-9]{2,4}।',line):
			m = re.findall(u'([0-9]{2,4})।',line)
			line = re.sub(u'([0-9]{2,4})।',u'{*\g<1>*}।',line)
			for member in m:
				print '*', sksutranum[0], member
				fillog.write('* '+sksutranum[0]+' '+member+'\n')
			
		# Point 4
		line = line.replace(u'(अ)',u'॒')
		line = line.replace(u'(स्व)',u'॑')
		# Point 2
		line = re.sub(u'([^ ])।',u'\g<1> ।',line)
		# Point 3
		line = line.replace(u'।।',u'॥')
		line = line.replace(u'। ।',u'॥')
		fout.write(line)
	fin.close()
	fout.close()
	fillog.close()
if __name__=="__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	logfile = sys.argv[3]
	step1(filein,fileout,logfile)
