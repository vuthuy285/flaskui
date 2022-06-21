import hashlib
# passwd = "nhung1234"
# hash_p1=hashlib.sha1(passwd.encode('utf-8')).hexdigest()       
# print(hash_p1)


passwd = ["admin1234", "nhung1234","duong1234", "Thao123", "An123", "Giang1234", "Bao123", "Dung123", "Tinh123", "Hai123", "huong1234", "Thuc123", "trong1234"  ]
for p in passwd:
    passwd=hashlib.sha1(p.encode('utf-8')).hexdigest()
    print(passwd)  

# passwd = ["admin1234", "nhung1234","duong1234", "Thao123", "An123", "Giang1234", "Bao123", "Dung123", "Tinh123", "Hai123", "huong1234", "Thuc123", "trong1234"  ]
# for p in passwd:
#     passwd=hashlib.md5(p.encode('utf-8')).hexdigest()
#     print(passwd)  

# passwd=hashlib.new('md5', "querty".encode('utf-8'))
# print(passwd.hexdigest())  

# passwd = " 'or 1=1; shutdown-- "
# passwd=passwd.replace("--", " ")
# passwd=passwd.replace(";", " ")
# passwd=passwd.replace("'", " ")
# print(passwd)

# print(hashlib.algorithms_available)
# print(hashlib.algorithms_guaranteed)