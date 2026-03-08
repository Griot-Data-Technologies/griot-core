# CHANGELOG


## v0.9.1 (2026-03-08)

### Bug Fixes

- Resolve PermissionError in release pipeline build step
  ([`678e1ee`](https://github.com/griot-data/griot-core/commit/678e1eef3504dc9b7b3198fc03150aac6309c449))

Remove build_command from semantic-release config so it only handles versioning and tagging. The
  build is done separately with a clean dist/ directory to avoid permission conflicts with
  hatchling.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.9.0 (2026-03-08)

### Chores

- **release**: V0.9.0
  ([`eee232e`](https://github.com/griot-data/griot-core/commit/eee232e778f2c1e842ecad6e00938a2f6d020e26))

### Features

- Initial PyPI release
  ([`f00bd2b`](https://github.com/griot-data/griot-core/commit/f00bd2b1afa93ccaa6c72ea7ac4509a7dd7b2ca8))


## v0.8.0 (2026-03-08)

### Features

- Add PyPI packaging and CI/CD release pipeline
  ([`a02917d`](https://github.com/griot-data/griot-core/commit/a02917dad6739c511d2dc77487deb84902188d1a))

Set up automated publishing to PyPI using python-semantic-release with conventional commits for
  version management, Trusted Publishing (OIDC) for auth, and GitHub Actions for CI (lint,
  typecheck, test, build) on PRs and automated releases on push to main.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
