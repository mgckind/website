import bibtexparser
import re
import json
import os
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogeneize_latex_encoding

ROOT = '/home/matias/Research/website/'

selected_titles = ['Kubernetes']

journal_dict = {
    "\\mnras": 'MNRAS',
    "\\aj": 'AJ',
    "\\apj": 'ApJ',
    "\\prd": 'PhRvD',
    "\\apjl": 'ApJL',
    "\\apjs": 'ApJS',
    "\\pasa": 'PASA',
    "\\aap": 'A\&A',
    "\\nat": 'Nature',
    "\\pasp": 'PASP',
}


with open('myrefs.bbl') as bibtex_file:
    parser = BibTexParser()
    # parser.customization = homogeneize_latex_encoding
    pubs = bibtexparser.load(bibtex_file, parser=parser)


def get_title(entry):
    title = entry['title'].replace('\n', '')
    return title


def get_journal(entry):
    try:
        title = entry['journal'].replace('\n', '')
    except:
        if entry['ENTRYTYPE'] == 'inproceedings':
            title = entry['booktitle'].replace('\n', '')
        else:
            title = None
    try:
        title = journal_dict[title]
    except:
        pass
    return title


def get_year(entry):
    title = entry['year'].replace('\n', '')
    title = title.replace('{', '')
    title = title.replace('}', '')
    return title


def get_pages(entry):
    try:
        volume = entry['volume'].replace('\n', '')
        volume = volume.replace('{', '')
        volume = volume.replace('}', '')
        pages = entry['pages'].replace('\n', '')
        pages = pages.replace('{', '')
        pages = pages.replace('{', '')
        all_pages = volume+':'+pages
    except:
        all_pages = ''
    return all_pages


def get_url(entry):
    try:
        title = entry['adsurl'].replace('\n', '')
        title = title.replace('{', '')
        title = title.replace('}', '')
        adslink = True
    except:
        title = ""
        adslink = False
    return title, adslink


def get_doi(entry):
    try:
        title = entry['doi'].replace('\n', '')
        title = 'http://dx.doi.org/'+title
    except:
        title = '#'
    return title


def get_authors(entry):
    temp = entry['author'].replace('\n', ' ')
    authors = temp.split(' and ')
    newlist = []
    shortlist = []
    new_dict = []
    i = 0
    num_authors = 6
    for a in authors:
        i = i+1
        temp = {}
        try:
            last, first = a.split(',')
        except:
            last = a
            first = ''
        # print(first, last)
        first = first.replace(' ', '')
        first = first.replace('~', ' ')
        ser = re.search('{(.+)}', last)
        if ser is None:
            continue
        else:
            last = ser.group(1)

        if last == 'Kind':
            last = 'Carrasco Kind'
            first = 'M.'
            temp['first'] = first
            temp['last'] = last
            temp['main'] = True
            temp['color'] = 'black'
        elif last == 'Carrasco-Kind':
            last = 'Carrasco Kind'
            first = 'M.'
            temp['first'] = first
            temp['last'] = last
            temp['main'] = True
            temp['color'] = 'black'
        else:
            temp['first'] = first
            temp['last'] = last
            temp['main'] = False
            temp['color'] = 'blue'
        if i < num_authors:
            shortlist.append(first+' '+last)
        newlist.append(first+' '+last)
        new_dict.append(temp)

    if i >= num_authors:
        shortlist.append('et al.')
    return ", ".join(shortlist), ", ".join(newlist)


def get_arxiv(entry):
    try:
        arxiv = entry['eprint'].replace('\n', '')
        prefix = entry['archiveprefix'].replace('\n', '')
    except:
        if entry['ENTRYTYPE'] == 'inproceedings':
            arxiv = 'None'
            prefix = 'inpro'
        else:
            arxiv = ''
            prefix = ''
    return prefix, arxiv


with open(os.path.join(ROOT, 'publications.json'), 'w') as out:
    print('ddd')
    Alldata = []
    Alldatamine = []
    datamine = []
    texall = []
    texmine = []
    for y in ('0000', '2018', '2017', '2016', '2015', '2014', '2013', '2012'):
        temp2 = {}
        temp3 = {}
        temp2['byear'] = y
        if y == '0000':
            temp2['byear'] = 'In preparation'
        data = []
        for i in range(len(pubs.entries)):
            et = pubs.entries[i]
            year = get_year(et)
            if year != y:
                continue
            preplink = False
            doi = get_doi(et)
            if doi == "#":
                doilink = False
            else:
                doilink = True
                kind = 'Published'
            url, adslink = get_url(et)
            journal = get_journal(et)
            pages = get_pages(et)
            prefix, arxiv = get_arxiv(et)
            if arxiv == '':
                arxiv_url = '#'
                alink = False
                slink = False
                pdf_link = False
                pdf_url = '#'
            else:
                if prefix == 'arXiv':
                    arxiv_url = 'http://arxiv.org/abs/'+arxiv
                    alink = True
                    slink = False
                    pdf_link = True
                    pdf_url = 'http://arxiv.org/pdf/'+arxiv
                    if not doilink:
                        kind = 'Arxiv'
                if prefix == 'inpro':
                    for tt in selected_titles:
                        if tt in et['title']:
                            arxiv_url = '#'
                            alink = False
                            slink = False
                            pdf_link = True
                            pdf_url = ''
                        else:
                            arxiv_url = '#'
                            alink = False
                            slink = False
                            pdf_link = False
                            pdf_url = ''
                if prefix == 'ascl':
                    arxiv_url = 'http://ascl.net/'+arxiv
                    alink = False
                    slink = True
                    journal = 'Astrophysics Source Code Library'
                    kind = 'Software'
                    pdf_link = False
                    pdf_url = '#'
                if prefix == 'prep':
                    arxiv_url = '#'
                    alink = False
                    slink = False
                    preplink = True
                    year = '2018'
                    kind = "Finishing"
                    pdf_link = False
                    pdf_url = '#'

            temp = {}
            temp['title'] = get_title(et)
            short, long = get_authors(et)
            temp['authors'] = short
            temp['authors_long'] = long
            temp['arxiv'] = arxiv
            temp['year'] = year
            temp['url'] = url
            temp['doi'] = doi
            temp['arxiv_link'] = alink
            temp['doi_link'] = doilink
            temp['soft_link'] = slink
            temp['ads_link'] = adslink
            temp['prep_link'] = preplink
            temp['journal'] = journal
            temp['pages'] = pages
            temp['arxiv_url'] = arxiv_url
            temp['kind'] = kind
            temp['pdf_link'] = pdf_link
            temp['pdf_url'] = pdf_url
            texline = r'\cvline{}{$\bullet $'
            if pdf_link:
                texline += r' '+short+', \\textit{``{{'+get_title(et)+'}}\'\'}, '
                if doilink:
                    texline += r'{\color{blue}\href{'+url+'}{'+journal+', '+pages+'}}'
                else:
                    texline += r'{\color{blue}\href{'+url+'}{'+journal+':'+arxiv+'}}'
                texline += r' ('+year+')}\\\\[1pt]'
                if texline.find('Carrasco Kind') > -1:

                    texline = texline.replace('M. Carrasco Kind', '\\textbf{M. Carrasco Kind}')
                    texmine.append(texline)
                else:
                    texall.append(texline)
                if short.find('Carrasco Kind') > -1:
                    datamine.append(temp)
                if arxiv in ['1801.03181']:
                    datamine.append(temp)
            data.append(temp)
        temp2['papers'] = data
        Alldata.append(temp2)
    json.dump(Alldata, out, indent=4)

Alldatamine.append({'papers': datamine})
with open(os.path.join(ROOT, 'publications_sel.json'), 'w') as out:
    json.dump(Alldatamine, out, indent=4)
    Fmine = open(os.path.join('/home/matias/', 'Dropbox/CV/ingles/mine_bibs.tex'), 'w')
    Fall = open(os.path.join('/home/matias', 'Dropbox/CV/ingles/all_bibs.tex'), 'w')
    for line in texmine:
        Fmine.write(line+'\n')
    Fmine.close()
    for line in texall:
        Fall.write(line+'\n')
    Fall.close()
