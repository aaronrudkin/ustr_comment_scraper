import pprint
import os
import time
import requests
import json
import pandas as pd
import tqdm

params = {
    'aura.ApexAction.execute': '1',
}

12345678901234567890123456789012345678901234567890123456789012345678901234567890
# Dockets were obtained by scraping the main USTR list page; the reason this is
# not implemented as a requests based scraper is because populating the docket
# list is a bit of a pain, and even once loaded, the nodes are in the "shadow
# DOM" so traditional Selenium scraping approaches don't work well. Anyway,
# this is all the dockets available.
all_dockets = ['https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0020', 'https://comments.ustr.gov/portal/s/submitnewcomment?docketNumber=USTR-2024-0020', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0025', 'https://comments.ustr.gov/s/submit-new-comment?docketNumber=USTR-2024-0025', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0024', 'https://comments.ustr.gov/s/submit-new-comment?docketNumber=USTR-2024-0024', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0021', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0022', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0016', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0007', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0005', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0004', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2024-0001', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2023-0001', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2022-0014', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2022-0009', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2022-0007', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2022-0001', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0019', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2019-0017', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0010', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0003', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0006', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0002', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0004', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0005', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0007', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0008', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0002-Hearing', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0003-Hearing', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0004-Hearing', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0005-Hearing', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0007-Hearing', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0006-Hearing', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2021-0008-Hearing', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0027', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0030', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0031', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0029', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0026', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0023', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0016', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0021', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0015', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0018', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0017', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2020-0013', 'https://comments.ustr.gov/s/docket?docketNumber=USTR-2019-0005']
all_dockets = list(set([x.split("=", 1)[1] for x in all_dockets]))

def docket_get_count(docket_id):
    data = {
        'message': '{"actions":[{"id":"82;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"UstrfbExclusionRequestListController","method":"getUnfilteredRecordCount","params":{"docketNumber":"' + docket_id + '"},"cacheable":false,"isContinuation":false}}]}',
        'aura.context': '{"mode":"PROD","fwuid":"eUNJbjV5czdoejBvRlA5OHpDU1dPd1pMVExBQkpJSlVFU29Ba3lmcUNLWlE5LjMyMC4y","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"1184_AgcTXn_6dZSShHXZ2PZsug","MODULE@markup://lightning:f6Controller":"300_MTpiBnsQUPWZH6VdweEpwA","COMPONENT@markup://instrumentation:o11ySecondaryLoader":"343_75unE-CE7CDfRvzL8FM_Uw"},"dn":[],"globals":{},"uad":false}',
        'aura.pageURI': f'/s/docket?docketNumber={docket_id}',
        'aura.token': 'null',
    }
    res = requests.post('https://comments.ustr.gov/s/sfsites/aura', params=params, data=data, timeout=10)
    d = json.loads(res.text)
    return int(d["actions"][0]["returnValue"]["returnValue"])

def docket_get_offset(docket_id, previous_fsv, previous_fi):
    print("Checking offset...")
    previous_fsv = r'\"' + previous_fsv + r'\"' if previous_fsv != "null" and not previous_fsv.startswith(r'\"') else previous_fsv

    data = {
        'message': '{"actions":[{"id":"84;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"UstrfbExclusionRequestListController","method":"getOffset","params":{"selectorJSON":"{\\"docketNumber\\":\\"' + docket_id + '\\",\\"filterString\\":\\"\\",\\"sortField\\":\\"Random_URL_Code__c\\",\\"contentFieldReferenceId\\":null,\\"sortDirection\\":\\"asc\\",\\"pageSize\\":\\"50\\",\\"previousFinalSortValue\\":' + previous_fsv + ',\\"previousFinalIndex\\":' + str(previous_fi) + '}"},"cacheable":false,"isContinuation":false}}]}',
        'aura.context': '{"mode":"PROD","fwuid":"eUNJbjV5czdoejBvRlA5OHpDU1dPd1pMVExBQkpJSlVFU29Ba3lmcUNLWlE5LjMyMC4y","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"1184_AgcTXn_6dZSShHXZ2PZsug","MODULE@markup://lightning:f6Controller":"300_MTpiBnsQUPWZH6VdweEpwA","COMPONENT@markup://instrumentation:o11ySecondaryLoader":"343_75unE-CE7CDfRvzL8FM_Uw"},"dn":[],"globals":{},"uad":false}',
        'aura.pageURI': f'/s/docket?docketNumber={docket_id}',
        'aura.token': 'null',
    }
    res = requests.post('https://comments.ustr.gov/s/sfsites/aura', params=params, data=data, timeout=10)
    d = json.loads(res.text)
    try:
        rv = d["actions"][0]["returnValue"]["returnValue"]
    except:
        import pdb
        import pprint
        pprint.pprint(data)
        pdb.set_trace()
        return -1, -1
    return rv["finalSortValue"], rv["finalIndex"]

def docket_get_comments(docket_id, max_id):
    results = None
    min_id = 0
    previous_fsv = "null"
    previous_fi = "null"
    while min_id < max_id:
        end_id = min(min_id + 50, max_id)
        offset_min_id = min_id % 8000
        offset_end_id = end_id % 8000 if end_id % 8000 != 0 else 8000
        if min_id % 8000 == 0 and min_id:
            previous_fsv, previous_fi = docket_get_offset(docket_id, previous_fsv, previous_fi)
            if previous_fi == -1:
                return
            previous_fsv = r'\"' + previous_fsv + r'\"' if previous_fsv != "null" and not previous_fsv.startswith('"') else previous_fsv
            print(previous_fsv)

        print(f"\tPage beginning with result {min_id} through to {end_id}")
        data = {
            'message': '{"actions":[{"id":"85;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"UstrfbExclusionRequestListController","method":"getPageRecords","params":{"selectorJSON":"{\\"docketNumber\\":\\"' + docket_id + '\\",\\"filterString\\":\\"\\",\\"sortField\\":\\"Random_URL_Code__c\\",\\"contentFieldReferenceId\\":null,\\"sortDirection\\":\\"asc\\",\\"pageSize\\":\\"50\\",\\"previousFinalSortValue\\":' + previous_fsv + ',\\"previousFinalIndex\\":' + str(previous_fi) + ',\\"startIndex\\":' + str(offset_min_id) + ',\\"endIndex\\":' + str(offset_end_id) + '}"},"cacheable":false,"isContinuation":false}}]}',
            'aura.context': '{"mode":"PROD","fwuid":"eUNJbjV5czdoejBvRlA5OHpDU1dPd1pMVExBQkpJSlVFU29Ba3lmcUNLWlE5LjMyMC4y","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"1184_AgcTXn_6dZSShHXZ2PZsug","MODULE@markup://lightning:f6Controller":"300_MTpiBnsQUPWZH6VdweEpwA","COMPONENT@markup://instrumentation:o11ySecondaryLoader":"343_75unE-CE7CDfRvzL8FM_Uw"},"dn":[],"globals":{},"uad":false}',
            'aura.pageURI': f'/s/docket?docketNumber={docket_id}',
            'aura.token': 'null',
        }
        error_count = 0
        while error_count < 20:
            try:
                res = requests.post('https://comments.ustr.gov/s/sfsites/aura', params=params, data=data, timeout=20)
                error_count = 0
                break
            except:
                print("Timeout!")
                time.sleep(5 * (error_count + 1))
            error_count = error_count + 1
        if error_count:
            print(f"DID NOT COMPLETE, stopped at {min_id}")
            return results

        print("Page load done")
        d = json.loads(res.text)
        rdf = pd.DataFrame.from_records(d["actions"][0]["returnValue"]["returnValue"])

        if min_id:
            results = pd.concat([results, rdf])
        else:
            results = rdf

        print(f"Total comments gathered is now {results.shape[0]}")

        min_id = min_id + 50

    return results

def write_docket(docket_id):
    if os.path.isfile(f"dockets/{docket_id}.csv"):
        return

    max_num = docket_get_count(docket_id)
    print(f"Docket {docket_id} max {max_num}")
    results = docket_get_comments(docket_id, max_num)
    try:
        print(f"Docket has {results.shape[0]} rows")
    except:
        print("Catastrophic failure....")
        return
    results.to_csv(f'dockets/{docket_id}.csv', index=False)

def do_all_dockets(dockets):
    os.makedirs("dockets/", exist_ok=True)
    for x in tqdm.tqdm(dockets):
        os.makedirs(f"dockets/{x}", exist_ok = True)
        write_docket(x)
        all_comments_from_docket(x)

def all_comments_from_docket(docket_id):
    try:
        df = pd.read_csv(f"dockets/{docket_id}.csv")
    except:
        return
    print(f"Pulling comments for docket {docket_id}")
    os.makedirs(f"dockets/{docket_id}", exist_ok=True)
    for comment_id in tqdm.tqdm(df["Random_URL_Code__c"]):
        pull_comment(docket_id, comment_id)

def pull_comment(docket_id, comment_id):
    if os.path.isfile(f"dockets/{docket_id}/{comment_id}.json"):
        return

    p2 = {'aura.ApexAction.execute': '4'}
    data = {
        'message': '{"actions":[{"id":"67;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"UstrfbPublicDetailsReviewPageAuraService","method":"getContentFields","params":{"referenceCode":"' + comment_id + '"},"cacheable":false,"isContinuation":false}},{"id":"68;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"UstrfbDisplayRepeatingRecordsController","method":"getRecordIdFromRandomUrlCodeOrId","params":{"rid":"' + comment_id + '"},"cacheable":false,"isContinuation":false}},{"id":"69;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"UstrfbPublicDocketCommentRefCtrl","method":"getPublicCommentReferences","params":{"commentReferenceCode":"' + comment_id + '"},"cacheable":false,"isContinuation":false}},{"id":"70;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"UstrPublicDocketCommentAttachController","method":"getAttachments","params":{"exclusionReferenceCode":"' + comment_id + '"},"cacheable":false,"isContinuation":false}}]}',
        'aura.context': '{"mode":"PROD","fwuid":"eUNJbjV5czdoejBvRlA5OHpDU1dPd1pMVExBQkpJSlVFU29Ba3lmcUNLWlE5LjMyMC4y","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"1184_AgcTXn_6dZSShHXZ2PZsug"},"dn":[],"globals":{},"uad":false}',
        'aura.pageURI': f'/s/commentdetails?rid={comment_id}',
        'aura.token': 'null',
    }

    try:
        res = requests.post('https://comments.ustr.gov/s/sfsites/aura', params=p2, data=data, timeout=30)
        d = json.loads(res.text)
    except:
        return

    with open(f"dockets/{docket_id}/{comment_id}.json", "w") as outfile:
        json.dump(d["actions"][0]["returnValue"]["returnValue"], outfile)

if __name__ == "__main__":
    do_all_dockets(all_dockets)
