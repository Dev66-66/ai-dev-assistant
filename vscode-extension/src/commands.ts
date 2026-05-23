import * as vscode from "vscode";

const BACKEND_URL = "http://localhost:8000";

async function postJson(path: string, body: object): Promise<Response> {
  return fetch(`${BACKEND_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

async function generateTests(): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const selection = editor.selection;
  const code = selection.isEmpty
    ? editor.document.getText()
    : editor.document.getText(selection);

  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: "Generating tests..." },
    async () => {
      const resp = await postJson("/tests/", { code, language: "python" });
      const data = (await resp.json()) as { tests: string };

      const doc = await vscode.workspace.openTextDocument({
        language: "python",
        content: data.tests,
      });
      await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
    }
  );
}

async function generateDocs(): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const selection = editor.selection;
  if (selection.isEmpty) {
    vscode.window.showWarningMessage("Select a function or class first.");
    return;
  }

  const code = editor.document.getText(selection);

  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: "Generating docstring..." },
    async () => {
      const resp = await postJson("/docs/", { code, language: "python" });
      const data = (await resp.json()) as { docstring: string };
      const docstring = `"""\n${data.docstring}\n"""`;

      await editor.edit((eb) => {
        eb.insert(selection.start, docstring + "\n");
      });
    }
  );
}

export function registerCommands(context: vscode.ExtensionContext): void {
  context.subscriptions.push(
    vscode.commands.registerCommand("aiDevAssistant.generateTests", generateTests),
    vscode.commands.registerCommand("aiDevAssistant.generateDocs", generateDocs)
  );
}
