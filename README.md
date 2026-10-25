# obsidian-bases-starter

Three ready-to-use Obsidian Bases views (`.base` files) for solo-business workflows:

- `pipeline.base`: deals grouped by stage (expects notes in `Business/Deals` with `status`, `amount`, `next_step` in frontmatter).
- `invoices-due.base`: unpaid invoices, earliest due date first (expects `Business/Invoices` with `status`, `due`, `amount`).
- `weekly-review.base`: Markdown notes touched in the last 7 days, grouped by folder.

Copy the files into your vault, adjust the folder names and frontmatter keys at the top of each file, and open them in Obsidian.

## Check the files

    python validate_bases.py            # checks the three views above
    python validate_bases.py some.base  # checks any other .base file

The validator checks the structure against the official Bases syntax (top-level keys, view types, groupBy shape). It does not run the views in Obsidian.

## Limits (honest)

- Not tested in the Obsidian app yet. Formula and date behaviour (for example `file.mtime > now() - "7d"`) is unverified until you open the views.
- Your frontmatter names must match the ones in each file, or the views will be empty.
- Obsidian's own documentation covers Bases in full. This pack is a starting point, not a replacement.
- Not affiliated with or endorsed by Obsidian.

License: MIT (see LICENSE).
