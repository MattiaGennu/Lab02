import csv

def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            righe = list(reader)
            if not righe:
                print("File vuoto.")
                return None

            num_sezioni = int(righe[0][0])
            biblioteca = [[] for _ in range(num_sezioni)]

            for riga in righe[1:]:
                if len(riga) < 5:
                    continue
                titolo, autore, anno, pagine, sezione = [x.strip() for x in riga]
                libro = {
                    "titolo": titolo,
                    "autore": autore,
                    "anno": int(anno),
                    "pagine": int(pagine),
                    "sezione": int(sezione)
                }
                if 1 <= libro["sezione"] <= num_sezioni:
                    biblioteca[libro["sezione"] - 1].append(libro)
                else:
                    print(f"Attenzione: sezione {libro['sezione']} non valida, libro ignorato.")

        print("Biblioteca caricata correttamente.")
        return biblioteca

    except FileNotFoundError:
        print("Errore: file non trovato.")
        return None
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        return None


def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""
    if sezione < 1 or sezione > len(biblioteca):
        print("Errore: sezione non esistente.")
        return None

    for sezione_libri in biblioteca:
        for libro in sezione_libri:
            if libro["titolo"].lower() == titolo.lower():
                print("Errore: titolo già presente.")
                return None

    nuovo_libro = {
        "titolo": titolo,
        "autore": autore,
        "anno": anno,
        "pagine": pagine,
        "sezione": sezione
    }

    biblioteca[sezione - 1].append(nuovo_libro)

    try:
        with open(file_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([titolo, autore, anno, pagine, sezione])
        return nuovo_libro
    except FileNotFoundError:
        print("Errore: file non trovato.")
        return None
    except Exception as e:
        print(f"Errore durante la scrittura del file: {e}")
        return None


def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    for sezione_libri in biblioteca:
        for libro in sezione_libri:
            if libro["titolo"].lower() == titolo.lower():
                return f"{libro['titolo']}, {libro['autore']}, {libro['anno']}, {libro['pagine']}, {libro['sezione']}"
    return None


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    if sezione < 1 or sezione > len(biblioteca):
        print("Errore: sezione non esistente.")
        return None

    sezione_libri = biblioteca[sezione - 1]
    if not sezione_libri:
        print("Nessun libro in questa sezione.")
        return []

    return sorted([libro["titolo"] for libro in sezione_libri])


def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

