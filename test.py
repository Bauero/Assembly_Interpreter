# from pympler import asizeof
# import array
# import numpy as np
# import ctypes

# # Przykład z array
# arr = array.array('', [0] * 32)
# print("Rozmiar array (pympler):", asizeof.asizeof(arr))

# # Przykład z numpy
# np_arr = np.zeros(32, dtype=np.bool)
# print("Rozmiar Numpy array (pympler):", asizeof.asizeof(np_arr))

# # Przykład z ctypes
# buffer = ctypes.create_string_buffer(32)
# print("Rozmiar ctypes buffer (pympler):", asizeof.asizeof(buffer))

# import tracemalloc

# # Startujemy monitorowanie alokacji pamięci
# tracemalloc.start()

# # Przykład z numpy
# import numpy as np
# np_arr = np.zeros(32, dtype=np.int32)

# # Uzyskanie statystyk pamięci
# current, peak = tracemalloc.get_traced_memory()
# print(f"Obecne zużycie pamięci: {current} B; Szczytowe zużycie: {peak} B")

# # Zatrzymujemy monitorowanie
# tracemalloc.stop()

from memory_profiler import profile

@profile
def test_array():
    import array
    arr = array.array('i', [0] * 10000)
    return arr

@profile
def test_numpy():
    import numpy as np
    np_arr = np.zeros(1000000, dtype=np.int32)
    return np_arr

@profile
def test_ctypes():
    import ctypes
    buffer = ctypes.create_string_buffer(32)
    return buffer

test_array()
test_numpy()
test_ctypes()