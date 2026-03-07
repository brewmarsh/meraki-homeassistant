module.exports = async ({ github, context }) => {
  const title = '🚨 Staging Smoke Test Failed';
  const { data: issues } = await github.rest.issues.listForRepo({
    owner: context.repo.owner,
    repo: context.repo.repo,
    state: 'open',
  });

  const existingIssue = issues.find((issue) => issue.title === title);
  if (existingIssue) {
    console.log(`Issue already exists: ${existingIssue.html_url}`);
    return;
  }

  const failedStep = process.env.FAILED_STEP_NAME || 'Unknown Step';
  let errorDetails = process.env.CI_ERROR_DETAILS || 'No details captured.';

  // Special handling for HA_USERNAME error
  if (errorDetails.includes('HA_USERNAME and HA_PASSWORD environment variables must be set')) {
    errorDetails =
      '❌ **Missing Credentials:** Playwright tests failed because `HA_USERNAME` and `HA_PASSWORD` are not set in the environment.\n\n' +
      'Please ensure these secrets are correctly configured in the repository settings and passed to the workflow.';
  } else if (errorDetails.startsWith('[') && errorDetails.endsWith(']')) {
    // Parse Python-style array strings into clean Markdown lists
    try {
      const items = errorDetails
        .slice(1, -1)
        .split(',')
        .map((s) => s.trim().replace(/^'|'$/g, '').replace(/^"|"$/g, ''));
      if (items.length > 0 && items[0] !== '') {
        errorDetails = items.map((item) => `- \`${item}\``).join('\n');
      }
    } catch (e) {
      errorDetails = `\`\`\`text\n${errorDetails}\n\`\`\``;
    }
  } else {
    errorDetails = `\`\`\`text\n${errorDetails}\n\`\`\``;
  }

  const commitSha = context.sha.substring(0, 7);
  const branch = context.ref.replace('refs/heads/', '');
  const actor = context.actor;

  let body =
    `The deployment to the staging environment failed.\n\n` +
    `### ❌ Failed Step: \`${failedStep}\`\n\n` +
    `### 📋 Error Details\n${errorDetails}\n\n`;

  if (failedStep === 'Run E2E tests') {
    body +=
      `### 🕵️ Playwright Trace\n` +
      `A Playwright trace has been recorded. You can download the \`playwright-trace\` artifact from the **Artifacts** section of this workflow run and view it at [trace.playwright.dev](https://trace.playwright.dev/).\n\n`;
  }

  body +=
    `---\n### 🔍 Contextual Traceability\n` +
    `- **Commit:** [\`${commitSha}\`](${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/commit/${context.sha})\n` +
    `- **Branch:** \`${branch}\`\n` +
    `- **Triggered by:** @${actor}\n\n` +
    `[🔗 View full failing run details](${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId})`;

  await github.rest.issues.create({
    owner: context.repo.owner,
    repo: context.repo.repo,
    title: title,
    body: body,
    labels: ['bug', 'automated-ci', 'jules'],
  });
};
