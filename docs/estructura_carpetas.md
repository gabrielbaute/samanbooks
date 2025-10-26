## 📚 Convención de nombres y estructura de archivos

### 📁 Estructura de carpetas

```plaintext
biblioteca/
├── Autor Principal/
│   ├── Libro suelto.epub
│   └── Serie/
│       ├── [Autor1-Autor2] (1995) - Libro 1.epub
│       └── [Autor1-Autor2] (1996) - Libro 2.epub
```

- Si el libro **no pertenece a una serie**, va directamente en la carpeta del autor.
- Si el libro **pertenece a una serie**, va en una subcarpeta dentro del autor.

---

### 📄 Convención de nombre de archivo

```
[Autor1-Autor2] (Año) - Título del libro.ext
```

- Autores entre corchetes `[...]`
- Separados por guiones `-` o comas `,` (evitar puntos)
- Año entre paréntesis `(1995)` — opcional
- Título después del guion `-`
- Extensión `.epub`, `.pdf`, etc.

---

## 🧠 Reglas de interpretación

| Elemento       | Regla                                                                 |
|----------------|-----------------------------------------------------------------------|
| Autores        | Extraídos desde los corchetes. Separados por `-` o `,`.              |
| Autor principal| El primero de la lista.                                               |
| Año            | Extraído desde los paréntesis. Opcional.                             |
| Título         | Todo lo que sigue después del guion.                                 |
| Serie          | Inferida desde la carpeta que contiene el archivo.                   |
| Autor carpeta  | Carpeta raíz que contiene el archivo o la serie.                     |

---

## ✅ ¿Qué hacer con múltiples autores?

- El **primer autor** se considera el principal.
- Los demás se agregan como coautores en la base de datos.
- Si la serie tiene múltiples autores, se repite este patrón por cada libro.

---