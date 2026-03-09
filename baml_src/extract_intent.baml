class Intent {
  category string
  confidence float
}

function ExtractIntent(input: string) -> Intent {
  client "openai/gpt-4o"
  prompt #"
    Extract the intent from the following input:
    {{ input }}

    {{ ctx.output_format }}
  "#
}
