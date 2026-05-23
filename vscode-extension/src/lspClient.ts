import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
  TransportKind,
} from "vscode-languageclient/node";

const LSP_HOST = "127.0.0.1";
const LSP_PORT = 2087;

let _client: LanguageClient | undefined;

export function createLspClient(): LanguageClient {
  const serverOptions: ServerOptions = {
    run: { transport: { kind: TransportKind.socket, port: LSP_PORT } },
    debug: { transport: { kind: TransportKind.socket, port: LSP_PORT } },
  } as unknown as ServerOptions;

  const clientOptions: LanguageClientOptions = {
    documentSelector: [{ scheme: "file", language: "python" }],
  };

  _client = new LanguageClient(
    "aiDevAssistant",
    "AI Dev Assistant",
    serverOptions,
    clientOptions
  );

  return _client;
}

export async function stopLspClient(client: LanguageClient): Promise<void> {
  await client.stop();
}
