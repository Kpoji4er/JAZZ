"""Small independent coverage, determinism and limit tests for ZIP delivery."""
import tempfile,zipfile,random
from pathlib import Path
from _prepare_release_assets import distribute

with tempfile.TemporaryDirectory(prefix='jazz-release-parts-') as temp:
    root=Path(temp);archive=root/'package.zip'
    rng=random.Random(371)
    originals={f'jazz_assets/file-{i}.bin':rng.randbytes(1800) for i in range(9)}
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in originals.items():z.writestr(name,data)
    first=distribute(archive,limit=8000,target=5000)
    assert len(first)>1
    seen={}
    for row in first:
        assert row['bytes']<8000
        with zipfile.ZipFile(root/row['artifact']) as z:
            assert z.testzip() is None
            for name in z.namelist():
                assert name not in seen
                seen[name]=z.read(name)
    assert seen==originals
    assert distribute(archive,limit=8000,target=5000)==first
    assert len(distribute(archive,limit=100000,target=5000))==1
    try:distribute(archive,limit=8000,target=1000)
    except ValueError:pass
    else:raise AssertionError('oversized entry accepted')
print('PASS: complete byte coverage, no duplicates, deterministic ZIP parts, size guards, unsplit package')
