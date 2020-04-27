import os

def labelChange(path_link):
    label = 'Label'
    
    #Customỉze class_id
    class_id = 0

    for v in os.listdir(path_link):
        #Load link
        file = os.path.join(path_link, v)
        file = file + '/' #On ubuntu dont need this
        file = os.path.join(file, label)
        file = file + '/'

        for i in os.listdir(file):
            #Link labelfile
            labelfile = os.path.join(file, i)

            #Get lineString
            f = open(labelfile, 'r')
            i = f.readlines()
            f.close()

            #Replace string to class_id
            f = open(labelfile, 'w')
            for line in i:
                #Load line and split
                listString = line.split()
                listString[0] = class_id    #Replace string

                list2String = ' '.join([str(elem) for elem in listString])
                f.write(list2String)
                f.write('\n')
            f.close()
        class_id += 1

#Link to pathfile, can customize it
train_link = 'OID/Dataset/train/'
test_link = 'OID/Dataset/test/'
val_link = 'OID/Dataset/validation/'

labelChange(train_link)
labelChange(test_link)
labelChange(val_link)