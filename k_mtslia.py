import itertools
import collections

def conjoin_dnf(*dnfs):
    if not dnfs:
        return ()
    if len(dnfs) == 1:
        return dnfs[0]
    while len(dnfs) > 2:
        first, second, *rest = tuple(dnfs)
        dnfs = (conjoin_dnf(first, second),) + tuple(rest)
    dnf1, dnf2 = dnfs
    result = set()
    for clause1 in dnf1:
        for clause2 in dnf2:
            result.add(tuple(sorted({*clause1, *clause2})))
    return tuple(sorted(result))

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

def map_k_gram_to_tiers(k_gram, data, edges):
    k = len(k_gram)
    projection = []
    for m, datum in enumerate(data):
        projection += [(m, -1, edges[0]) for i in range(k - 1)]
        for n, segment in enumerate(datum):
            if segment in k_gram:
                projection += [(m, n, segment)]
        projection += [(m, len(datum), edges[1]) for i in range(k - 1)]
    blocker_sets = set()
    for offset in range(len(projection) - k + 1):
        M, N, segments = zip(*projection[offset:(offset + k)])
        if segments == k_gram and all(m == M[0] for m in M):
            blocker_set = set()
            for n1, n2 in zip(N[:-1], N[1:]):
                blocker_set |= set(data[M[0]][(n1 + 1):n2])
            blocker_sets.add(tuple(sorted((blocker,) for blocker in blocker_set)))
    blocker_sets = tuple(blocker_sets)
    tiers = tuple(tuple(sorted({*k_gram, *tier} - {*edges})) for tier in conjoin_dnf(*blocker_sets))    
    return k_gram, tiers

def learn(data, k=2, runner=itertools.starmap, edges=('>', '<')):
    alpha = extract_alphabet(data)
    attested = extract_local_k_grams(data, k, edges)
    grammar = collections.defaultdict(set)
    k_grams = itertools.product(alpha | {*edges}, repeat=k)
    runner_result = runner(
        map_k_gram_to_tiers,
        ((k_gram, data, edges) for k_gram in k_grams \
         if valid_k_gram(k_gram, edges) and k_gram not in attested)
    )
    for k_gram, tiers in runner_result:
        for tier in tiers:
            if tier == ():
                continue
            grammar[tier].add(k_gram)    
    return dict(grammar)
