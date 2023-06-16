# k-mtslia
_k_-MTSLIA algorithm for arbitrary _k_. 

Generalizes the 2-MTSLIA from [(McMullin, Aksënova & De Santo 2019)](http://sites.rutgers.edu/lgsa/wp-content/uploads/sites/50/2018/10/2MTSLIA_SCiL2019abstract_McMullinAksenovaDeSanto.pdf). Lifts any assumptions about tier overlap.

Presented as a poster at SCiL 2023 [(Rudaitis, 2023)](https://scholarworks.umass.edu/scil/vol6/iss1/43/).

## Learning

```python
import k_mtslia

# Learn a MTSL₃ grammar with overlapping tiers
G = k_mtslia.learn(['miimimii', 'uumumu', 'mumumu', 'iimimi'], k=3, overlap=True)
```

## Using the grammar to accept/reject strings

```python
print(
  k_mtslia.scan('mimi', G),  # ⇒ True
  k_mtslia.scan('mumu', G),  # ⇒ True
  k_mtslia.scan('mimu', G),  # ⇒ False
)
```

## Inspecting the grammar

```python
for n_gram, tier_conditions in G:
  print(
    '*' + ''.join(n_gram), 
    ' ∧ '.join('(' + ' ∨ '.join(clause) + ')' for clause in tier_conditions)
  )
```

This prints out the following:

```
*><< (i ∨ m) ∧ (m ∨ u)
*>>< (i ∨ m) ∧ (m ∨ u)
*>u<
*>ui
*>um
*>i<
*>iu
*>im
*>m<
*>mm (i) ∧ (u)
*uu< (m)
*uuu (m)
*uui
*ui<
*uiu
```

and 22 more lines.

Let us interpret the first line of the output. `>` and `<` are word boundary symbols, added automatically to each string by _k_-MTSLIA. `*><<` is the restriction that the trigram `><<` must not occur on certain tiers. The formula `(i ∨ m) ∧ (m ∨ u)` specifies that these are the following tiers:

- {i, m, >, <},
- {i, u, >, <},
- {m, >, <}, 
- and any superset of the above.

In other words, these are the tiers that satisfy the formula _and_ contain the restricted trigram's symbols. 
