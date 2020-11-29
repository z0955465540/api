user = {
            'name':'123',
            'gender':'123'
        }
query = []

for key, value in user.items():
    if value != None:
        query.append(key + ' = ' + "' {} '".format(value))
    query = ','.join(query)
    sql = """ Updata API.users Set {} where id = "{}" """.format(query, id)
    result = cursor.execute(sql)
    db.commit()
    db.close()
    response = {
        'result':True
    }
    return jsonify(response)
