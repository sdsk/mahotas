import numpy as np
import mahotas.texture
import mahotas._texture

def test__cooccurence():
    cooccurence = mahotas._texture.cooccurence
    f = np.array([
          [0,1,1,1],
          [0,0,1,1],
          [2,2,2,2],
        ])
    res = np.zeros((5,5), np.long)
    cooccurence(f, res, 0, 0)
    assert res[0,0] == 1
    assert res[0,1] == 2
    assert res[1,0] == 0
    assert res[1,1] == 3
    assert res[2,2] == 3
    assert not np.any(res[2,:2])
    assert not np.any(res[:2,2])
    res[:3,:3] = 0
    assert not np.any(res)

    res = np.zeros((5,5), np.long)
    cooccurence(f, res, 1, 0)
    assert res[0,0] == 1
    assert res[0,1] == 0
    assert res[0,2] == 2
    assert res[1,0] == 0
    assert res[1,1] == 2
    assert res[1,2] == 1
    res[:3,:3] = 0
    assert not np.any(res)


def brute_force(f, dy, dx):
    res = np.zeros((f.max()+1, f.max() + 1), np.double)
    for y in xrange(f.shape[0]):
        for x in xrange(f.shape[1]):
            if 0 <= y + dy < f.shape[0] and \
                0 <= x + dx < f.shape[1]:
                res[f[y,x], f[y +dy,x+dx]] += 1
    return res


def brute_force_sym(f, dy, dx):
    cmat = brute_force(f, dy, dx)
    return (cmat + cmat.T)

def test_cooccurence():
    np.random.seed(222)
    f = np.random.rand(32, 32)
    f = (f * 255).astype(np.int32)

    assert np.all(mahotas.texture.cooccurence(f, 0, symmetric=False) == brute_force(f, 0, 1))
    assert np.all(mahotas.texture.cooccurence(f, 1, symmetric=False) == brute_force(f, 1, 1))
    assert np.all(mahotas.texture.cooccurence(f, 2, symmetric=False) == brute_force(f, 1, 0))
    assert np.all(mahotas.texture.cooccurence(f, 3, symmetric=False) == brute_force(f, 1, -1))

    assert np.all(mahotas.texture.cooccurence(f, 0, symmetric=1) == brute_force_sym(f, 0, 1))
    assert np.all(mahotas.texture.cooccurence(f, 1, symmetric=1) == brute_force_sym(f, 1, 1))
    assert np.all(mahotas.texture.cooccurence(f, 2, symmetric=1) == brute_force_sym(f, 1, 0))
    assert np.all(mahotas.texture.cooccurence(f, 3, symmetric=1) == brute_force_sym(f, 1, -1))

def test_haralick():
    np.random.seed(123)
    f = np.random.rand(1024, 1024)
    f = (f * 255).astype(np.int32)
    feats = mahotas.texture.haralick(f)
    assert not np.any(np.isnan(feats))

