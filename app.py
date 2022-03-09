from PIL import Image

class CImage:
    def __init__(self, path):
        self.image = Image.open(path)

    def size(self):
        return self.image.size
    
    def get_image(self):
        return self.image
    
    def get_pixel(self, x, y):
        return self.image.getpixel((x, y))

    def set_pixel(self, x, y, color):
        self.image.putpixel((x, y), color)


img = CImage("img.jpg")

bw_image      = Image.new('RGB', img.size())
blurred_image = Image.new('RGB', img.size())
pixeled_image = Image.new('RGB', img.size())

def average_pixel_value(color):
    r,g,b = color
    avg = int((r + g + b) / 3)
    return (avg,avg,avg)

for x in range(0, img.size()[0]):
    for y in range(0, img.size()[1]):
        avg_color = average_pixel_value(img.get_pixel(x, y))
        bw_image.putpixel((x, y), avg_color)




def get_colors_array(x,y, image, batch_size=10):
    colors=[]
    size_x, size_y = image.size()
    for i in range(int(x-batch_size/2), int(x+batch_size/2)):
        for j in range(int(y-batch_size/2), int(y+batch_size/2)):
            if i >= 0 and i < size_x and j >= 0 and j < size_y: 
                colors.append(image.get_pixel(i, j))

    r = [c[0] for c in colors]
    g = [c[1] for c in colors]
    b = [c[2] for c in colors]
    
    r = int(sum(r) / len(r))
    g = int(sum(g) / len(g))
    b = int(sum(b) / len(b))
    
    return (r,g,b)


""" blurring """
batch_size = 5
size_x, size_y = img.size()
for x in range(0, size_x):
    for y in range(0, size_y):
        avg_color_of_field = get_colors_array(x,y, img, batch_size)
        blurred_image.putpixel((x, y), avg_color_of_field)


""" pixelating  """
batch_size = 2
size_x, size_y = img.size()
for x in range(0, size_x, batch_size):
    for y in range(0, size_y, batch_size):
        avg_color_of_field = get_colors_array(x,y, img, batch_size)
        
        for x1 in range(x, x+batch_size):
            for y1 in range(y, y+batch_size):
                try:
                    pixeled_image.putpixel((x1, y1), avg_color_of_field)
                except:
                    pass
        



def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

im1 = get_concat_v(img.get_image(), bw_image)
im2 = get_concat_v(im1, blurred_image)
im3 = get_concat_v(im2, pixeled_image)

im3.show()