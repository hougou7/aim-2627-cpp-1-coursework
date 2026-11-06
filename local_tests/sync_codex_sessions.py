import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Copy this coursework\'s interactive Codex sessions.'
    )
    parser.add_argument(
        '--source', type=Path, default=Path.home() / '.codex' / 'sessions'
    )
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    source = args.source.expanduser().resolve()
    destination = repository / '.agent-sessions' / 'source' / 'codex'
    if not source.is_dir():
        parser.error('The Codex session directory does not exist.')
    copied = 0
    for path in sorted(source.glob('[0-9][0-9][0-9][0-9]/*/*/rollout-*.jsonl')):
        if path.is_symlink() or not path.is_file():
            continue
        if any(parent.is_symlink() for parent in path.parents
               if parent != source and source in parent.parents):
            continue
        with path.open('rb') as stream:
            header = stream.readline()
        try:
            record = json.loads(header)
        except (ValueError, UnicodeDecodeError):
            continue
        metadata = record.get('payload', {})
        if record.get('type') != 'session_meta':
            continue
        session_source = metadata.get('source')
        if not isinstance(session_source, str) or session_source not in {
                'cli', 'vscode'}:
            continue
        workdir = metadata.get('cwd')
        if not isinstance(workdir, str):
            continue
        workdir_path = Path(workdir).resolve()
        if workdir_path != repository and repository not in workdir_path.parents:
            continue
        payload = path.read_bytes()
        if not payload.endswith(b'\n'):
            raise RuntimeError('Session is being written; run the sync again.')
        for line in payload.splitlines():
            json.loads(line)
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        if target.read_bytes() != payload:
            raise RuntimeError('Copied session does not match its source.')
        copied += 1
    print(f'Copied {copied} project sessions to {destination}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
