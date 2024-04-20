# How to contribute

## Commits

I try to follow these guidelines:

* Git commits
  * Short commit message headline (if possible, up to 60 characters)
  * Blank line before message body
  * Message should be like: "Add foo ...", "Fix ..."
  * If you need to do formatting changes like indentation, put them
    into their own commit
* Git workflow
  * Rebase every branch before merging it with --no-ff. Rebasing your
    pull request to the current main branch helps me merging it.
  * No merging main into branches - try to rebase always
  * User branches might be heavily rebased/reordered/squashed because
    I like a clean history


## Code

* No Tabs please
* No trailing whitespace please
* 4 spaces indentation
* Run flake8

## Testing

    pytest tests/test-schema.py

## Contact

IRC: tinita on libera
Matrix: tinita on matrix.org

Check out https://matrix.to/#/#chat:yaml.io for chatting about YAML
