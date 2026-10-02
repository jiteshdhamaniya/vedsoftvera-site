import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('prepare_site', Path(__file__).with_name('prepare-site.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PrepareSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'source'
        self.source.mkdir()
        for name in ('index.html', 'contact.html', 'styles.css'):
            (self.source / name).write_text('public content')
        (self.source / 'assets').mkdir()
        (self.source / 'assets/logo.png').write_bytes(b'image')

    def prepare(self):
        return module.prepare(self.source, self.base / 'public', self.base / 'manifest')

    def test_excludes_internal_files_and_checksums_public_files(self):
        for name in ('AGENTS.md', 'README.md', '.env'):
            (self.source / name).write_text('not public')
        self.assertEqual(self.prepare(), 4)
        published = {p.relative_to(self.base / 'public').as_posix() for p in (self.base / 'public').rglob('*') if p.is_file()}
        self.assertEqual(published, {'index.html', 'contact.html', 'styles.css', 'assets/logo.png'})
        self.assertEqual(len((self.base / 'manifest').read_text().splitlines()), 4)

    def test_rejects_missing_homepage_before_writing(self):
        (self.source / 'index.html').unlink()
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse((self.base / 'public').exists())

    def test_rejects_asset_symlink_to_private_file(self):
        (self.source / '.env').write_text('not public')
        (self.source / 'assets/leak.png').symlink_to(self.source / '.env')
        with self.assertRaises(ValueError):
            self.prepare()

    def test_rejects_hidden_assets(self):
        (self.source / 'assets/.env').write_text('not public')
        with self.assertRaises(ValueError):
            self.prepare()


if __name__ == '__main__':
    unittest.main()
