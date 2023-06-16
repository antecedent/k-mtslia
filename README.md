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
