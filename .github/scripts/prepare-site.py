#!/usr/bin/env python3
"""Validate and stage only public static website files for production."""
import argparse
import hashlib
from pathlib import Path
import shutil

ROOT_TYPES = {'.html', '.css', '.js', '.ico', '.png', '.svg', '.webmanifest'}
ROOT_NAMES = {'robots.txt', 'sitemap.xml', 'feed.xml'}
ASSET_TYPES = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.svg', '.ico',
               '.css', '.js', '.woff', '.woff2', '.ttf', '.otf', '.mp4', '.webm', '.pdf'}


def prepare(source: Path, output: Path, manifest: Path) -> int:
    source = source.resolve()
    if output.exists() or manifest.exists():
        raise ValueError('Output directory and manifest must be new paths')
    for required in ('index.html', 'contact.html', 'styles.css'):
        p = source / required
        if p.is_symlink() or not p.is_file() or p.stat().st_size == 0:
            raise ValueError(f'Missing, empty, or symlinked required file: {required}')
    files = []
    for p in source.iterdir():
        if p.suffix.lower() in ROOT_TYPES or p.name in ROOT_NAMES:
            if p.is_symlink() or not p.is_file():
                raise ValueError(f'Invalid public file: {p.name}')
            files.append(p)
    assets = source / 'assets'
    if assets.is_symlink() or not assets.is_dir():
        raise ValueError('assets must be a real directory')
    for p in assets.rglob('*'):
        if p.is_symlink() or any(part.startswith('.') for part in p.relative_to(source).parts):
            raise ValueError(f'Hidden or symlinked asset: {p.relative_to(source)}')
        if p.is_file():
            if p.suffix.lower() not in ASSET_TYPES:
                raise ValueError(f'Unsupported asset type: {p.relative_to(source)}')
            files.append(p)
    rows = []
    for p in sorted(files):
        rel = p.relative_to(source)
        if any(char in str(rel) for char in ('\n', '\r', '\\')):
            raise ValueError('Unsupported filename in checksum manifest')
        rows.append((p, rel))
    output.mkdir(parents=True, exist_ok=False)
    sums = []
    for p, rel in rows:
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dest)
        dest.chmod(0o644)
        sums.append(f'{hashlib.sha256(dest.read_bytes()).hexdigest()}  ./{rel.as_posix()}\n')
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(''.join(sums))
    return len(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    print(f'Staged {prepare(args.source, args.output, args.manifest)} public files.')
