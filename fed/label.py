from itertools import islice
import re
import glob
import os.path
import pandas as pd
import pyarrow as pa

label = {}
documents = []

def record_type(value, key, dict=label):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]


for file in glob.glob("./fedminutes/monetary*"):
    N=10
    with open(file) as myfile:
        headN = list(islice(myfile, N))
    filename = os.path.basename(file)
    documents.append(filename)
    # if 'pdf' in filename:
    #     if 'monetary' in filename:
    #         record_type(filename, 'y'+filename[-18:-14])
    # elif 'monetary' in filename:
    record_type(filename, 'zy'+filename[8:12])
    mm = filename[12:14]
    record_type(filename, 'zm'+mm)

    def grep(phrase, headN = headN):
        return list(filter(lambda x: re.search(phrase, x), headN))
        # return [line for line in headN if phrase in line]


    if grep(r'^Federal Reserve issues FOMC statement$'): # statement
        record_type(filename, 'statement')
    elif grep(r'^DISCOUNT AND ADVANCE [\s]*RATES -'): # discount_rates
        record_type(filename, 'discount_rates')
    elif grep(r'MONETARY POLICY IMPLEMENTATION -- Rates '): # discount_rates
        record_type(filename, 'discount_rates')
    elif grep(r'^Federal Reserve Board approves [\sA-Za-z]*action[s]* by the '): # approval
        record_type(filename, 'approval')
    elif grep(r'^Approval of the discount rate action of the '):  # approval
        record_type(filename, 'approval')
    elif grep(r'^Approval of the discount rate requests of the '):  # approval
        record_type(filename, 'approval')
    elif grep(r'^Minutes of the Federal Open Market Committee$'): # minutes
        record_type(filename, 'minutes')
    elif grep(r'^Statement Regarding '): # statement
        record_type(filename, 'statement')
    elif grep(r'^Federal Reserve[to\s]*offer[s]* '): # offer, tender announcement
        record_type(filename, 'tender')
    elif grep(r'^Federal Reserve[will\s]*offer[s]* '): # offer, tender announcement
        record_type(filename, 'tender')
    elif grep(r'^Federal Reserve[will\s]*conduct [\sA-Za-z0-9-]*auction'): # offer, tender announcement
        record_type(filename, 'tender')
    elif grep('^Federal Reserve announces results of offering '): # offer_auction results
        record_type(filename, 'tender_results')
    elif grep('^Federal Reserve announces [\sA-Za-z0-9_-]*results of auction '):  # offer_auction results
        record_type(filename, 'tender_results')
    elif grep(' tentative [\sA-Za-z0-9_-]*meeting schedule'): # schedule
        record_type(filename, 'schedule')
    elif grep('publish Monetary Policy Report to the Congress '): # congress
        record_type(filename, 'congress')
    elif grep('Term Deposit Facility') or grep(' TDF '): # tdf
        record_type(filename, 'tdf')
    elif grep(r' (?i)normalization '):
        record_type(filename, 'normalization')
    elif grep('(?i)economic projection'): # project
        record_type(filename, 'projection')
    elif grep(' swap '): # swap
        record_type(filename, 'swap')
    elif grep('(?i)talf'): # talf
        record_type(filename, 'talf')
    elif grep(r'goals and policy strategy'): # goal
        record_type(filename, 'goals')
    elif grep(r'FOMC statement'): # statement
        record_type(filename, 'statement')
    elif grep(r' meeting of the Federal Open Market Committee '): # minutes
        record_type(filename, 'minutes')
    elif grep('^Minutes of [the\s]*Federal Open Market Committee'): # minutes
        record_type(filename, 'minutes')
    elif grep(r' global [\sA-Za-z0-9_-]*markets'): # global
        record_type(filename, 'global')
    elif grep(r' liquidity '): # liquidity
        record_type(filename, 'liquidity')
    else:
        record_type(filename, 'unknown')



labeldf={}
for labeltype in sorted(label):
    label_exists = []
    labelset = set(label[labeltype])
    for doc in documents:
        if doc in labelset:
            label_exists.append(1)
        else:
            label_exists.append(0)
    labeldf[labeltype] = list(label_exists)
labeldf['doc'] = documents
# print(labeldf)
df=pd.DataFrame(labeldf)
df.to_csv("./label.csv")
print(df.head().T)