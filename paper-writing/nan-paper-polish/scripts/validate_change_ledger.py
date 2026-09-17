#!/usr/bin/env python3
"""Validate traceability between an original, revision, and Nan-paper-polish change ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    'change_id',
    'location',
    'change_type',
    'original',
    'revised',
    'reason',
    'criteria',
    'root_cause',
    'tags',
    'meaning_effect',
    'author_confirmation',
}
ALLOWED_TYPES = {'replace', 'delete', 'add', 'move', 'split', 'merge', 'global'}
ORIGINAL_SENTINELS = {'', '[none]', '[无]'}
REVISED_SENTINELS = {'', '[deleted]', '[删除]'}
GENERIC_REASONS = {
    'improve readability',
    'improve flow',
    'reads better',
    'more academic',
    'more concise',
    'grammar',
    'style',
}


def normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text or '').strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def load_ledger(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw = json.loads(read_text(path))
    if isinstance(raw, list):
        return {'changes': raw}, raw
    if not isinstance(raw, dict) or not isinstance(raw.get('changes'), list):
        raise ValueError('Ledger must be a JSON object with a changes list, or a list of changes.')
    return raw, raw['changes']


def number_tokens(text: str) -> Counter[str]:
    pattern = r'(?<![\w.])[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?%?'
    return Counter(re.findall(pattern, text))


def protected_latex_tokens(text: str) -> Counter[str]:
    commands = r'\\(?:cite\w*|label|ref|eqref|autoref|cref|Cref)\{([^}]*)\}'
    tokens: list[str] = []
    for payload in re.findall(commands, text):
        tokens.extend(part.strip() for part in payload.split(',') if part.strip())
    return Counter(tokens)


def residual_tokens(
    text: str,
    changes: list[dict[str, Any]],
    side: str,
    tokenizer: Any,
) -> Counter[str]:
    """Remove tokens covered by explicitly authorized protected-content edits."""
    residual = tokenizer(text)
    for change in changes:
        if (
            change.get('protected_change_authorized') is True
            and change.get('author_confirmation') is False
        ):
            residual.subtract(tokenizer(str(change.get(side, ''))))
    return +residual


def meaningful(text: str) -> bool:
    return bool(re.search(r'[\w\u4e00-\u9fff]', text))


def chunk_covered(chunk: str, entries: list[str]) -> bool:
    chunk = normalize(chunk)
    if not meaningful(chunk):
        return True
    if any(chunk in entry for entry in entries):
        return True
    remainder = chunk
    for entry in sorted(entries, key=len, reverse=True):
        if entry and entry in remainder:
            remainder = remainder.replace(entry, ' ')
    return not meaningful(normalize(remainder))


def diff_coverage_errors(original: str, revised: str, changes: list[dict[str, Any]]) -> list[str]:
    source_entries = [
        normalize(str(change.get('original', '')))
        for change in changes
        if normalize(str(change.get('original', ''))).lower() not in ORIGINAL_SENTINELS
    ]
    revised_entries = [
        normalize(str(change.get('revised', '')))
        for change in changes
        if normalize(str(change.get('revised', ''))).lower() not in REVISED_SENTINELS
    ]
    source = normalize(original)
    target = normalize(revised)
    errors: list[str] = []
    matcher = SequenceMatcher(None, source, target, autojunk=False)
    for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
        if opcode == 'equal':
            continue
        old_chunk = source[i1:i2]
        new_chunk = target[j1:j2]
        if old_chunk and not chunk_covered(old_chunk, source_entries):
            errors.append(f'Unaccounted original change span: {old_chunk[:120]!r}')
        if new_chunk and not chunk_covered(new_chunk, revised_entries):
            errors.append(f'Unaccounted revised change span: {new_chunk[:120]!r}')
    return errors


def validate(original: str, revised: str, ledger: dict[str, Any], changes: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    original_norm = normalize(original)
    revised_norm = normalize(revised)

    for index, change in enumerate(changes, start=1):
        prefix = f'Change #{index}'
        if not isinstance(change, dict):
            errors.append(f'{prefix} is not an object.')
            continue
        missing = sorted(REQUIRED_FIELDS - set(change))
        if missing:
            errors.append(f'{prefix} missing fields: {", ".join(missing)}')
            continue

        change_id = str(change['change_id']).strip()
        if not re.fullmatch(r'CH-\d{3,}', change_id):
            errors.append(f'{prefix} has invalid change_id {change_id!r}; expected CH-###.')
        if change_id in seen_ids:
            errors.append(f'Duplicate change_id: {change_id}')
        seen_ids.add(change_id)

        change_type = str(change['change_type']).strip().lower()
        if change_type not in ALLOWED_TYPES:
            errors.append(f'{change_id}: invalid change_type {change_type!r}.')

        if not change['location']:
            errors.append(f'{change_id}: location is empty.')

        reason = normalize(str(change['reason']))
        if not reason:
            errors.append(f'{change_id}: reason is empty.')
        elif reason.lower().rstrip('.') in GENERIC_REASONS:
            errors.append(f'{change_id}: reason is too generic: {reason!r}.')

        criteria = change['criteria']
        if not isinstance(criteria, list) or not criteria or not all(str(item).strip() for item in criteria):
            errors.append(f'{change_id}: criteria must be a non-empty list.')

        if not normalize(str(change['root_cause'])):
            errors.append(f'{change_id}: root_cause is empty.')

        tags = change['tags']
        if not isinstance(tags, list) or not tags or not all(str(tag).strip() for tag in tags):
            errors.append(f'{change_id}: tags must be a non-empty list.')

        if not isinstance(change['author_confirmation'], bool):
            errors.append(f'{change_id}: author_confirmation must be Boolean.')

        old = normalize(str(change['original']))
        new = normalize(str(change['revised']))
        old_is_sentinel = old.lower() in ORIGINAL_SENTINELS
        new_is_sentinel = new.lower() in REVISED_SENTINELS

        if change_type == 'add' and not old_is_sentinel:
            errors.append(f'{change_id}: add must use [none] or an empty original.')
        if change_type != 'add' and old_is_sentinel:
            errors.append(f'{change_id}: non-add change requires exact original text.')
        if change_type == 'delete' and not new_is_sentinel:
            errors.append(f'{change_id}: delete must use [deleted] or an empty revision.')
        if change_type != 'delete' and new_is_sentinel:
            errors.append(f'{change_id}: non-delete change requires exact revised text.')

        if not old_is_sentinel and old not in original_norm:
            errors.append(f'{change_id}: original excerpt not found in source.')
        if not new_is_sentinel and new not in revised_norm:
            errors.append(f'{change_id}: revised excerpt not found in revision.')

    confirmations = [change for change in changes if change.get('author_confirmation') is True]
    questions = ledger.get('author_questions', [])
    if confirmations and (not isinstance(questions, list) or not questions):
        errors.append('Ledger has confirmation-required changes but no author_questions.')

    original_numbers = residual_tokens(original, changes, 'original', number_tokens)
    revised_numbers = residual_tokens(revised, changes, 'revised', number_tokens)
    if original_numbers != revised_numbers:
        errors.append(
            'Protected number tokens changed outside an explicitly authorized, resolved change record.'
        )

    original_latex = residual_tokens(original, changes, 'original', protected_latex_tokens)
    revised_latex = residual_tokens(revised, changes, 'revised', protected_latex_tokens)
    if original_latex != revised_latex:
        errors.append(
            'Protected LaTeX citation/reference tokens changed outside an explicitly authorized, resolved change record.'
        )

    errors.extend(diff_coverage_errors(original, revised, changes))
    return errors


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        original = 'The results prove that X causes Y in 20 participants.'
        revised = 'In 20 participants, the results suggest that X was associated with Y.'
        ledger = {
            'changes': [
                {
                    'change_id': 'CH-001',
                    'location': 'Results, paragraph 1, sentence 1',
                    'change_type': 'replace',
                    'severity': 'major',
                    'original': original,
                    'revised': revised,
                    'reason': 'Calibrates an unsupported causal claim while preserving the sample size.',
                    'criteria': ['EVIDENCE-CLAIM', 'CAUSALITY', 'HEDGING'],
                    'root_cause': 'claim_exceeds_observational_evidence',
                    'tags': ['HEDGE', 'EVIDENCE-CLAIM-MISMATCH'],
                    'meaning_effect': 'narrows_claim',
                    'author_confirmation': True,
                    'protected_change_authorized': False,
                }
            ],
            'author_questions': ['Does the study design support causal inference?'],
        }
        source_path = root / 'original.txt'
        revised_path = root / 'revised.txt'
        ledger_path = root / 'ledger.json'
        source_path.write_text(original, encoding='utf-8')
        revised_path.write_text(revised, encoding='utf-8')
        ledger_path.write_text(json.dumps(ledger), encoding='utf-8')
        loaded, changes = load_ledger(ledger_path)
        errors = validate(read_text(source_path), read_text(revised_path), loaded, changes)
        if errors:
            print('Self-test failed:', *errors, sep='\n- ', file=sys.stderr)
            return 1
        broken = json.loads(json.dumps(ledger))
        broken['changes'][0]['reason'] = 'Improve flow'
        errors = validate(original, revised, broken, broken['changes'])
        if not any('too generic' in error for error in errors):
            print('Self-test failed to reject a generic reason.', file=sys.stderr)
            return 1

        number_change = json.loads(json.dumps(ledger))
        number_change['changes'][0]['revised'] = revised.replace('20', '21')
        errors = validate(original, number_change['changes'][0]['revised'], number_change, number_change['changes'])
        if not any('number tokens changed' in error for error in errors):
            print('Self-test failed to reject an unresolved number change.', file=sys.stderr)
            return 1

        number_change['changes'][0]['protected_change_authorized'] = True
        number_change['changes'][0]['author_confirmation'] = False
        number_change['author_questions'] = []
        errors = validate(original, number_change['changes'][0]['revised'], number_change, number_change['changes'])
        if errors:
            print('Self-test failed to accept an explicitly authorized number change:', *errors, sep='\n- ', file=sys.stderr)
            return 1
    print('validate_change_ledger.py self-test passed')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', type=Path)
    parser.add_argument('--revised', type=Path)
    parser.add_argument('--ledger', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not all((args.original, args.revised, args.ledger)):
        parser.error('--original, --revised, and --ledger are required unless --self-test is used.')

    try:
        ledger, changes = load_ledger(args.ledger)
        errors = validate(read_text(args.original), read_text(args.revised), ledger, changes)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'Validation error: {exc}', file=sys.stderr)
        return 2

    if errors:
        print('Change ledger validation failed:', file=sys.stderr)
        for error in errors:
            print(f'- {error}', file=sys.stderr)
        return 1
    print(f'Change ledger validation passed ({len(changes)} changes).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
