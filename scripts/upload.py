#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.use_cases.youtube_use_cases import UploadMultipleVideosUseCase
from src.infrastructure.file_system.file_service import YouTubeFileSystemService
from config.settings import config


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.log_file)
        ]
    )


def ask_user_confirmation(message: str) -> bool:
    """Pergunta confirmação ao usuário."""
    while True:
        response = input(f"\n{message} (s/n): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            return True
        elif response in ['n', 'não', 'nao', 'no']:
            return False
        else:
            print("Por favor, digite 's' para sim ou 'n' para não.")


def delete_successful_folders(successful_folders: list) -> int:
    """Delete pastas que tiveram upload bem-sucedido."""
    if not successful_folders:
        return 0
    
    print("\n" + "=" * 70)
    print("PASTAS COM UPLOAD BEM-SUCEDIDO")
    print("=" * 70)
    
    for idx, folder in enumerate(successful_folders, 1):
        print(f"{idx}. {folder}")
    
    print("\n" + "=" * 70)
    
    if ask_user_confirmation(f"Deseja deletar essas {len(successful_folders)} pasta(s)?"):
        file_service = YouTubeFileSystemService()
        deleted_count = 0
        
        for folder in successful_folders:
            if file_service.delete_folder(folder):
                print(f"✓ Deletada: {folder}")
                deleted_count += 1
            else:
                print(f"✗ Erro ao deletar: {folder}")
        
        print(f"\n{deleted_count}/{len(successful_folders)} pastas deletadas com sucesso.")
        return deleted_count
    
    return 0


def main():
    setup_logging()
    
    print("=" * 70)
    print("UPLOAD DE VÍDEOS - YouTube")
    print("=" * 70)
    print(f"Diretório de origem: {config.video_source_dir}")
    print(f"Vídeos por execução: {config.videos_to_upload_per_run}")
    print("=" * 70)
    
    try:
        if not Path(config.video_source_dir).exists():
            print(f"\n✗ Diretório não encontrado: {config.video_source_dir}")
            sys.exit(1)
        
        use_case = UploadMultipleVideosUseCase()
        stats = use_case.execute(
            config.video_source_dir,
            config.videos_to_upload_per_run
        )
        
        print("\n" + "=" * 70)
        print("RESUMO DO UPLOAD")
        print("=" * 70)
        print(f"Total:    {stats['total']}")
        print(f"Sucessos: {stats['success']}")
        print(f"Falhas:   {stats['failed']}")
        if stats['total'] > 0:
            print(f"Taxa:     {(stats['success']/stats['total']*100):.1f}%")
        print("=" * 70)
        
        # Perguntar se quer deletar pastas com sucesso
        if stats['successful_folders']:
            delete_successful_folders(stats['successful_folders'])
        
    except Exception as e:
        print(f"\n✗ Erro durante upload: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
