#!/usr/bin/env python3
"""Generate per-target CHPL metadata files from the bulk download.

Usage:
    python3 wiggum/build-metadata.py

Reads:  chpl-data/all-active-listings.json, work/targets.json
Writes: work/target-metadata/NNNN.json (one per target)
"""
import json, os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BULK = os.path.join(ROOT, 'chpl-data', 'all-active-listings.json')
TARGETS = os.path.join(ROOT, 'work', 'targets.json')
OUTDIR = os.path.join(ROOT, 'work', 'target-metadata')


def fmt_date(val):
    if isinstance(val, (int, float)):
        return datetime.fromtimestamp(val / 1000, tz=timezone.utc).strftime('%Y-%m-%d')
    if isinstance(val, str) and val:
        return val[:10]
    return None


def get_status(listing):
    for key in ('currentStatus', 'certificationStatus'):
        cs = listing.get(key)
        if isinstance(cs, dict) and cs.get('name'):
            return cs['name']
        if isinstance(cs, str) and cs:
            return cs
    return 'Active'


def strip_empty(obj):
    """Recursively remove keys whose value is an empty string."""
    if isinstance(obj, dict):
        return {k: strip_empty(v) for k, v in obj.items() if v != ''}
    if isinstance(obj, list):
        return [strip_empty(v) for v in obj]
    return obj


def main():
    with open(BULK) as f:
        listings = json.load(f)
    by_id = {l['id']: l for l in listings}

    with open(TARGETS) as f:
        targets = json.load(f)

    os.makedirs(OUTDIR, exist_ok=True)

    for idx, target in enumerate(targets):
        products = []
        for chpl_id in target['chpl_ids']:
            listing = by_id.get(chpl_id)
            if not listing:
                continue
            criteria = sorted([
                cr['criterion']['number']
                for cr in listing.get('certificationResults', [])
                if cr.get('success') and cr.get('criterion', {}).get('number')
            ])
            products.append({
                'chpl_id': listing['id'],
                'chpl_product_number': listing.get('chplProductNumber', ''),
                'product_name': listing.get('product', {}).get('name', ''),
                'version': listing.get('version', {}).get('version', ''),
                'certification_date': fmt_date(listing.get('certificationDate')),
                'certification_status': get_status(listing),
                'practice_type': (listing.get('practiceType') or {}).get('name'),
                'certified_criteria': criteria,
            })

        first = by_id.get(target['chpl_ids'][0], {})
        dev = first.get('developer', {})
        contact = dev.get('contact') or {}

        meta = {
            'url': target['url'],
            'developer': {
                'name': dev.get('name', ''),
                'website': dev.get('website', ''),
                'contact_name': contact.get('fullName', ''),
                'contact_email': contact.get('email', ''),
                'contact_phone': contact.get('phoneNumber', ''),
            },
            'sed_intended_user_description': first.get('sedIntendedUserDescription') or '',
            'mandatory_disclosures_url': first.get('mandatoryDisclosures') or '',
            'products': products,
        }

        meta = strip_empty(meta)

        with open(os.path.join(OUTDIR, f'{idx:04d}.json'), 'w') as f:
            json.dump(meta, f, indent=2)

    print(f'Wrote {len(targets)} metadata files to {OUTDIR}/')


if __name__ == '__main__':
    main()
