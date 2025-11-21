#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.use_cases.youtube_use_cases import UploadMultipleVideosUseCase
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
        
    except Exception as e:
        print(f"\n✗ Erro durante upload: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
