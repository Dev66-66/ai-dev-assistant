import * as vscode from "vscode";
import { createLspClient, stopLspClient } from "./lspClient";
import { registerCommands } from "./commands";

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  const client = createLspClient();
  await client.start();

  registerCommands(context);

  context.subscriptions.push({
    dispose: () => stopLspClient(client),
  });
}

export function deactivate(): void {}
