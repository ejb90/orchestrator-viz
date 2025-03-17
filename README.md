# Visualisation

## Table

Show each step in a Worklow in a Table.

### Usage

```bash
# Database with UUID query
wf-table --source db --path <path/to/db> --uuid <uuid.hex>
# Database with path query
wf-table --source db --path <path/to/db> --path <path/to/workflow/root>

# Pickle with UUID query
wf-table --source pkl --path <path/to/pkl> --uuid <uuid.hex>
# Pickle with path query
wf-table --source pkl --path <path/to/pkl> --path <path/to/workflow/root>

# JSON with UUID query
wf-table --source json --path <path/to/db> --uuid <uuid.hex>
# JSON with path query
wf-table --source json --path <path/to/db> --path <path/to/workflow/root>
```

## Tree

Show the Worklow DAG as a Tree.

### Usage

```bash
# Database with UUID query
wf-tree --source db --path <path/to/db> --uuid <uuid.hex>
# Database with path query
wf-tree --source db --path <path/to/db> --path <path/to/workflow/root>

# Pickle with UUID query
wf-tree --source pkl --path <path/to/pkl> --uuid <uuid.hex>
# Pickle with path query
wf-tree --source pkl --path <path/to/pkl> --path <path/to/workflow/root>

# JSON with UUID query
wf-tree --source json --path <path/to/db> --uuid <uuid.hex>
# JSON with path query
wf-tree --source json --path <path/to/db> --path <path/to/workflow/root>
```

