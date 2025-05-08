# Cel i kontekst programu:
# Program generuje losową sekwencję DNA i zapisuje ją w formacie FASTA.
# Dodatkowo oblicza statystyki zawartości nukleotydów i wstawia imię użytkownika w losowym miejscu.

import random  # do losowania nukleotydów i pozycji
import sys     # do ewentualnego wyjścia z programu
import os      # do zbudowania ścieżki dla pliku

# Funkcja pomocnicza: generowanie sekwencji DNA
def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length)) #Zwraca tekst jako sekwencje losową z liter ACGT

# Funkcja pomocnicza: obliczanie statystyk nukleotydów
def calculate_statistics(sequence):
    stats = {} #Pusta tablica
    total = len(sequence) #Liczba symbolizujaca dlugosc sekwencji
    for base in 'ACGT': #Petla dla kazdej litery
        stats[base] = sequence.count(base) / total * 100 #Liczy procentowo czestotliwosc kazdej litery do calosci
    cg = sequence.count('C') + sequence.count('G') #Ilosc C + G
    at = sequence.count('A') + sequence.count('T') #Ilosc A + T
    cg_at_ratio = cg / total * 100 if at != 0 else 0 #Procentowa zawartosc CG do calości
    return stats, cg_at_ratio #Zwraca statystyki wszystkie

# Pobieranie danych wejściowych od użytkownika
#ORIGINAL
#length = int(input("Podaj długość sekwencji: "))
#MODIFIED (Sekwencja nie może być krótsza od 1 bo nie miałoby to sensu)
try:
    length = int(input("Podaj długość sekwencji: ")) #Pobieranie dlugosci sekwencji ktora ma stworzyc
    if length <= 0: #Jesli dlugosc mniejsza rowna 0
        raise ValueError #Podnies blad
except ValueError:
    print("Długość sekwencji musi być dodatnią liczbą całkowitą.")
    sys.exit(1) #Jesli zlapie blad ma wypisac to co u gory i wyjsc z programu

seq_id = input("Podaj ID sekwencji: ").strip() #Pobieranie ID sekwencji
description = input("Podaj opis sekwencji: ").strip() #Pobieranie opisu sekwencji
name = input("Podaj imię: ").strip() #Pobieranie imiona użytkownika

# Generowanie sekwencji
sequence = generate_dna_sequence(length) #Wywolanie metody

# Wstawianie imienia w losowe miejsce
insert_pos = random.randint(0, len(sequence)) #Wyznaczenie losowego miejsca w sekwencji dla imienia
sequence_with_name = sequence[:insert_pos] + name + sequence[insert_pos:] #Dodanie imienia do tejze sekwencji

# Lokalizacja pliku
#ORIGINAL
#filename = f"{seq_id}.fasta"
#MODIFIED (Umożliwia użytkownikowi wybranie ścieżki gdzie plik ma zostać zapisany)
folder_path = input("Podaj pełną ścieżkę folderu, w którym chcesz zapisać plik (np. C:\\Users\\TwojeImie\\Documents): ") #Pobieranie pelnej lokalizacji dla pliku
if not os.path.isdir(folder_path): #Jesli uzytkownik nie podal lokalizacji
    print("Podany folder nie istnieje. Zapiszę plik w bieżącym katalogu.") #Wypisuje to
    folder_path = "."  #Bieżący folder #Tworzy plik w roboczym katalogu
filename = os.path.join(folder_path, f"{seq_id}.fasta") #Laczy sciezke wraz z nazwa pliku do ktorej wstawia sekwencje

# Zapis do pliku FASTA
with open(filename, 'w') as f: #Otwieranie mozliwosci zapisania pliku
    f.write(f">{seq_id} {description}\n") #Wpisuje do pliku id i opis sekwencji
    #ORIGINAL
    #f.write(sequence_with_name + "\n")
    #MODIFIED (Poprawa czytelności przy dużych/długich sekwencjach)
    for i in range(0, len(sequence_with_name), 40): #Petla co 40 zeby w linii byly po 40 znaki
        f.write(sequence_with_name[i:i + 40] + '\n') #Zapisuje liniowo do pliku po 40 znakow wycinajac z calosci

# Obliczanie statystyk (na podstawie sekwencji bez imienia)
stats, cg_at_ratio = calculate_statistics(sequence) #Komentarz wyzej

# Wyświetlanie wyników
print(f"Sekwencja została zapisana do pliku {filename}")
print("Statystyki sekwencji:")
for base in 'ACGT': #Petla idzie dla kazdej litery podajac wlasciwosci
    print(f"{base}: {stats[base]:.1f}%")
print(f"%CG: {cg_at_ratio:.1f}%")
