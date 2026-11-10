# ChatDigest

Turn a pasted chat transcript into a clean digest: who took part, what was asked, what was decided, and what needs doing.

## Transcript format

One message per line, with the speaker's name first:

```
Name: message text
```

For example:

```
Sara: Did everyone review the new menu draft?
Ahsan: I will send the final prices by tomorrow.
```

Lines that do not have a `Name: ` prefix are skipped, and the digest tells you at the end how many were ignored.

## How it works

ChatDigest uses simple keyword matching, not AI. There is no machine learning and nothing is sent anywhere - it is plain text scanning:

- **Questions** are messages whose text ends with `?`.
- **Decisions** are messages containing words like `decided`, `agreed`, `we will go with`, `confirmed` or `final:`.
- **Action items** are messages containing words like `i will`, `you will`, `please`, `todo`, `action:`, `by tomorrow`, `by friday` or `deadline`.

Matching is case-insensitive, and one message can appear in several sections. Because it is only keyword matching, it can miss things phrased unusually and can occasionally catch something that was not really a decision - read the digest as a helpful summary, not the final word.

## Requirements

- Python 3
- Standard library only - nothing to install

## Usage

Digest a transcript saved in a file:

```bash
python3 chatdigest.py --file /tmp/chat.txt
```

Or pass the transcript directly as text:

```bash
python3 chatdigest.py --text "Sara: Did everyone review the new menu draft?"
```

See [examples.md](examples.md) for a full sample transcript and its real output.

## License

MIT License - see [LICENSE](LICENSE). Copyright (c) 2026 Muhammad Ahsan Anwar.
