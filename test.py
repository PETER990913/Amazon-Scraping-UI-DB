import json
with open('musicalinstrument.json', 'r') as file:
    for line in file:
        # Do something with line1 and line2
        line_word = line.strip()
        print(line_word)
        # item = json.loads(line_word)                 
        if(line_word == "back"):
            pass   
        else:
            item = json.loads(line_word)
            item_text = item['name']
            item_link = item['link'] 
            print('item_text:', item_text) 
            print('item_link:', item_link) 
file.close()