from multiprocessing import Pool, cpu_count, Queue, Process
from concurrent.futures import ProcessPoolExecutor


from my_time import timing_decorator

def work_process(num: int) -> list[int]:
    res = [1]
    for i in range(2, num):
        if not num % i:
            res.append(i)
    return res + [num]

# def work_process_queue(qu: Queue, result_qu: Queue):
#     while not qu.empty():
#         num = qu.get()
#         res = [1]
#         for i in range(2, num):
#             if not num % i:
#                 res.append(i)
#         result_qu.put(res + [num])
#         sys.exit(0)  

@timing_decorator
def one_process_factorize(*numbers):
    res = []
    for num in numbers:
        res.append(work_process(num))
    return res

def callback(result):
    return result

@timing_decorator
def multi_callback_factorize(*numbers):
    with Pool(cpu_count()) as p:
        results = p.map_async(work_process, numbers, callback=callback)
        p.close()  # перестати виділяти процеси в пулл
        p.join()  # дочекатися закінчення всіх процесів
        
    return results.get()    

@timing_decorator
def multi_pool_map_factorize(*numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(work_process, numbers)

@timing_decorator
def multi_process_pool_executor(*numbers):
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        return executor.map(work_process, numbers)
       
# @timing_decorator        
# def multi_queua_factorize(*numbers):
#     input_queue = Queue()
#     result_queue = Queue()
#     [input_queue.put(num) for num in numbers]

#     processes = []
#     for _ in range(cpu_count()):
#         p = Process(target=work_process_queue, args=(input_queue, result_queue))
#         processes.append(p)
#         p.start()
#     [p.join() for p in processes]
#     result_queue.put(None)
#     results = []
#     results = list(iter(result_queue.get_nowait, None))
#TODO не вийшло витягнути послідовно результати
#     return results

def call_assert(a,b,c,d):
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(a, b, c, d, sep="\n", end='\n\n')
  
if __name__ == "__main__":
    numbers = 128, 255, 99999, 10651060, 128, 255, 99999, 10651060, 128, 255, 99999, 10651060, 128, 255, 99999, 10651060
    
    a, b, c, d, *_  = one_process_factorize(*numbers)
    call_assert(a,b,c,d)

    a, b, c, d, *_ = multi_callback_factorize(*numbers)
    call_assert(a,b,c,d)
   
    a, b, c, d, *_ = multi_pool_map_factorize(*numbers)
    call_assert(a,b,c,d)
    
    a, b, c, d, *_ = multi_process_pool_executor(*numbers)
    call_assert(a,b,c,d)