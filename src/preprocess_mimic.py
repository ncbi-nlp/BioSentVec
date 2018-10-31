import re

from nltk import sent_tokenize, word_tokenize

SECTION_TITLES = re.compile(
    r'('
    r'ABDOMEN AND PELVIS|CLINICAL HISTORY|CLINICAL INDICATION|COMPARISON|COMPARISON STUDY DATE'
    r'|EXAM|EXAMINATION|FINDINGS|HISTORY|IMPRESSION|INDICATION'
    r'|MEDICAL CONDITION|PROCEDURE|REASON FOR EXAM|REASON FOR STUDY|REASON FOR THIS EXAMINATION'
    r'|TECHNIQUE'
    r'):|FINAL REPORT',
    re.IGNORECASE | re.MULTILINE)


def pattern_repl(matchobj):
    """
    Return a replacement string to be used for match object
    """
    s = matchobj.group(0).lower()
    return ' '.rjust(len(s))


def sub(text):
    """
    Replace [**Patterns**] with spaces.
    Replace `_` with spaces.
    """
    text = re.sub(r'\[\*\*.*?\*\*\]', pattern_repl, text)
    text = re.sub(r'_', ' ', text)
    return text


def find_end(text):
    """Find the end of the report."""
    ends = [len(text)]
    patterns = [
        re.compile(r'BY ELECTRONICALLY SIGNING THIS REPORT', re.I),
        re.compile(r'\n {3,}DR.', re.I),
        re.compile(r'[ ]{1,}RADLINE ', re.I),
        re.compile(r'.*electronically signed on', re.I),
        re.compile(r'M\[0KM\[0KM')
    ]
    for pattern in patterns:
        m = pattern.search(text)
        if m:
            ends.append(m.start())
    return min(ends)


def split_heading(text):
    """Split the report into sections"""
    start = 0
    for matcher in SECTION_TITLES.finditer(text):
        # add last
        end = matcher.start()
        if end != start:
            t = text[start:end].strip()
            if t:
                yield t

        # add title
        start = end
        end = matcher.end()
        if end != start:
            t = text[start:end].strip()
            if t:
                yield t

        start = end

    # add last piece
    end = len(text)
    if start < end:
        t = text[start:end].strip()
        if t:
            yield t


def trim(text):
    # Replace [**Patterns**] with spaces.
    text = re.sub(r'\[\*\*.*?\*\*\]', pattern_repl, text)
    # Replace `_` with spaces.
    text = re.sub(r'_', ' ', text)

    start = 0
    end = find_end(text)
    new_text = ''
    if start > 0:
        new_text += ' ' * start
    new_text = text[start:end]

    # make sure the new text has the same length of old text.
    if len(text) - end > 0:
        new_text += ' ' * (len(text) - end)
    return new_text


def preprocess_mimic(text):
    """
    Preprocess reports in MIMIC-III.
    1. Remove [**Patterns**] and signature
    2. Split the report into sections
    3. Sentence and word tokenization
    4. lowercase
    """
    for sec in split_heading(trim(text)):
        for sent in sent_tokenize(sec):
            text = ' '.join(word_tokenize(sent))
            yield text.lower()


def preprocess_pubmed(text):
    """
    Preprocess PubMed abstract. (https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PubMed/)
    1. Sentence and word tokenization
    2. lowercase
    """
    for sent in sent_tokenize(text):
        text = ' '.join(word_tokenize(sent))
        yield text.lower()


def test_preprocess_mimic():
    text = """Normal sinus rhythm. Right bundle-branch block with secondary ST-T wave
    abnormalities. Compared to the previous tracing of [**2198-5-26**] no diagnostic
    interim change.

    """
    sents = [sen for sen in preprocess_mimic(text)]
    assert sents[0] == 'normal sinus rhythm .'
    assert sents[1] == 'right bundle-branch block with secondary st-t wave abnormalities .'
    assert sents[2] == 'compared to the previous tracing of no diagnostic interim change .'


def test_preprocess_pubmed():
    # from https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pubmed.cgi/BioC_xml/30096728/ascii

    text = """A novel chiral porous-layer stationary phase was developed for use in open-tubular 
    nano liquid chromatography. The stationary phase was prepared by an in-situ polymerization of 
    3-chloro-2-hydroxypropylmethacrylate (HPMA-Cl) and ethylene dimethacrylate (EDMA). The reactive
     chloro groups at the surface of the porous stationary phase were reacted with 
     beta-Cyclodextrin (beta-CD). """
    sents = [sen for sen in preprocess_pubmed(text)]
    assert sents[2] == 'the reactive chloro groups at the surface of the porous stationary phase' \
                       ' were reacted with beta-cyclodextrin ( beta-cd ) .'
