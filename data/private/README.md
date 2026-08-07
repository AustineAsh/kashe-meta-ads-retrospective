# Private source location

The original workbook is **not committed** because one historical campaign name contains a WhatsApp phone number.

To reproduce the pipeline locally, place the verified source workbook here as:

`data/private/30-01-23.xlsx`

Expected SHA-256:

`5facbe664cfd86bdc64822ed081c43668637a67dff59ce754dc97eb5397e5dc0`

Then run:

```bash
python -m scripts.run_pipeline
```

The preparation script checks the hash by default before regenerating the public dataset.
