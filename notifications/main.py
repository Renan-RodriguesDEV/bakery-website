import json
import sys
import threading
import time

from consumer import callback, consumer
from publisher import publisher
from utilities import check


def run_publisher():
    while True:
        print("Verificando resultados")
        results = check()
        print(f"Total de produtos abaixo de estoque: {len(results)}")
        for product in results:
            if product:
                msg = json.dumps(
                    {
                        "status": "warning" if product.get("estoque") > 0 else "danger",
                        "product": product.get("nome"),
                        "stock": product.get("estoque"),
                        "id": product.get("id"),
                    }
                )
                try:
                    publisher.publish(msg)
                except Exception as e:
                    print(str(e))
        time.sleep(60 * 1)  # Await 1 minutes to check again


def run_consumer():
    try:
        consumer.start(callback=callback)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    thread_1 = threading.Thread(target=run_publisher)
    thread_2 = threading.Thread(target=run_consumer)
    thread_1.daemon = (
        True  # ← Permite sair do programa mesmo se a thread estiver rodando
    )
    thread_2.daemon = (
        True  # ← Permite sair do programa mesmo se a thread estiver rodando
    )
    thread_1.start()
    thread_2.start()
    try:
        while True:
            time.sleep(1)  # Mantém o programa principal rodando
    except KeyboardInterrupt:
        print("Process interrupted.")
        sys.exit(0)
