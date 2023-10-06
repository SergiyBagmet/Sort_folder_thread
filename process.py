from multiprocessing import Pool, cpu_count
import time



def work_process(num):
    res = [1]
    for i in range(2, num):
        if not num % i:
            res.append(i)
    return res + [num]      

def callback(result):
    return result




def factorize(*numbers):
    with Pool(cpu_count()) as p:
        results = p.map_async(
            work_process,
            numbers,
            callback=callback,
        )
        p.close()  # перестати виділяти процеси в пулл
        p.join()  # дочекатися закінчення всіх процесів
        
    return results.get()    
    
if __name__ == "__main__":
    start_time = time.time()  # Засекаем начальное время
    
    a, b, c, d  = factorize(128, 255, 99999, 10651060)
    
    end_time = time.time()  # Засекаем конечное время

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    
    
    execution_time = end_time - start_time  # Вычисляем время выполнения
    print(f"\nExecution time: {execution_time} seconds\n")
    print(a,b,c,d, sep="\n")
   