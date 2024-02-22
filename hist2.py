
import cv2 
import glob
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

image_stage1 = list(glob.glob('stage hydro/stage1/train/*.png'))
#print("Images1:", len(image_stage1))
image_stage2 = list(glob.glob('stage hydro/stage2/train/*.png'))
#print("Images2:", len(image_stage2))
image_stage3 = list(glob.glob('stage hydro/stage3/train/*.*'))
#print("Images3:", len(image_stage3))
test_stage = list(glob.glob('testimage/*.*'))
#print("temp test:", len(test_stage))


histogram1 = []
histogram2 = []
histogram3 = []
# stage1 image รูปมาเฉลี่ย
def count_white_pixel(detect,width,height):
        white_pixel_count = 0
        for i in range(width):
            for j in range(height):
                # Check if the pixel is white (255 in grayscale)
                if detect[i, j] == 255:
                    white_pixel_count += 1

        return white_pixel_count
    
def processing_img():
    
    for i,image_path in enumerate(image_stage1):
        
        image = cv2.imread(image_path)
        # Define the new size (width, height)
        new_size = (400, 300)

    # Resize the image
        image = cv2.resize(image, new_size) 
        #print(f"Processing image: {image_path}")
        sens = 20
        min = np.array([50-sens, 100, 50])
        max = np.array([50+sens, 255, 255])

        
        image1 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        detect = cv2.inRange(image1, min, max)
        white_pixel_count1 = cv2.countNonZero(detect) 
        hist1 = cv2.calcHist([detect], [0],  
                              None, [256], [0, 256])
        histogram1.append(hist1)
    mean_histogram1 = np.mean(histogram1, axis=0) 
    plt.plot(mean_histogram1,label = 'stage1')

    # stage2 image 
    for i,image_path in enumerate(image_stage2):
        
        image = cv2.imread(image_path) 
        new_size = (400, 300)

    # Resize the image
        image = cv2.resize(image, new_size) 
        sens = 20
        min = np.array([50-sens, 100, 50])
        max = np.array([50+sens, 255, 255])

        
        image2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        detect = cv2.inRange(image2, min, max)
        white_pixel_count2 = cv2.countNonZero(detect)
        hist2 = cv2.calcHist([detect], [0],  
                              None, [256], [0, 256])
        histogram2.append(hist2) 
    mean_histogram2 = np.mean(histogram2, axis=0) 
    plt.plot(mean_histogram2,label = 'stage2')
     
    # stage3 image 
    for i,image_path in enumerate(image_stage3):

        image = cv2.imread(image_path)
        new_size = (400, 300)

    # Resize the image
        image = cv2.resize(image, new_size) 
        #width,height = image.shape() 
        if image is not None:
            sens = 20
            min = np.array([50-sens, 100, 50])
            max = np.array([50+sens, 255, 255])

        
            image3 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            detect = cv2.inRange(image3, min, max)
            white_pixel_count3 = cv2.countNonZero(detect)
            hist3 = cv2.calcHist([detect], [0],  
                              None, [256], [0, 256])

            histogram3.append(hist3)


        else:
            print(f"Error reading image: {image_path}") 

    mean_histogram3 = np.mean(histogram3, axis=0)
     
    plt.plot(mean_histogram3,label = 'stage3')

    # test image
    #fig, axs = plt.subplots(1, len(image_paths), figsize=(12, 4))
    for i,image_path in enumerate(test_stage):

        image = cv2.imread(image_path) 
        # Define the new size (width, height)
        new_size = (400, 300)

    # Resize the image
        image = cv2.resize(image, new_size)
        sens = 20
        min = np.array([50-sens, 100, 50])
        max = np.array([50+sens, 255, 255])

        
        test_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        detect = cv2.inRange(test_image, min, max) 
        white_pixel_count = cv2.countNonZero(detect)
        histogram = cv2.calcHist([detect], [0],  
                             None, [256], [0, 256])
        #print(image_path)
        #print(f'No. white pixels{white_pixel_count}') 
        plt.plot(histogram,label = 'test')


        c1, c2 ,c3= 0, 0, 0
        # white = 255
        # Euclidean Distance between data1 and test 
        i = 0
        """while i<len(histogram) and i<len(mean_histogram1): 
            c1+=(histogram[i]-mean_histogram1[i])**2
            i+= 1
        c1 = c1**(1 / 2) 
        
        
        # Euclidean Distance between data2 and test 
        i = 0
        while i<len(histogram) and i<len(mean_histogram2): 
            c2+=(histogram[i]-mean_histogram2[i])**2
            i+= 1
        c2 = c2**(1 / 2)
        # Euclidean Distance between stage3 and test 
        i = 0
        while i<len(histogram) and i<len(mean_histogram3): 
            c3+=(histogram[i]-mean_histogram2[3])**2
            i+= 1
        c3 = c3**(1 / 2)
    """
        c1 = (white_pixel_count - white_pixel_count1)**2
        c1 = c1**(1/2)
        c2 = (white_pixel_count - white_pixel_count2)**2
        c2 = c2**(1/2)
        c3 = (white_pixel_count - white_pixel_count3)**2
        c3 = c3**(1/2)
        if(c1<c2) and (c1<c3): 
            
            #print(f'c1 score ={c1} ',end="")
            #print(f'c2 score ={c2} ',end="")
            #print(f'c3 score ={c3} ')
            print("a period of exponential phase") #
            return "a period of exponential phase"
        elif(c2<c1)and(c2<c3): 
            #print(f'c1 score ={c1} ',end="")
            #print(f'c2 score ={c2} ',end="")
            #print(f'c3 score ={c3} ')
            print("linear phase") #
            return "linear phase"
        elif(c3<c1)and(c3<c2): 
            #print(f'c1 score ={c1} ',end="")
            #print(f'c2 score ={c2} ',end="")
            #print(f'c3 score ={c3} ')
            print("steady state phase") #
            return "steady state phase"
        else: 
            print("error no stage detect")
            return "error no stage detect"


