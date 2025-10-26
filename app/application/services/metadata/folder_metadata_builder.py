from pathlib import Path
from typing import Dict, Optional
import logging
import re

class FolderMetadataBuilder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.IGNORED_FOLDERS = {"Libros", "ePub", "PDF", "biblioteca"}

    def build_metadata(self, file_path: Path) -> Dict[str, Optional[str]]:
        """
        Combina metadatos inferidos desde la carpeta y el nombre del archivo.

        Args:
            file_path (Path): Ruta completa del archivo EPUB o PDF.

        Returns:
            Dict[str, Optional[str]]: Diccionario con autor, autores, serie, año y título.
        """
        folder_meta = self._infer_from_folder(file_path)
        file_meta = self._parse_filename(file_path)

        metadata = {
            "autor_principal": file_meta.get("autor_principal") or folder_meta.get("autor"),
            "autores": file_meta.get("autores"),
            "serie": folder_meta.get("serie"),
            "year": file_meta.get("year") or folder_meta.get("year"),
            "titulo": file_meta.get("titulo") or folder_meta.get("titulo")
        }

        self.logger.debug(f"Metadatos combinados: {metadata}")
        return metadata

    def _infer_from_folder(self, file_path: Path) -> Dict[str, Optional[str]]:
        """
        Extrae autor, serie y año desde la jerarquía de carpetas.

        Se asume:
        - autor/serie/archivo
        - autor/archivo

        Returns:
            Dict[str, Optional[str]]
        """
        metadata = {
            "autor": None,
            "serie": None,
            "year": None,
            "titulo": file_path.stem
        }

        # Filtrar carpetas irrelevantes
        folders = [p.name for p in file_path.parents if p.name not in self.IGNORED_FOLDERS]

        if not folders:
            return metadata

        metadata["autor"] = folders[0]

        # Si hay más de una carpeta, asumimos que la segunda es la serie
        if len(folders) > 1:
            metadata["serie"] = folders[1]

        # Si hay una tercera y es un año, lo tomamos como año
        if len(folders) > 2 and folders[2].isdigit():
            metadata["year"] = folders[2]

        self.logger.debug(f"Metadatos desde carpeta (filtrados): {metadata}")
        return metadata


    def _parse_filename(self, file_path: Path) -> Dict[str, Optional[str]]:
        nombre = file_path.stem
        patron = r"""
            

\[(?P<autores>.+?)\]

       # Autores entre corchetes
            (?:\s\((?P<year>\d{4})\))? # Año entre paréntesis (opcional)
            \s*-\s*(?P<titulo>.+)      # Título después del guion
        """
        match = re.match(patron, nombre, re.VERBOSE)
        if not match:
            self.logger.warning(f"Nombre de archivo no coincide con el patrón: {nombre}")
            return {
                "autores": [],
                "autor_principal": None,
                "year": None,
                "titulo": nombre
            }

        autores_raw = match.group("autores")
        autores = [a.strip() for a in re.split(r"[-,]", autores_raw)]
        return {
            "autores": autores,
            "autor_principal": autores[0] if autores else None,
            "year": match.group("year"),
            "titulo": match.group("titulo")
        }
