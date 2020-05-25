challenge_list=[
        {
            'battle_id': 0,
            'behalf': None,
            'boss_num': 1,
            'challenge_pcrdate': 18407,
            'challenge_pcrtime': 56216,
            'challenge_time': 1590410216,
            'cycle': 1,
            'damage': 15000,
            'health_ramain': 5985000,
            'is_continue': False,
            'message': None,
            'qqid': 740984027
        },
        {
            'battle_id': 0,
            'behalf': None,
            'boss_num': 1,
            'challenge_pcrdate': 18407,
            'challenge_pcrtime': 56297,
            'challenge_time': 1590410297,
            'cycle': 1,
            'damage': 5985000,
            'health_ramain': 0,
            'is_continue': False,
            'message': '',
            'qqid': 740984027
        },
        {
            'battle_id': 0,
            'behalf': None,
            'boss_num': 2,
            'challenge_pcrdate': 18407,
            'challenge_pcrtime': 56321,
            'challenge_time': 1590410321,
            'cycle': 1,
            'damage': 21312,
            'health_ramain': 7978688,
            'is_continue': True,
            'message': '',
            'qqid': 740984027
        },
        {
            'battle_id': 0,
            'behalf': None,
            'boss_num': 2,
            'challenge_pcrdate': 18407,
            'challenge_pcrtime': 56356,
            'challenge_time': 1590410356,
            'cycle': 1,
            'damage': 213120,
            'health_ramain': 7765568,
            'is_continue': False,
            'message': '',
            'qqid': 740984027
        },
        {
            'battle_id': 0,
            'behalf': None,
            'boss_num': 2,
            'challenge_pcrdate': 18407,
            'challenge_pcrtime': 56356,
            'challenge_time': 1092669206,
            'cycle': 1,
            'damage': 213120,
            'health_ramain': 7765568,
            'is_continue': False,
            'message': '',
            'qqid': 1092669206
        },
        {
            'battle_id': 0,
            'behalf': None,
            'boss_num': 2,
            'challenge_pcrdate': 18407,
            'challenge_pcrtime': 56356,
            'challenge_time': 1092669206,
            'cycle': 1,
            'damage': 213120,
            'health_ramain': 7765568,
            'is_continue': False,
            'message': '',
            'qqid': 1092669206
        },
        {
            'battle_id': 0,
            'behalf': None,
            'boss_num': 2,
            'challenge_pcrdate': 18407,
            'challenge_pcrtime': 56356,
            'challenge_time': 1092669206,
            'cycle': 1,
            'damage': 213120,
            'health_ramain': 7765568,
            'is_continue': False,
            'message': '',
            'qqid': 1092669206
        }
    ]
member_list= [
        {
            'nickname': 'Scar',
            'qqid': 740984027,
            'sl': None
        },
        {
            'nickname': '工具人',
            'qqid': 1092669206,
            'sl': None
        },
        {
            'nickname': '可可萝',
            'qqid': 1453766088,
            'sl': None
        }
    ]

challenge={}
for item in member_list:
  challenge[item['qqid']] = 0

for item in challenge_list:
  if not item['is_continue']:
    challenge[item['qqid']] = challenge[item['qqid']]+1
  print(challenge)

non_record_qqid_list=[]
for key in challenge:
  if challenge[key] == 0:
    non_record_qqid_list.append(key) 

print(non_record_qqid_list)
print(challenge)

# print(challenge)

# member=[]
# for item in member_list:
#     member.append(item['qqid'])
# member.append(740984027)
# print(member)