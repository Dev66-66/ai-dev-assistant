import * as vscode from "vscode";

const BACKEND_URL = "http://localhost:8000";
const DEBOUNCE_MS = 1500;

export class AiInlineCompletionProvider implements vscode.InlineCompletionItemProvider {
  async provideInlineCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position,
    _context: vscode.InlineCompletionContext,
    token: vscode.CancellationToken
  ): Promise<vscode.InlineCompletionList | null> {
    const cancelled = await new Promise<boolean>((resolve) => {
      const timer = setTimeout(() => resolve(false), DEBOUNCE_MS);
      token.onCancellationRequested(() => {
        clearTimeout(timer);
        resolve(true);
      });
    });

    if (cancelled || token.isCancellationRequested) {
      return null;
    }

    try {
      const controller = new AbortController();
      token.onCancellationRequested(() => controller.abort());

      const resp = await fetch(`${BACKEND_URL}/completion/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: document.getText(),
          language: "python",
          cursor_line: position.line,
        }),
        signal: controller.signal,
      });

      if (!resp.ok || token.isCancellationRequested) {
        return null;
      }

      const data = (await resp.json()) as { suggestion: string };
      if (!data.suggestion?.trim()) {
        return null;
      }

      return {
        items: [
          new vscode.InlineCompletionItem(
            data.suggestion,
            new vscode.Range(position, position)
          ),
        ],
      };
    } catch {
      return null;
    }
  }
}
