import sys, os, base64, requests, json


def get_auth_header ():
    username = 'openskykcapi'
    password = 'W!n+er5now#'
    auth_string = '{}:{}'.format(username, password)
    auth_base64 = base64.b64encode(auth_string)

    return 'Basic %s' % auth_base64



# sponsor_award_id = '2019-05'
# sponsor_award_id = '001379-00001'
# sponsor_award_id = 'DE-SC0012711'
# sponsor_award_id = '711'
# sponsor_award_id = 'SC0012711'


def check_award_id (sponsor_award_id):

    base_url = 'http://fatomcat-test.fin.ucar.edu:8081/kualiapi/awardsbysponsorawardid'

    params = {
        'sponsorAwardId' : sponsor_award_id
    }

    headers = {
        'Authorization': get_auth_header()
    }

    resp = requests.get(base_url, params=params, headers=headers)

    print json.dumps(resp.json(), indent=4)

    data = resp.json()
    if type(data) == type([]) and len(data) == 1:
        data = data[0]
    if type(data) == type({}):  # single result
        # print json.dumps(resp.json(), indent=4)
        if data['awardId'] is None:
            return 0
        else:
            return 1
    else:
        print 'there are %d results' % len (data)
        print json.dumps(data, indent=4)
        return 0

if __name__ == '__main__':
    award_ids = [
        # 'AGS-1762096',
        # 'NNX14AH54G', 'NNH12ZDA001N',
        # 'NA15OAR4310099', 'NA13OAR431009',
        # 'DE-FG02-94ER61937', 'DE-SC0012778',
        # 'FA9550-16-1-0050' # yes

        'FA9550-16-1-0050',
        ]

    for id in award_ids:
        print '- {} - {}'.format(id, check_award_id(id) and 'YES' or 'No')

