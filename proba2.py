import os
import json
import matplotlib.pyplot as plt

data = []
if not os.path.exists("stat2.json"):
    data.append(40)
    with open("stat2.json","w") as f:
        f.write(json.dumps(data))

else:
    with open("stat2.json","r") as f:
            main_data = json.load(f)
    
    new=50
    main_data.append(new)

    with open("stat2.json", "w") as f:
        f.write(json.dumps(main_data))

    for num in main_data:
        data.append(num)



def func():
    y = [100]*len(data)
    #print(y)
    plt.scatter(data,y)
    plt.show()

func()


        for char in word:
            if char in "123456789#&@<>~ˇ^~˘°˛+%?Ł$ßł´˝¨¸":
                raise Exception("Invalid Word")
        for c in definition:
            if c in "123456789#&@<>~ˇ^~˘°˛+%?Ł$ßł´˝¨¸":
                raise Exception("Invalid Definition")      
            