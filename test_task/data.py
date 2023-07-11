from faker import Faker
import requests
from multiprocessing import Pool

fake = Faker()

num_polygons = 10000
polygon_list = []
def random_gen(_):
    # Generate random coordinates
    x1 = round(float(fake.longitude()),2)
    y1 = round(float(fake.latitude()), 2)
    x2 = x1 + fake.random_int()
    y2 = y1 + fake.random_int()
    coords = [[[x1, y1], [x1, y2], [x2, y2], [x2, y1], [x1, y1]]]
    #polygon = Polygon(coords)
    #polygon_list.append(coords)
    d = {"name": "test", "price": 1, "provider": 2, "polygon": {
        "type": "Polygon",
        "coordinates": coords
    }
         }
    return d

def generate_random_numbers_parallel(num_numbers, num_processes):
    with Pool(num_processes) as pool:
        random_numbers = pool.map(random_gen, range(num_numbers))
    return random_numbers

#l=[]
#for p in polygon_list:
#    d = {"name":"test","price":1,"provider":2,"polygon":{
#    "type": "Polygon",
#     "coordinates": p
#  }
#  }
#    l.append(d)


if __name__ == "__main__":
    num_processes = 10
    num_numbers = 100000
    random_numbers = generate_random_numbers_parallel(num_numbers, num_processes)
    print('sending')
    r = requests.post('http://127.0.0.1:8000/service-area/add', json=random_numbers)
    print('sent')
    print(r.text)
