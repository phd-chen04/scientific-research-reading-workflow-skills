# scientific research reading workflow-skills

[中文](README.md) · **English**

You might already have a routine: save papers in Zotero, read and annotate them in Xiaolvjing, ask ChatGPT when something is unclear, and turn a few papers into slides for a lab meeting.

The hard part often comes later. You remember reading a paper, but where did you put that note? What did you ask about it? Did you ever use it in a presentation?

This workflow brings those records together in Obsidian. Keep reading the way you normally do. When you want to catch up on your notes, tell Codex:

> Update my reading notes.

Codex works through the sources it can access and adds the notes, discussions, and presentation references to your literature library.

## What it helps with

- **Keep a paper's records together.** Link its Xiaolvjing notes, relevant ChatGPT discussions, and slide references from one paper note.
- **Include notes even without slides.** A meaningful annotation or remark is enough. Presentation use is tracked separately.
- **Pick up where you left off.** Add new notes and changes in your understanding while keeping your own judgments intact.
- **Keep your familiar folders.** Use the original Zotero or Xiaolvjing categories. A paper can appear in several indexes without duplicating its note.
- **Avoid interrupting your work.** Prefer a separate, signed-in browser page over desktop control. Anything unavailable stays on the list for a later pass.

It fits regular paper reading, lab-meeting preparation, and the gradual cleanup of a scattered literature library. You can also start with just a few papers.

## Install as a Codex plugin

### Install from a downloaded folder

1. Download and extract this repository. Open a terminal at the **repository root**.
2. If Codex CLI is installed, run:

```sh
codex plugin marketplace add .
codex plugin add scientific-research-reading-workflow-skills@scientific-reading
```

3. Start a new Codex chat after installation.

The commands register this repository's marketplace and install its plugin. The required manifests are included. Interfaces may differ between versions; see the [OpenAI plugin instructions](https://developers.openai.com/plugins/build/plugins).

Without the CLI, open the repository as a project in a desktop client that supports local marketplaces. In the plugin directory, choose **Scientific Reading** and install this plugin. If that option is unavailable, use the [manual skill installation](docs/INSTALL.md).

This project is distributed through its repository. A GitHub release does not mean it is listed in the official plugin directory.

## What you need

Start with a Codex environment that supports skills and an Obsidian vault Codex can write to. Connect the sources you use; you do not need all of them on day one.

| What you want to include | What to provide |
|---|---|
| Zotero papers and collections | An available Zotero connection, or an exported bibliography |
| Xiaolvjing notes and remarks | A signed-in web session and a browser tool Codex can use; existing exports also work |
| ChatGPT paper discussions | Selected conversations and a tool that can read them, or excerpts/exports you provide |
| Presentation slides | The local file location; reviewing images and equations requires access to the rendered slides |

Installing this plugin does not give Codex access to those accounts or files. It checks what is available when you first use it.

You do not need to run Python for the normal workflow. Python 3.10 or later is only needed for the optional initialization and audit scripts.

## Your first run

Send Codex something like this, replacing the paths. Leave out any sources you do not use.

```text
Use $scientific-research-reading-workflow-skills to organize my reading notes.

My Obsidian vault is at: [your path]
I use Zotero and Xiaolvjing to read papers.
My presentation file is at: [your path, if any]
The relevant ChatGPT discussions are: [selected chats or excerpts]

Check which sources you can read, then organize my notes.
Keep the original folder categories and my own judgments.
Do not control my desktop apps.
```

The setup is saved in your own vault, so you do not have to repeat it each time. If Xiaolvjing asks you to sign in again, complete the login yourself. Keep passwords and session credentials out of the configuration.

## Everyday prompts

The usual request is enough:

```text
Update my reading notes.
```

Or be more specific:

```text
Organize papers I read in the last two weeks and revisit sources that were unavailable last time.
Only include notes from my “Research topic” folder in Xiaolvjing.
Add this paper discussion to its note and keep my earlier comments.
Check whether these papers appear in the presentation I selected, and record the slide numbers.
Only check the library structure. Do not change anything yet.
```

After each run, Codex reports which papers changed, where the notes are saved, and what it could not read.

## Where your notes go

The default starting page is `Reading/INDEX.md` inside your Obsidian vault:

- `papers/`: one main note per paper.
- `collections/`: indexes based on your original folders.
- `discussions/` and `presentations/`: related conversations and slide references.
- `updates/`: changes and follow-ups from each run.

Already have a note format you like? Ask Codex to keep it. The detailed conventions are in the [archive reference](skills/scientific-research-reading-workflow-skills/references/schema.md).

## A few things to know

The workflow runs when you ask. It is not an always-on sync service. Xiaolvjing testing so far mainly covers web note text and remarks in the paper list; images, handwriting, and PDF annotations depend on what the available tools can actually read.

AI explanations stay separate from your own judgments. A failed text search in a slide deck does not become a claim that you never presented the paper. Incomplete coverage is recorded.

Keep your real notes, chats, papers, and slide decks in your private library. They do not belong in this public repository.

## Make it your own

These are ordinary files you can edit directly:

| What to change | Where to edit |
|---|---|
| Chinese introduction, instructions, and examples | `README.md` |
| English introduction and instructions | `README.en.md` |
| How Codex organizes reading notes | `skills/scientific-research-reading-workflow-skills/SKILL.md` |
| The default configuration example for new users | `skills/scientific-research-reading-workflow-skills/assets/workflow.example.json` |
| Your vault path, presentations, and source scope | `Reading/workflow.json` in your private vault |

The two READMEs are independent Markdown files. No generator is needed. When you edit one, update the other to match; the packaging tool reads these files without rewriting them.

[Maintenance and checks](docs/MAINTAINING.md) · [Validation record](docs/VALIDATION.md) · [Publishing to GitHub](docs/PUBLISHING.md)

## License

[MIT](LICENSE). Adapt it to your reading habits and share your improvements.
