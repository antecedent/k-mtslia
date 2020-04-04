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

def map_k_gram_to_blockers(k_gram, data, edges):
    k = len(k_gram)
    projection = []
    for m, datum in enumerate(data):
        projection += [(m, -1, edges[0]) for i in range(k - 1)]
        for n, segment in enumerate(datum):
            if segment in k_gram:
                projection += [(m, n, segment)]
        projection += [(m, len(datum), edges[1]) for i in range(k - 1)]
    blocker_cnf = set()
    for offset in range(len(projection) - k + 1):
        M, N, segments = zip(*projection[offset:(offset + k)])
        if segments == k_gram and all(m == M[0] for m in M):
            blocker_clause = set()
            for n1, n2 in zip(N[:-1], N[1:]):
                blocker_clause |= set(data[M[0]][(n1 + 1):n2])
            blocker_cnf.add(tuple(sorted(blocker_clause)))
    return k_gram, tuple(sorted(set(blocker_cnf)))

def extract_tier_no_overlap(blocker_cnf, k_gram, edges):
    blockers = set(blocker for blocker_clause in blocker_cnf for blocker in blocker_clause)
    if blocker_cnf:
        for blocker in sorted(blockers, reverse=True):
            if all(blockers - {blocker} & set(blocker_clause) for blocker_clause in blocker_cnf):
                blockers -= {blocker}
    return tuple((element,) for element in sorted({*blockers} - {*edges}))

def learn(data, k=2, overlap=True, edges=('>', '<'), runner=itertools.starmap):
    alpha = extract_alphabet(data)
    attested = extract_local_k_grams(data, k, edges)
    grammar = collections.defaultdict(set)
    k_grams = itertools.product(alpha | {*edges}, repeat=k)
    runner_result = runner(
        map_k_gram_to_blockers,
        ((k_gram, data, edges) for k_gram in k_grams \
         if valid_k_gram(k_gram, edges) and k_gram not in attested)
    )
    grammar = ()
    for k_gram, blocker_cnf in runner_result:
        if () in blocker_cnf:
            continue
        if overlap:
            grammar += ((k_gram, blocker_cnf),)
        else:
            grammar += ((k_gram, extract_tier_no_overlap(blocker_cnf, k_gram, edges)),)
    return grammar

def scan(string, grammar, edges=('>', '<')):
    for k_gram, blocker_cnf in grammar:
        k_gram, scan_cnf = map_k_gram_to_blockers(k_gram, (string,), edges)
        for scan_clause in scan_cnf:
            if all(not {*blocker_clause}.issubset({*scan_clause}) for blocker_clause in blocker_cnf):
                return False
    return True
