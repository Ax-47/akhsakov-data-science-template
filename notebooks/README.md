# Notebooks

Naming convention: `<number>-<initials>-<short-description>.ipynb`, e.g. `01-ma-eda.ipynb`.

Import project code instead of copying it into notebooks:

```python
%load_ext autoreload
%autoreload 2

from ds_project.data import load_example_dataset
```
