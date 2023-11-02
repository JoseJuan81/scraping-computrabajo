import time

def tiempo_ejecucion(plataform):
    def inner_fn(fn):
        def calculating_time(*args, **kwargs):
            print("!!!"*40)
            init_time = time.time
            print(f"INICIO: {plataform}")
            print("!!!"*40)

            fn(*args, **kwargs)

            print("!!!"*40)
            print(f"FIN: {plataform}")
            print(f"=== Realizado en {time.time() - init_time} segundos ===")
            print("!!!"*40)

        return calculating_time

    return inner_fn