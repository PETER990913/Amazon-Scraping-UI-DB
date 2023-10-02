import mysql.connector
import json

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)

# Check if connection was successful
if mydb.is_connected():
    print("Connected to MySQL database")

# Create a cursor object to execute SQL queries


def save_into_database():
    with open('data/pbn_domaininfos.txt', 'r') as file1, open('data/pbn_domainnames.txt', 'r') as file2:
        for line1, line2 in zip(file1, file2):
            # Do something with line1 and line2
            item = json.loads(line1.strip())
            domain_name = line2.strip()

            # Execute the SQL query to select the row with domain equals admin
            select_sql = "SELECT id FROM pbns WHERE domain = %s"
            mycursor = mydb.cursor()
            mycursor.execute(select_sql, (domain_name,))

            # Fetch the result of the query
            results = mycursor.fetchall()
            mycursor.close()

            if (len(results) != 0):
                id = results[0][0]
                update_sql = "UPDATE pbns SET domain=%s, added_date=%s, page_rank=%s, google_index=%s, traffic=%s, lang=%s, age=%s, r_ip=%s, rd=%s, tf=%s, cf=%s, bl=%s, spams=%s, expiration_date=%s, topicals=%s, efferings=%s, historical_keywords=%s, screenshots=%s WHERE id=%s;"
                update_values = [domain_name, item['added_date'],  item['page_rank'], item['google_index'], item['traffic'], item['lang'], item['age'], item['r_ip'], item['rd'], item['tf'], item['cf'], item['bl'], json.dumps(
                    item['spams']), item['expiration_date'], json.dumps(item['topicals']), json.dumps(item['efferings']), json.dumps(item['historical_keywords']), json.dumps(item['screenshots']), id]
                try:
                    mycursor1 = mydb.cursor()
                    mycursor1.execute(update_sql, update_values)
                    # Commit changes to the database
                    mydb.commit()
                    print(mycursor.rowcount, "rows were updated.")
                except:
                    print("error")
            else:
                insert_sql = "INSERT INTO pbns (domain, added_date, page_rank, google_index, traffic, lang, age, r_ip, rd, tf, cf, bl, spams, expiration_date, topicals, efferings,  historical_keywords, screenshots) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                insert_values = [domain_name, item['added_date'],  item['page_rank'], item['google_index'], item['traffic'], item['lang'], item['age'], item['r_ip'], item['rd'], item['tf'], item['cf'], item['bl'], json.dumps(
                    item['spams']), item['expiration_date'], json.dumps(item['topicals']), json.dumps(item['efferings']), json.dumps(item['historical_keywords']), json.dumps(item['screenshots'])]
                try:
                    mycursor2 = mydb.cursor()
                    mycursor2.execute(insert_sql, insert_values)
                    mydb.commit()
                    print(mycursor.rowcount, "rows were inserted.")
                except:
                    print("error")

    file1.close()
    file2.close()


def main():
    # create_table()

    save_into_database()
    status_file = open('data/pbn_status.txt', 'w')
    status_file.write("success")
    print("Saved Success")
    # setStatus(False)


if __name__ == '__main__':
    main()
