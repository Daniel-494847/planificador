import torch

print("=" * 50)
print("PRUEBA DE PYTORCH")
print("=" * 50)
print("Version de PyTorch:", torch.__version__)
print("CUDA disponible:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    dispositivo = torch.device("cuda")
else:
    print("Usando CPU")
    dispositivo = torch.device("cpu")

# Crear un tensor simple y hacer una operacion
x = torch.rand(5, 3, device=dispositivo)
print("\nTensor de ejemplo (5x3):")
print(x)

y = torch.rand(5, 3, device=dispositivo)
z = x + y
print("\nSuma de dos tensores:")
print(z)

print("\n" + "=" * 50)
print("PyTorch esta funcionando correctamente!")
print("=" * 50)