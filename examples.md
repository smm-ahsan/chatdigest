# Examples

## Sample transcript

Saved as `/tmp/chat.txt`:

```
Sara: Did everyone review the new menu draft?
Ahsan: I will send the final prices by tomorrow.
Sara: We decided to launch on Monday, agreed by all.
Tom: Can we get the photos ready by Friday?
Ahsan: The photos are confirmed, Tom will shoot them.
Tom: Please book the studio for Saturday.
Sara: Looks good to me.
System update line without name
```

## Command

```bash
python3 chatdigest.py --file /tmp/chat.txt
```

## Real output

```
Participants:
Sara: 3 messages
Ahsan: 2 messages
Tom: 2 messages

Questions:
- Sara: Did everyone review the new menu draft?
- Tom: Can we get the photos ready by Friday?

Decisions:
- Sara: We decided to launch on Monday, agreed by all.
- Ahsan: The photos are confirmed, Tom will shoot them.

Action items:
- Ahsan: I will send the final prices by tomorrow.
- Tom: Can we get the photos ready by Friday?
- Tom: Please book the studio for Saturday.

Ignored 1 lines without a 'Name:' prefix.
```

Note how Tom's photos message appears twice - once under Questions (it ends
with `?`) and once under Action items (it contains `by Friday`). That is
expected: a message can belong to several sections.

The last line of the transcript, `System update line without name`, has no
`Name: ` prefix, so it is skipped and counted in the "Ignored" note at the
end.
