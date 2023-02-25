#!/usr/bin/python3
# -*- coding: utf-8 -*-

print("\n******************* Python Calculator *******************")

print("Selecione o número da opção desejada:")

print("1 - Soma\n 2 - Subtração\n 3 - Multiplicação\n 4 - Divisão")

operação = int(input("Digite sua opção (1/2/3/4): "))

primeiro = int(input("Digite o primeiro número: "))

segundo = int(input("Digite o segundo número: "))

if operação == 1:
    print(primeiro+segundo)
elif operação == 2:
    print(primeiro-segundo)
elif operação == 3:
    print(primeiro*segundo)
elif operação == 4 :
    print(primeiro/segundo)
else :
    print("Opção inválida")
