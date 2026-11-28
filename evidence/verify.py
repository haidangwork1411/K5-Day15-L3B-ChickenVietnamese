"""Validate TV3 evidence artifacts without contacting a service or changing Git."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'


def main():
    spec = importlib.util.spec_from_file_location('evidence_count', E / 'count.py')
    counter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(counter)
    computed = counter.calculate(E / 'public-reviews/reviews.csv')
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
    baseline = '58632f5f794120b4efbabaef75f480b3171edf7d'
    protected = ['spec.md','canvas.md','eval/metric_spec.yaml','eval/benchmark.csv','data/DATA_CARD.md',
                 'codebase/agent.py','codebase/ai.py','codebase/tools.py','codebase/tracing.py',
                 'eval/run_eval.py','cost/simulate.py','run.py']
    hashes = {}
    for name in protected:
        original = subprocess.check_output(['git','show',baseline+':'+name],cwd=ROOT)
        current = (ROOT/name).read_bytes().replace(b'\r\n',b'\n')
        assert original.replace(b'\r\n',b'\n') == current, name+' differs from CP2 baseline'
        hashes[name] = hashlib.sha256(current).hexdigest()
    assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip(), 'Unexpected staged changes'
    changed = subprocess.check_output(['git','diff','--name-only','-z',baseline],cwd=ROOT).decode('utf8').split('\0')
    untracked = subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode('utf8').split('\0')
    assert all(name.startswith('evidence/') for name in changed+untracked if name), 'Changes outside TV3 ownership'
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    print(json.dumps({'verified':True,'reviews':computed['N'],'counts':computed['counts'],
        'case_sources':len(cases),'protected_baseline_files':len(hashes),
        'counts_reproduced':True,'impact_arithmetic_verified':True,
        'staged_files':0,'ownership_scope':'evidence/ only','git_diff_check':'passed','human_review':'pending'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
