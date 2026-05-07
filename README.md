# Minecraft Mod Builder

Aplikacja do tworzenia i kompilowania modów do Minecrafta bez ręcznej konfiguracji.

---

## Pobieranie

Pobierz gotowy plik `.exe` z zakładki **[Releases](../../releases/latest)**.

---

## Wymagania

Przed uruchomieniem zainstaluj odpowiednią wersję Javy:

- **Java 17** — dla Minecraft 1.16.5 – 1.20.4
- **Java 21** — dla Minecraft 1.20.5 – 1.21.4

Pobierz Javę: [adoptium.net](https://adoptium.net)

---

## Jak używać

### 1. Konfiguracja

W zakładce **Ustawienia** wypełnij dane moda:

- **Nazwa moda** — np. `MyCoolMod`
- **Autor** — twój nick
- **Wersja Minecraft** — wybierz z listy
- **Mod Loader** — Forge lub Fabric
- **Folder wyjściowy** — gdzie zostanie zapisany projekt

### 2. Dodanie kodu (opcjonalnie)

Przejdź do zakładki **Kod Java**:

- Kliknij **Importuj** i wybierz swoje pliki `.java`
- Lub kliknij **+ Nowy**, wklej kod ręcznie
- Jeśli nie dodasz kodu — zostanie użyty domyślny szablon

### 3. Utwórz projekt

Kliknij **Utwórz Strukturę** — aplikacja wygeneruje wszystkie pliki i pobierze wymagane zależności.

### 4. Kompilacja

Kliknij **Kompiluj Moda**. Przy pierwszym uruchomieniu Gradle pobierze pliki Minecrafta (~300–500 MB, jednorazowo). Gotowy mod `.jar` znajdziesz w:

```
NazwaModa/build/libs/
```

---

## Obsługiwane wersje

**Forge:** 1.16.5, 1.18.2, 1.19.2, 1.19.4, 1.20.1 – 1.20.6, 1.21 – 1.21.4

**Fabric:** 1.19.4, 1.20.1 – 1.20.6, 1.21 – 1.21.4

---

## Uwaga — antywirus

Plik `.exe` może zostać fałszywie wykryty przez program antywirusowy. To znane zachowanie plików tworzonych przez PyInstaller i nie oznacza zagrożenia. Kod źródłowy jest dostępny w tym repozytorium do weryfikacji.
