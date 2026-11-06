# Two-Pole Evidence Gates Lab

A small, offline Python reference for handling uncertainty in structured decisions. The evaluator distinguishes evidence-supported findings, controlling gates and the **human decision** that must not be fabricated by software.

## Try it

```bash
python -m unittest discover -s tests -v
```

Read the [method](docs/METHOD.md) and inspect the [fictional example case](examples/example_case.json). A failing required gate produces HOLD; unknown required evidence produces INSUFFICIENT_EVIDENCE. Even READY_FOR_HUMAN_DECISION does not authorize an action.

This is a deterministic educational model, not a safety-certified control system or a substitute for domain review. No network connection, account or personal information is required.

**Use and rights:** Public source viewing only; this repository grants no additional redistribution or derivative-use license. [MANIFEST.sha256](MANIFEST.sha256) lists the included source checksums.
