import settings

con = settings.CONNECTION
c = con.cursor()
c.execute("show tables")
print("===========")
print(c.fetchall())
print("===========")
c.execute('insert into anime values (000000,"てすと","あばうとなあらすじ",000001,000002,000003,000004,000005,000006,"http://www.google.co.jp","http://www.yahoo.co.jp");')
c.execute('select * from anime')
for i in c.fetchall():
    print("ID:", i[0], "Title:", i[1], "About:", i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10])

con.commit()
c.close()
con.close()
