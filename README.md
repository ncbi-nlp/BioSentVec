# BioWordVec & BioSentVec: <br><small>pre-trained embeddings for biomedical words and sentences</small>

[![HitCount](https://hits.dwyl.com/ncbi-nlp/BioSentVec.svg)](https://hits.dwyl.com/ncbi-nlp/BioSentVec)

## Table of contents

* [Text corpora](#text-corpora)
* [BioWordVec: biomedical word embeddings with fastText](#biowordvec)
* [BioSentVec: biomedical sentence embeddings with sent2vec](#biosentvec)
* [FAQ](#faq)
* [References](#references)
* [Acknowledgments](#acknowledgments)


## Text corpora
We created biomedical word and sentence embeddings using [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) and the clinical notes from [MIMIC-III Clinical Database](https://physionet.org/works/MIMICIIIClinicalDatabase/access.shtml). Both PubMed and MIMIC-III texts were split and tokenized using [NLTK](https://www.nltk.org/). We also lowercased all the words. The statistics of the two corpora are shown below.

| Sources | Documents | Sentences | Tokens |
| :------ | --------: | --------: | -----: |
| PubMed | 28,714,373 | 181,634,210 | 4,354,171,148 |
| MIMIC III Clinical notes | 2,083,180 | 41,674,775 | 539,006,967 |


## <a name="biowordvec">BioWordVec [1]: biomedical word embeddings with fastText</a>

We applied [fastText](https://fasttext.cc/) to compute 200-dimensional word embeddings. We set the window size to be 20, learning rate 0.05, sampling threshold 1e-4, and negative examples 10. Both the word vectors and the model with hyperparameters are available for download below. The model file can be used to compute word vectors that are not in the dictionary (i.e. out-of-vocabulary terms). This work extends the original [BioWordVec](https://github.com/ncbi-nlp/BioWordVec) which provides fastText word embeddings trained using PubMed and MeSH. We used the same parameters as the original BioWordVec which has been thoroughly evaluated in a range of applications.

* [BioWordVec vector](https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/BioSentVec/BioWordVec_PubMed_MIMICIII_d200.vec.bin) 13GB (200dim, trained on PubMed+MIMIC-III, word2vec bin format)
* [BioWordVec model](https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/BioSentVec/BioWordVec_PubMed_MIMICIII_d200.bin) 26GB (200dim, trained on PubMed+MIMIC-III)

We evaluated BioWordVec for medical word pair similarity. We used the MayoSRS (101 medical term pairs; download [here](http://rxinformatics.umn.edu/data/MayoSRS.csv)) and UMNSRS_similarity (566 UMLS concept pairs; download [here](http://rxinformatics.umn.edu/SemanticRelatednessResources.html)) datasets.

| Model | MayoSRS | UMNSRS_similarity |
| :---- | ------: | ----------------: |
| word2vec | 0.513 | 0.626 |
| BioWordVec model | 0.552 | 0.660 |

## <a name="biosentvec"> BioSentVec [2]: biomedical sentence embeddings with sent2vec</a>

We applied [sent2vec](https://github.com/epfml/sent2vec) to compute the 700-dimensional sentence embeddings. We used the bigram model and set window size to be 20 and negative examples 10.

* [BioSentVec model](https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/BioSentVec/BioSentVec_PubMed_MIMICIII-bigram_d700.bin) 21GB (700dim, trained on PubMed+MIMIC-III)

We evaluated BioSentVec for clinical sentence pair similarity tasks. We used the BIOSSES (100 sentence pairs; download [here](http://tabilab.cmpe.boun.edu.tr/BIOSSES/DataSet.html)) and the MedSTS (1068 sentence pairs; download [here](https://arxiv.org/ftp/arxiv/papers/1808/1808.09397.pdf)) datasets.

|                                                                             | BIOSSES     | MEDSTS      |
|-----------------------------------------------------------------------------|------------:|------------:|
| ***Unsupervised methods*** |
| &nbsp;&nbsp;&nbsp;&nbsp;[doc2vec](https://www.ncbi.nlm.nih.gov/pubmed/28881973) | 0.787 | - |
| &nbsp;&nbsp;&nbsp;&nbsp;[Levenshtein Distance](https://arxiv.org/abs/1808.09397) | - | 0.680 |
| &nbsp;&nbsp;&nbsp;&nbsp;[Averaged word embeddings](http://www.aclweb.org/anthology/W16-2922) | 0.694 | 0.747 |
| &nbsp;&nbsp;&nbsp;&nbsp;[Universal Sentence Encoder](https://arxiv.org/abs/1803.11175) | 0.345 | 0.714 |
| &nbsp;&nbsp;&nbsp;&nbsp;BioSentVec (PubMed) | **0.817** | 0.750 |
| &nbsp;&nbsp;&nbsp;&nbsp;BioSentVec (MIMIC-III) | 0.350 | 0.759 |
| &nbsp;&nbsp;&nbsp;&nbsp;BioSentVec (PubMed + MIMIC-III) | 0.795 | **0.767** |       
| ***Supervised methods***
| &nbsp;&nbsp;&nbsp;&nbsp;[Linear Regression](https://www.ncbi.nlm.nih.gov/pubmed/28881973) | 0.836 | - |
| &nbsp;&nbsp;&nbsp;&nbsp;[Random Forest](https://www.researchgate.net/publication/327402060_Combining_rich_features_and_deep_learning_for_finding_similar_sentences_in_electronic_medical_records) | - | 0.818 |
| &nbsp;&nbsp;&nbsp;&nbsp;Deep learning + [Averaged word embeddings](http://www.aclweb.org/anthology/W16-2922) | 0.703 | 0.784 |
| &nbsp;&nbsp;&nbsp;&nbsp;Deep learning + [Universal Sentence Encoder](https://arxiv.org/abs/1803.11175)       | 0.401 | 0.774 |
| &nbsp;&nbsp;&nbsp;&nbsp;Deep learning + BioSentVec (PubMed)                                      | 0.824 | 0.819 |
| &nbsp;&nbsp;&nbsp;&nbsp;Deep learning + BioSentVec (MIMIC-III)                                   | 0.353 | 0.805 |
| &nbsp;&nbsp;&nbsp;&nbsp;Deep learning + BioSentVec (PubMed + MIMIC-III)                          | **0.848** | **0.836** |

## FAQ

You can find [answers to frequently asked questions](https://github.com/ncbi-nlp/BioSentVec/wiki/) on our Wiki; e.g., you can find the instructions on how to load these models.

You can also find [this tutorial](https://github.com/ncbi-nlp/BioSentVec/blob/master/BioSentVec_tutorial.ipynb) on how to use BioSentVec for a quick start.

## References
When using some of our pre-trained models for your application, please cite the following papers:

1. Zhang Y, Chen Q, Yang Z, Lin H, Lu Z. [BioWordVec, improving biomedical word embeddings with subword information and MeSH](https://www.nature.com/articles/s41597-019-0055-0). Scientific Data. 2019.
2. Chen Q, Peng Y, Lu Z. [BioSentVec: creating sentence embeddings for biomedical texts](http://arxiv.org/abs/1810.09302). The 7th IEEE International Conference on Healthcare Informatics. 2019.

## Acknowledgments
This work was supported by the Intramural Research Programs of the National Institutes of Health, National Library of Medicine. We are grateful to the authors of fastText, sent2vec, MayoSRS, UMNSRS, BIOSSES, and MedSTS for making their software and data publicly available.
