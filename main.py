import itertools
import collections

def extract_alphabet(data):
    alpha = set()
    for datum in data:
        alpha |= set(datum)
    return alpha

def extract_local_k_grams(data, k, edges):
    attested = set()
    for datum in data:
        datum = (edges[0],) * (k - 1) + tuple(datum) + (edges[1],) * (k - 1)
        for offset in range(len(datum) - k + 1):
            attested.add(tuple(datum[offset:(offset + k)]))
    return attested

def valid_k_gram(k_gram, edges):
    k = len(k_gram)
    return any(True for L, R in itertools.product(range(k + 1), repeat=2) \
               if  all(k_gram[i] == edges[0]  for i in range(L)) \
               and all(k_gram[i] == edges[1]  for i in range(R, k)) \
               and not any(k_gram[i] in edges for i in range(L, R)) \
               and not any({*k_gram} == {e} for e in edges) \
               if L <= R)

def mtslia(data, k=2, edges=('>', '<')):
    alpha = extract_alphabet(data)
    attested = extract_local_k_grams(data, k, edges)
    grammar = collections.defaultdict(set)
    for k_gram in itertools.product(alpha | {*edges}, repeat=k):
        if k_gram in attested:
            continue
        if not valid_k_gram(k_gram, edges):
            continue
        projection = []
        for m, datum in enumerate(data):
            projection += [(m, -(i + 1), edges[0]) for i in range(k)]
            for n, segment in enumerate(datum):
                if segment in k_gram:
                    projection += [(m, n, segment)]
            projection += [(m, len(datum) + i, edges[1]) for i in range(k)]
        projection.sort()
        blocker_sets = set()
        for offset in range(len(projection) - k + 1):
            M, N, segments = zip(*projection[offset:(offset + k)])
            if segments == k_gram and all(m == M[0] for m in M):
                blocker_set = set()
                for n1, n2 in zip(N[:-1], N[1:]):
                    blocker_set |= set(data[M[0]][(n1 + 1):n2])
                blocker_sets.add(tuple(sorted(blocker_set)))
        blockers = set(blocker for blocker_set in blocker_sets for blocker in blocker_set)
        if blocker_sets:
            if () in blocker_sets:
                continue
            for blocker in sorted(blockers, reverse=True):
                if all(blockers - {blocker} & set(blocker_set) for blocker_set in blocker_sets):
                    blockers -= {blocker}
        tier = tuple(sorted({*k_gram, *blockers} - {*edges}))
        grammar[tier].add(k_gram)
    return dict(grammar)
