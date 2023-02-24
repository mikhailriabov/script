
MAIN_FILE_NAME = "D327971_fc1.txt"
RESULT_FILE_NAME = "cnc.txt"

import re

# writing the result into the output file
def make_result_file(begin_list, t_list, end_list):
    result_file = open(RESULT_FILE_NAME, "wt")
    result_file.writelines(begin_list)
    result_file.writelines(t_list)
    result_file.writelines(end_list)
    result_file.close()

#creating 3 lists, the second one is the one that we are interested in
def make_t_list_from_orig(text_list):
    begin_t_list = "(M47, Zacatek bloku vrtani)\n"
    begin_list = list()
    t_list = list()
    end_list = list()
    index_t_list = 0
    
#creating the first part (until the line "M47, Zacatek bloku vrtani")
    for i in range(len(text_list)):
        begin_list.append(text_list[i])
        if text_list[i] == begin_t_list:
            index_t_list = i
            break
        
# + one empty line (there is one more line in the input file)
    begin_list.append(text_list[index_t_list + 1])
# jump to the right line
    index_t_list += 2

# creating the main list until we find \n and $\n after that (the end of our list)
    while (text_list[index_t_list] != '\n') and\
          (text_list[index_t_list + 1] != '$\n'):
        t_list.append(text_list[index_t_list])
        index_t_list += 1

#creating the third part until the end of the input file
    while index_t_list != len(text_list):
        end_list.append(text_list[index_t_list])
        index_t_list += 1

    return begin_list, t_list, end_list


#creating the dictionary where the key is the number of the line and the value is the number after T
#it's working with the second part t_list that we already created
def slovnik(t_list):
    result_dict = dict()

#this loop is looking for the line with "T"
    for i in range(len(t_list)):
        t_index = t_list[i].find('T') + 1 #+1 because the .find function is returning -2
        if t_index != -1 and t_index != 0:
            # we found the T line
            string = t_list[i]
            value = str()
            # we are writind the number after T into the value of our dictionary
            while string[t_index] != '\n':
                value += string[t_index]
                t_index += 1
            value = int(value)
            result_dict[i] = value

    return result_dict


def t_sort(t_dict, t_list):
    sort_list = list()
    sort_dict = dict()

    # sorting the keys
    buf_sorted_values = sorted(t_dict.values())
    for i in buf_sorted_values:
        for k in t_dict.keys():
            if t_dict[k] == i:
                sort_dict[k] = t_dict[k]
                break
            
    for key in sort_dict: # we are going through sorted keys of the dictionary
        # appening the T line
        sort_list.append(t_list[key])
        # the number of the line after
        t_index = key + 1
        # the loop to append all lines until we find the new "T"
        while (t_index < len(t_list)) and (t_list[t_index].find('T') == -1):
            sort_list.append(t_list[t_index])
            t_index += 1
    
    return sort_list

#the function for changing the default sort_list
def change(sort_list):
    i,p=0,0
    floats_list = list()
    default_x = list()
    changed_y = list()
    changed_sort_list = list()

    #find all the numbers in sort_list
    for x in sort_list:
        floats_list.append(re.findall("[-+]?\d+\.\d+", x))

    #calculating the new Y values  
    for j in floats_list:
        if float(j[0])>50.0:
            default_x.append(j[0])
            changed_y.append(str((float(j[1]))+10.0))
        if float(j[0])<=50.0:
            default_x.append(j[0])
            changed_y.append(j[1])
            
    #creating the list with new Y values     
    for c in sort_list:
        changed_sort_list.append("X"+str(default_x[i])+"Y"+str(changed_y[p])+"\n")
        i+=1
        p+=1

    return changed_sort_list

# the main function funkce1
def funkce1():
    main_file = open(MAIN_FILE_NAME, "rt") #open the input file
    text_list = main_file.readlines() #read line by line
    begin_list, t_list, end_list = make_t_list_from_orig(text_list) #deviding the input text on 3 lists
    t_dict = slovnik(t_list)
    sort_list = t_sort(t_dict, t_list)#sort the input text according to the dictionary

    changed_sort_list = change(sort_list)
    
    main_file.close()# close the file
    make_result_file(begin_list, changed_sort_list, end_list)#write the lists into .txt file

#the main function funkce2
def funkce2():
    floats_list = list()
    float_x = list()
    float_y = list()
    
    #reading the input file
    main_file = open(MAIN_FILE_NAME, "rt") #open the input file
    text_list = main_file.readlines() #read line by line
    begin_list, t_list, end_list = make_t_list_from_orig(text_list) #deviding the input text on 3 lists
    t_dict = slovnik(t_list)
    sort_list = t_sort(t_dict, t_list)#sort the input text according to the dictionary
    
    #find all numbers in strings
    for x in sort_list:
            floats_list.append(re.findall("[-+]?\d+\.\d+", x))
            
    #create 2 lists of X and Y coordinates for simplier
    #calculation of max/min parameters
    for j in floats_list:
        float_x.append(float(j[0]))
        float_y.append(float(j[1]))
        
    #calculation of max/min    
    max_x = max(float_x)
    min_x = min(float_x)
    max_y = max(float_y)
    min_y = min(float_y)

    #printing the results
    print("Max_X= ",max_x)
    print("Min_X= ",min_x)
    print("Max_Y= ",max_y)
    print("Min_Y= ",min_y)

