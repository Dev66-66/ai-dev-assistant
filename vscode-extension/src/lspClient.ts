import * as net from "net";
import {
  LanguageClient,
  LanguageClientOptions,
  RevealOutputChannelOn,
  ServerOptions,
  StreamInfo,
  Trace,
} from "vscode-languageclient/node";

const LSP_HOST = "127.0.0.1";
const LSP_PORT = 2087;

let _client: LanguageClient | undefined;

export function createLspClient(): LanguageClient {
  const serverOptions: ServerOptions = () => {
    const socket = net.createConnection({ host: LSP_HOST, port: LSP_PORT });
    const result: StreamInfo = { writer: socket, reader: socket };
    return Promise.resolve(result);
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [{ scheme: "file", language: "python" }],
    outputChannelName: "AI Dev Assistant",
    revealOutputChannelOn: RevealOutputChannelOn.Info,
  };

  _client = new LanguageClient(
    "aiDevAssistant",
    "AI Dev Assistant",
    serverOptions,
    clientOptions
  );

  _client.setTrace(Trace.Verbose);

  return _client;
}

export async function stopLspClient(): Promise<void> {
  if (_client) {
    await _client.stop();
    _client = undefined;
  }
}
