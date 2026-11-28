"""Validate TV3 evidence artifacts without contacting a service or changing Git."""
import csv
import json
from pathlib import Path
import re

from count import calculate

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'


def main():
    if not __debug__:
        raise SystemExit('Run evidence/verify.py without -O so all validation checks are active.')
    computed = calculate(E / 'public-reviews/reviews.csv')
    saved = json.loads((E / 'public-reviews/counts.json').read_text(encoding='utf8'))
    assert computed == saved, 'Counts do not match the coded snapshot'
    collection = json.loads((E / 'public-reviews/collection.json').read_text(encoding='utf8'))
    assert collection['eligible_unique_reviews'] == computed['N']
    assert [p['page'] for p in collection['pages']] == [1, 2, 3, 4]
    assert sum(p['returned_reviews'] for p in collection['pages']) - collection['duplicates_excluded'] - collection['blank_excluded'] == computed['N']
    cases = list(csv.DictReader((E / 'source-cases.csv').open(encoding='utf-8-sig', newline='')))
    reviews = {r['evidence_id']:r for r in csv.DictReader((E / 'public-reviews/reviews.csv').open(encoding='utf-8-sig', newline=''))}
    assert len({c['case_source_id'] for c in cases}) == len(cases)
    for case in cases:
        assert all(value for value in case.values()), case['case_source_id']
        assert case['source_url'].startswith('https://')
        if case['source_kind'] == 'public_review':
            source = reviews[case['evidence_id']]
            assert case['source_ref'] == source['source_id']
            assert case['source_url'] == source['source_url']
            assert case['source_date'] == source['review_date']
    impact = json.loads((E / 'impact-inputs.json').read_text(encoding='utf8'))
    assert impact['all_inputs_are_estimates'] is True
    for row in impact['directions'] + impact['sensitivity']:
        assert abs(row['N']*row['F']*row['C']-row['minutes']) < 1e-9
    for doc in E.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text(encoding='utf-8-sig')):
            if not link.startswith(('https://', 'http://', '#')):
                assert (doc.parent / link.split('#')[0]).exists(), (doc.name, link)
    for file in E.rglob('*'):
        if not file.is_file() or file.suffix not in ('.md','.csv','.json'):
            continue
        text = file.read_text(encoding='utf-8-sig')
        assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',text), file.name
    print(json.dumps({
        'verified': True, 'reviews': computed['N'], 'counts': computed['counts'],
        'snapshot_sha256': computed['snapshot_sha256'], 'case_sources': len(cases),
        'counts_reproduced': True, 'impact_arithmetic_verified': True,
        'human_review': 'pending',
    }, ensure_ascii=False, indent=2))


if __name__=='__main__':
    main()
