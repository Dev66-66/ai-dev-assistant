import * as vscode from "vscode";
import { createLspClient, stopLspClient } from "./lspClient";
import { registerCommands } from "./commands";
import { AiInlineCompletionProvider } from "./inlineCompletion";

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  registerCommands(context);

  context.subscriptions.push(
    vscode.languages.registerInlineCompletionItemProvider(
      { language: "python" },
      new AiInlineCompletionProvider()
    )
  );

  const client = createLspClient();
  try {
    await client.start();
    context.subscriptions.push({
      dispose: () => stopLspClient(client),
    });
  } catch {
    vscode.window.showWarningMessage("AI Dev Assistant: LSP server unavailable.");
  }
}

export function deactivate(): void {}
