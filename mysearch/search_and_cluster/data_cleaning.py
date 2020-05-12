import numpy as np
import pandas as pd
import re


def data_loader(file_path):
    data = pd.read_csv(file_path)
    return data

# # data preprocessing (removing common words, dropping missing values, filling nulls)
_display_clos = ['paper_id', 'title', 'authors', 'abstract', 'text']
_abstract_terms_ = '(Publisher|Abstract|Summary|BACKGROUND|INTRODUCTION)'
_relevant_re_ = '.*vir.*|.*sars.*|.*mers.*|.*corona.*|.*ncov.*|.*immun.*|.*nosocomial.*' # keep relevant terms in title
_relevant_re_ = _relevant_re_ + '.*epidem.*|.*emerg.*|.*vacc.*|.*cytokine.*'


def remove_common_terms(abstract):
    return re.sub(_abstract_terms_, '', abstract)


def start(data):
    return data.copy()


def clean_title(data):
    # Set junk titles to NAN
    title_relevant = data.title.fillna('').str.match(_relevant_re_, case=False)
    title_short = data.title.fillna('').apply(len) < 30
    title_junk = title_short & ~title_relevant # ~, bitwise not
    data.loc[title_junk, 'title'] = ''
    return data


def show_common(data, column):
    common_column = data[column].value_counts().to_frame()
    common_column = common_column[common_column[column] > 1]
    return common_column


def clean_abstract(data):
    # Fill missing abstract with the title
    data.abstract = data.abstract.fillna(data.title)

    # Remove common terms like publisher
    data.abstract = data.abstract.apply(remove_common_terms)

    # Remove the abstract if it is too common
    common_abstracts = show_common(data, 'abstract').query('abstract > 2').reset_index().query('~(index =="")')['index'].tolist()
    data.loc[data.abstract.isin(common_abstracts), 'abstract'] = ''
    return data


def drop_missing(data):
    missing = (data.paper_id.isnull()) & (data.title == '') & (data.abstract == '')
    return data[~missing].reset_index(drop=True)


def fill_nulls(data):
    data.title = data.title.fillna('')
    data.authors = data.authors.fillna('')
    data.abstract = data.abstract.fillna('')
    return data

