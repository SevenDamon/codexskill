"""Validate selected platform coverage and copy fields in a publishing package."""
import argparse
import json
from pathlib import Path


def validate_package(package):
    limits = package.get('title_limits')
    if not isinstance(limits, dict) or not limits:
        raise ValueError('title_limits must contain the selected platforms and limits')
    for platform, limit in limits.items():
        if not isinstance(platform, str) or not platform.strip():
            raise ValueError('platform names must be non-empty strings')
        if type(limit) is not int or limit < 1:
            raise ValueError(f'{platform}: title limit must be a positive integer')

    clips = package.get('clips')
    if not isinstance(clips, list) or not clips:
        raise ValueError('clips must be a non-empty list')

    errors = []
    titles = []
    for index, clip in enumerate(clips, 1):
        if not isinstance(clip, dict):
            errors.append(f'clip {index}: expected an object')
            continue
        clip_id = clip.get('id', str(index))
        posts = clip.get('posts')
        if not isinstance(posts, list):
            errors.append(f'{clip_id}: posts must be a list')
            continue
        seen = set()
        for post in posts:
            if not isinstance(post, dict):
                errors.append(f'{clip_id}: each post must be an object')
                continue
            platform = post.get('platform')
            if not isinstance(platform, str) or platform not in limits:
                errors.append(f'{clip_id}: post platform must have a configured limit')
                continue
            label = f'{clip_id}/{platform}'
            if platform in seen:
                errors.append(f'{label}: duplicate platform post')
            seen.add(platform)

            title = post.get('title')
            if not isinstance(title, str) or not title.strip():
                errors.append(f'{label}: title must be non-empty text')
            else:
                count = len(title)
                titles.append(dict(clip=clip_id, platform=platform, title=title,
                                   count=count, limit=limits[platform]))
                if '\n' in title or '\r' in title:
                    errors.append(f'{label}: title must be a single line')
                if count > limits[platform]:
                    errors.append(f'{label}: title has {count} characters, limit {limits[platform]}')

            description = post.get('description')
            if not isinstance(description, str) or not description.strip():
                errors.append(f'{label}: description must be non-empty text')
            topics = post.get('topics')
            if not isinstance(topics, list):
                errors.append(f'{label}: topics must be a list, which can be empty')
            elif any(not isinstance(topic, str) or not topic.strip() for topic in topics):
                errors.append(f'{label}: each topic must be non-empty text')

        missing = set(limits) - seen
        if missing:
            errors.append(f'{clip_id}: missing platform posts for {", ".join(sorted(missing))}')

    return dict(valid=not errors, titles=titles, errors=errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path, help='UTF-8 publish-package.json')
    args = parser.parse_args()
    try:
        package = json.loads(args.package.read_text(encoding='utf-8-sig'))
        if not isinstance(package, dict):
            raise ValueError('the package must be a JSON object')
        report = validate_package(package)
    except (OSError, UnicodeError, ValueError) as error:
        report = dict(valid=False, titles=[], errors=[str(error)])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
