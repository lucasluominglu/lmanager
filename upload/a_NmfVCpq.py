def  max_min(the_list):
  max_value = the_list[0]
  min_value = the_list[0]
  for j in the_list[1:]:
    if j > max_value:
    	max_value = j
    if j < min_value:
    	min_value = j

    print(max_value, min_value)

if __name__ == '__main__':
	num = [1,0,4,2,3]
	max_min(num)