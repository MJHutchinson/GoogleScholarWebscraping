#!/usr/bin/env python
# coding: utf-8

# In[35]:


import requests
from bs4 import BeautifulSoup
import pprint


# In[36]:


p = pprint.PrettyPrinter(indent=4)


# In[37]:


scholar_href = 'https://scholar.google.com'
root_paper = '/scholar?hl=en&as_sdt=2005&sciodt=0,5&cites=14542735200645169180&scipsc='


# In[38]:


db = {}


# In[39]:


wuinn = {
    'title': 'Weight uncertainty in neural networks',
    'pdf_link': 'https://arxiv.org/pdf/1505.05424.pdf',
    'page_link': 'https://arxiv.org/abs/1505.05424',
    'authors': [],
    'short_abstract': 'We introduce a new, efficient, principled and backpropagation-compatible algorithm for learning a probability distribution on the weights of a neural network, called Bayes by Backprop. It regularises the weights by minimising a compression cost, known as the',
    'cited_by_link': '/scholar?cites=14542735200645169180&as_sdt=2005&sciodt=0,5&hl=en',
    'related_articles_link': '/scholar?q=related:HEAGQZ0s0skJ:scholar.google.com/&scioq=&hl=en&as_sdt=0,5',
    'cited_by': [],
    'cites': [],
    'tree_level': 0,
    'forward_pass_done': False
}


# In[41]:


db['Weight uncertainty in neural networks'] = wuinn


# In[42]:


citation_class = 'gs_r gs_or gs_scl'
title_class = 'gs_rt'
author_class = 'gs_a'
abstract_class = 'gs_rs'
meta_info_class = 'gs_fl'


# In[43]:


def process_paper(paper):
    children = list(paper.children)
    
    if len(children) == 1:
        pdf_link=""
        body = children[0]
    else:
        pdf_link = children[0].find('a')['href']
        body = children[1]
        
    if len(list(body.children))<4: return None
        
    page_link = body.find(class_=title_class).find('a')['href']
    title = body.find(class_=title_class).find('a').get_text()
    author_list = body.find(class_=author_class).find_all('a')
    if len(author_list) == 0:
        authors = []
    else:
        authors = [(a.get_text(), a['href'].split('=')[1].split('&')[0]) for a in author_list]
    short_abstract = body.find(class_=abstract_class).get_text()
    meta = list(body.find(class_=meta_info_class).find_all('a'))
    if (len(meta) == 8) | (len(meta) == 7):
        cited_by_link = meta[2]['href']
        related_articles_link = meta[3]['href']
    else:
        cited_by_link = ''
        related_articles_link = ''
        
    
    return {
        'title': title,
        'pdf_link': pdf_link,
        'page_link': page_link,
        'authors': authors,
        'short_abstract': short_abstract,
        'cited_by_link': cited_by_link,
        'related_articles_link': related_articles_link,
        'cited_by': [],
        'cites': []
    }


# In[44]:


def get_citations(paper):
    start = 0
    title = paper['title']
    citation_list = []
    citation_url = paper['cited_by_link']
    tree_level = paper['tree_level']

    while True:
        url = f'{scholar_href}{citation_url}&start={start}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        citations = soup.find_all('div', class_=citation_class)
        if(len(citations)) == 0: break

        papers = [process_paper(p) for p in citations if p is not None]
        papers_strip = [p for p in papers if p is not None]
        for p in papers_strip:
            p['level'] = tree_level+1

        start += len(papers)
        citation_list.extend(papers_strip)
        print(f'\rCollected {start} papers for {title}', end='')
        
    print(f'\rFinished with {title}')
    return citation_list


citations_of_paper = get_citations(wuinn)

print(citations_of_paper)




