F=open('lsst.xml', 'r')
A=F.readlines()
F.close()

list1=[]
for l in A:
    l=l.strip()
    l=l[8:-9]
    last,first=l.split(',')
    first=first[1:]
    list1.append('{'+last+'}, '+first[0].upper()+'.')

all_people = ' and '.join(list1)

text="""
@ARTICLE{2012arXiv1211.0310L,
   author = {{LSST Dark Energy Science Collaboration} and %s},
    title = "{Large Synoptic Survey Telescope: Dark Energy Science Collaboration}",
  journal = {ArXiv e-prints},
archivePrefix = "arXiv",
   eprint = {1211.0310},
 primaryClass = "astro-ph.CO",
 keywords = {Astrophysics - Cosmology and Extragalactic Astrophysics, High Energy Physics - Experiment},
     year = 2012,
    month = nov,
   adsurl = {http://adsabs.harvard.edu/abs/2012arXiv1211.0310L},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
""" % all_people

F=open('lsst.bib','w')
F.write(text)
F.close()
