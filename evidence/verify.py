"""Validate TV3 evidence artifacts without contacting a service or changing Git."""
import csv
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re

from count import calculate

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'


def validate_cp4(root):
    """Check saved CP4 provenance and arithmetic; do not certify human activity."""
    folder = root / 'evidence/cp4'

    def read(name):
        return json.loads((folder / name).read_text(encoding='utf-8'))

    manifest = read('cp3-snapshot.json')
    assert manifest['baseline_commit'] == 'c9246a27da9a3238d8015819873ab71279375530'
    required = {
        'evidence/public-reviews/reviews.csv', 'evidence/public-reviews/counts.json',
        'evidence/public-reviews/collection.json', 'evidence/source-cases.csv',
        'evidence/impact-inputs.json', 'evidence/coding-protocol.md',
        'evidence/collection-plan.md', 'evidence/data-mining.md',
        'evidence/hypothesis.md', 'evidence/count.py',
    }
    assert set(manifest['files']) == required, 'CP3 snapshot manifest is incomplete'
    for relative, expected in manifest['files'].items():
        actual = hashlib.sha256((root / relative).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        assert actual == expected, 'CP3 snapshot changed: ' + relative

    ledger = read('supplemental-sources.json')
    records = ledger['records']
    assert len({row['id'] for row in records}) == len(records), 'Duplicate supplemental source'
    date.fromisoformat(ledger['accessed_on'])
    for row in records:
        assert row['kind'] in {'publisher_report', 'public_user_post'}
        assert row['source_url'].startswith('https://')
        assert all(row[key] for key in ('locator', 'date_display', 'interpretation', 'limits'))
        assert row['accessed_on'] == ledger['accessed_on']
        if row['published_on'] is not None:
            assert date.fromisoformat(row['published_on']) <= date.fromisoformat(row['accessed_on'])
        excerpt = row['excerpt']
        assert 0 < len([word for word in excerpt.split() if word != '[…]']) <= 25
        assert len(re.findall(r'[.!?](?:\s|$)', excerpt)) <= 2
        assert hashlib.sha256(excerpt.encode('utf-8')).hexdigest() == row['excerpt_sha256'], row['id']
        for label in ('missing_food', 'complaint_difficulty'):
            if row['kind'] == 'publisher_report':
                assert row[label] is None, 'Publisher reports cannot enter the post denominator'
            else:
                assert type(row[label]) is int and row[label] in (0, 1)
    posts = [row for row in records if row['kind'] == 'public_user_post']
    counts = {
        'publisher_reports': len(records) - len(posts), 'user_posts': len(posts),
        'missing_food_posts': sum(row['missing_food'] for row in posts),
        'complaint_difficulty_posts': sum(row['complaint_difficulty'] for row in posts),
        'both_posts': sum(row['missing_food'] == row['complaint_difficulty'] == 1 for row in posts),
    }
    assert counts == ledger['counts'], 'Supplemental counts or denominators do not match'

    with (root / 'evidence/public-reviews/reviews.csv').open(encoding='utf-8-sig', newline='') as handle:
        reviews = {row['evidence_id']: row for row in csv.DictReader(handle)}
    audit = read('label-audit.json')
    assert audit['reviewer_kind'] == 'AI'
    assert audit['rows_inspected'] == len(reviews)
    hidden = set(audit['unassessable_ids'])
    assert hidden == {key for key, row in reviews.items() if row['excerpt'].startswith('[không trích:')}
    assert audit['excerpts_assessable'] == len(reviews) - len(hidden)
    flags = audit['pending_adjudication']
    assert len({row['evidence_id'] for row in flags}) == len(flags)
    assert audit['unflagged_assessable_rows'] + len(flags) == audit['excerpts_assessable']
    for flag in flags:
        assert flag['evidence_id'] in reviews and flag['evidence_id'] not in hidden
        for label in ('missing_food', 'complaint_difficulty'):
            assert flag['saved'][label] == int(reviews[flag['evidence_id']][label])
        assert flag['proposed_complaint_difficulty'] in (0, 1) and flag['reason']
    confirmed = audit['human_confirmed_rows']
    assert audit['human_confirmed_count'] == len(confirmed), 'Human count needs row-level records'
    for row in confirmed:
        assert row['evidence_id'] in reviews
        assert all(row[key] for key in ('reviewer_alias', 'reviewed_on', 'reason'))
        date.fromisoformat(row['reviewed_on'])
    assert audit['human_actual_total'] is None or audit['human_actual_total'] >= len(confirmed)
    assert audit['label_accuracy'] is None, 'No ground-truth label study is attached'

    impact = json.loads((root / 'evidence/impact-inputs.json').read_text(encoding='utf-8'))
    cost = read('cost-handoff.json')
    assert cost['status'] == 'proposal_for_TV4_not_applied_to_cost_config'
    assert cost['source'].startswith('(tự ước tính)')
    assert cost['population_customers'] == impact['population_is_not_a_survey']
    assert 0 <= cost['assistant_uptake_among_affected'] <= 1
    personas = cost['personas']
    assert len(personas) >= 3 and len({row['name'] for row in personas}) == len(personas)
    assert all(row['share'] > 0 and row['uses_per_month'] > 0
               and type(row['turns_per_session']) is int and row['turns_per_session'] >= 1
               and row['source'].startswith('(tự ước tính)') for row in personas)
    assert math.isclose(sum(row['share'] for row in personas), 1)
    sessions = sum(row['share'] * row['uses_per_month'] for row in personas)
    turns = sum(row['share'] * row['uses_per_month'] * row['turns_per_session'] for row in personas)
    assert math.isclose(sessions, cost['sessions_per_assistant_user_month'])
    assert math.isclose(turns, cost['turns_per_assistant_user_month'])
    for scenario, sensitivity in zip(('low', 'base', 'high'), impact['sensitivity']):
        users = cost['users'][scenario]
        assert math.isclose(users, sensitivity['N'] * cost['assistant_uptake_among_affected'])
        assert 0 <= users <= cost['population_customers']
        assert math.isclose(cost['traffic'][scenario]['sessions_per_month'], users * sessions)
        assert math.isclose(cost['traffic'][scenario]['turns_per_month'], users * turns)
    original = next(row for row in impact['directions'] if row['name'] == 'thiếu món')
    base = cost['base_loss']
    assert (base['affected_people'], base['events_per_affected_person_month'],
            base['active_minutes_per_event']) == (original['N'], original['F'], original['C'])
    assert math.isclose(base['sessions_per_month'], original['N'] * original['F'])
    assert math.isclose(base['active_minutes_per_month'], original['minutes'])
    assert math.isclose(base['minutes_per_affected_person_month'], original['minutes'] / original['N'])
    assert math.isclose(base['minutes_per_baseline_customer_month'], original['minutes'] / cost['population_customers'])
    assert cost['observed_savings_minutes'] is None, 'No measured savings study is attached'
    return {
        'cp3_snapshot_files_unchanged': len(required), 'supplemental_counts': counts,
        'ai_rows_inspected': audit['rows_inspected'], 'assessable_excerpts': audit['excerpts_assessable'],
        'labels_pending_human_adjudication': len(flags), 'human_confirmed_count': len(confirmed),
        'base_sessions_per_month_estimated': base['sessions_per_month'],
        'base_loss_minutes_estimated': base['active_minutes_per_month'],
    }


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
    cp4 = validate_cp4(ROOT)
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
        'cp4': cp4,
    }, ensure_ascii=False, indent=2))


if __name__=='__main__':
    main()
