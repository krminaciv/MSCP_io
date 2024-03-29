def getKeysByValue(dictionary, search_value):
    matching_keys = []
    for key, value in dictionary.items():
        for i in value:
            if i == search_value:
                matching_keys.append(key)
    return matching_keys



def create_graph(fp):
     file_path = fp
     dict = {}

     try:
          with open(file_path, 'r') as file:
               for line in file:
                    key, value = line.split(' ', 1)
                    if key in dict:
                         dict[key].append(value.strip('\n'))
                    else:
                         dict[key] = [value.strip('\n')]
     except FileNotFoundError:
          print(f"File '{file_path}' not found.")
     except Exception as e:
          print("An error occurred:", e)
     

     for i in range(len(dict)):
          lista = getKeysByValue(dict, str(i))
          for l in lista:
               if l not in dict[str(i)]:
                    dict[str(i)].append(l)
     
     max_length = len(dict[max(dict, key=lambda key: len(dict[key]))])
     return dict


#print(create_graph("instances/male -50/queen5_5.txt"))